package com.coralshop.catalog.client;

import com.coralshop.common.exception.ExternalServiceException;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.time.Instant;
import java.time.OffsetDateTime;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;

/**
 * Adaptador de la API de CJ Dropshipping: autentica, respeta su límite de peticiones y
 * traduce sus respuestas JSON a {@link CjSearchPage} y {@link CjProduct}.
 */
@Component
public class CjClient {

    private static final String BASE_URL = "https://developers.cjdropshipping.com/api2.0/v1";
    private final HttpClient http = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(5)).build();
    private final ObjectMapper json;
    private final String apiKey;
    private String accessToken;
    private Instant expiresAt = Instant.EPOCH;
    private long lastRequestNanos;

    public CjClient(ObjectMapper json, @Value("${CJ_API_KEY:}") String apiKey) {
        this.json = json;
        this.apiKey = apiKey;
    }

    public CjSearchPage search(String keyword, int page) {
        JsonNode data = get(BASE_URL + "/product/listV2?page=" + page + "&size=20&keyWord=" +
                URLEncoder.encode(keyword, StandardCharsets.UTF_8));
        List<CjSearchPage.Item> items = new ArrayList<>();
        for (JsonNode group : data.path("content")) {
            for (JsonNode item : group.path("productList")) {
                if (!item.path("id").asText().isBlank()) {
                    items.add(new CjSearchPage.Item(item.path("id").asText(), item.path("nameEn").asText(),
                            item.path("bigImage").asText(), item.path("sellPrice").asText()));
                }
            }
        }
        return new CjSearchPage(items, data.path("totalPages").asInt(0));
    }

    public CjProduct product(String pid) {
        JsonNode data = get(BASE_URL + "/product/query?pid=" + URLEncoder.encode(pid, StandardCharsets.UTF_8));
        List<CjProduct.Variant> variants = new ArrayList<>();
        for (JsonNode item : data.path("variants")) {
            variants.add(new CjProduct.Variant(item.path("vid").asText(), item.path("variantSku").asText(),
                    item.path("variantKey").asText(), item.path("variantSellPrice").asText()));
        }
        return new CjProduct(data.path("pid").asText(), data.path("productNameEn").asText(),
                data.path("bigImage").asText(), data.path("sellPrice").asText(), variants);
    }

    private JsonNode get(String url) {
        String token = token();
        HttpRequest request = HttpRequest.newBuilder(URI.create(url))
                .timeout(Duration.ofSeconds(15)).header("CJ-Access-Token", token).GET().build();
        JsonNode response = send(request);
        if (!response.path("result").asBoolean(false)) {
            throw new ExternalServiceException(HttpStatus.BAD_GATEWAY,
                    "CJ no pudo completar la solicitud; intenta más tarde");
        }
        return response.path("data");
    }

    private synchronized String token() {
        if (apiKey.isBlank()) {
            throw new ExternalServiceException(HttpStatus.SERVICE_UNAVAILABLE,
                    "CJ no está configurado en el servidor (falta CJ_API_KEY)");
        }
        if (accessToken != null && Instant.now().isBefore(expiresAt.minus(Duration.ofMinutes(5)))) {
            return accessToken;
        }
        try {
            HttpRequest request = HttpRequest.newBuilder(URI.create(BASE_URL + "/authentication/getAccessToken"))
                    .timeout(Duration.ofSeconds(15)).header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(json.writeValueAsString(Map.of("apiKey", apiKey))))
                    .build();
            JsonNode response = send(request);
            JsonNode data = response.path("data");
            if (!response.path("result").asBoolean(false) || data.path("accessToken").asText().isBlank()) {
                throw new ExternalServiceException(HttpStatus.BAD_GATEWAY,
                        "Falló la autenticación con CJ; revisa la clave configurada en el servidor");
            }
            accessToken = data.path("accessToken").asText();
            expiresAt = OffsetDateTime.parse(data.path("accessTokenExpiryDate").asText()).toInstant();
            return accessToken;
        } catch (JsonProcessingException exception) {
            throw new ExternalServiceException(HttpStatus.BAD_GATEWAY, "Falló la autenticación con CJ", exception);
        } catch (DateTimeParseException exception) {
            throw new ExternalServiceException(HttpStatus.BAD_GATEWAY,
                    "CJ devolvió una fecha de expiración inválida", exception);
        }
    }

    private synchronized JsonNode send(HttpRequest request) {
        try {
            // CJ limita las cuentas gratuitas a una petición por segundo.
            long remaining = Duration.ofMillis(1100).toNanos() - (System.nanoTime() - lastRequestNanos);
            if (lastRequestNanos != 0 && remaining > 0) {
                TimeUnit.NANOSECONDS.sleep(remaining);
            }
            lastRequestNanos = System.nanoTime();
            HttpResponse<String> response = http.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() == 429) {
                throw new ExternalServiceException(HttpStatus.TOO_MANY_REQUESTS,
                        "Se alcanzó el límite de peticiones de CJ; espera un momento y reintenta");
            }
            if (response.statusCode() < 200 || response.statusCode() >= 300) {
                throw new ExternalServiceException(HttpStatus.BAD_GATEWAY,
                        "CJ no está disponible (HTTP " + response.statusCode() + ")");
            }
            return json.readTree(response.body());
        } catch (InterruptedException exception) {
            Thread.currentThread().interrupt();
            throw new ExternalServiceException(HttpStatus.BAD_GATEWAY, "Se interrumpió la petición a CJ", exception);
        } catch (IOException exception) {
            throw new ExternalServiceException(HttpStatus.BAD_GATEWAY, "No se pudo conectar con CJ", exception);
        }
    }
}
