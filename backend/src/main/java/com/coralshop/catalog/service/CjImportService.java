package com.coralshop.catalog.service;

import com.coralshop.catalog.client.CjClient;
import com.coralshop.catalog.client.CjProduct;
import com.coralshop.catalog.dto.CjImportRequest;
import com.coralshop.catalog.dto.CjProductResponse;
import com.coralshop.catalog.dto.CjSearchResponse;
import com.coralshop.catalog.model.NewProduct;
import com.coralshop.catalog.repository.ProductRepository;
import com.coralshop.common.exception.BusinessRuleException;
import com.coralshop.common.exception.ConflictException;
import com.coralshop.common.exception.NotFoundException;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

/**
 * Búsqueda e importación selectiva de productos de CJ Dropshipping. La consulta a CJ
 * ocurre fuera de la transacción; solo el registro en la base es transaccional.
 */
@Service
public class CjImportService {

    private static final int MAX_SKU_LENGTH = 80;

    private final CjClient cjClient;
    private final ProductRepository productRepository;
    private final ProductAdminService productAdminService;

    public CjImportService(CjClient cjClient, ProductRepository productRepository,
                           ProductAdminService productAdminService) {
        this.cjClient = cjClient;
        this.productRepository = productRepository;
        this.productAdminService = productAdminService;
    }

    public CjSearchResponse search(String keyword, int page) {
        var result = cjClient.search(keyword.trim(), page);
        List<CjSearchResponse.Item> items = result.items().stream()
                .map(item -> new CjSearchResponse.Item(item.pid(), item.name(), item.imageUrl(), item.sellPrice()))
                .toList();
        return new CjSearchResponse(items, result.totalPages());
    }

    public CjProductResponse product(String pid) {
        CjProduct product = fetch(pid);
        List<CjProductResponse.Variant> variants = product.variants().stream()
                .map(variant -> new CjProductResponse.Variant(variant.vid(), variant.sku(), variant.optionKey(),
                        variant.sellPrice()))
                .toList();
        return new CjProductResponse(pid, product.name(), secureImage(product), product.sellPrice(), variants,
                productRepository.existsByCjProductId(pid));
    }

    public long importProduct(CjImportRequest request) {
        if (productRepository.existsByCjProductId(request.pid())) {
            throw new ConflictException("Este producto de CJ ya fue importado");
        }
        CjProduct product = fetch(request.pid());
        Map<String, String> supplierSkus = product.variants().stream()
                .collect(Collectors.toMap(CjProduct.Variant::vid, CjProduct.Variant::sku, (first, second) -> first));

        Set<String> selected = new HashSet<>();
        List<NewProduct.Variant> variants = request.variants().stream().map(variant -> {
            String supplierSku = supplierSkus.get(variant.vid());
            String sku = "CJ-" + supplierSku;
            if (!selected.add(variant.vid()) || supplierSku == null || supplierSku.isBlank()
                    || sku.length() > MAX_SKU_LENGTH) {
                throw new BusinessRuleException("Selecciona variantes de CJ distintas y con SKU válido");
            }
            return new NewProduct.Variant(variant.sizeId(), variant.colorId(), sku, variant.stock(), variant.vid());
        }).toList();

        // Por defecto la importación queda como borrador: el administrador decide si se publica.
        return productAdminService.register(new NewProduct(request.name().trim(), request.description(),
                request.basePrice(), request.categoryId(), secureImage(product), request.isActive(),
                request.pid(), variants));
    }

    private CjProduct fetch(String pid) {
        CjProduct product = cjClient.product(pid);
        if (!pid.equalsIgnoreCase(product.pid())) {
            throw new NotFoundException("Producto de CJ no encontrado");
        }
        return product;
    }

    private static String secureImage(CjProduct product) {
        if (product.imageUrl() == null || !product.imageUrl().startsWith("https://")) {
            throw new BusinessRuleException("El producto de CJ no tiene una imagen principal segura (HTTPS)");
        }
        return product.imageUrl();
    }
}
