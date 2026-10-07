package com.coralshop.design.controller;

import com.coralshop.common.exception.InvalidRequestException;
import com.coralshop.design.dto.DesignView;
import com.coralshop.design.model.DesignImage;
import com.coralshop.design.service.DesignService;
import com.coralshop.user.service.CurrentUserService;
import java.io.IOException;
import java.time.Duration;
import org.springframework.http.CacheControl;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

/** Diseños del cliente: subida (multipart, campo «file») y descarga de la imagen. */
@RestController
@RequestMapping("/api/designs")
public class DesignController {

    private final DesignService designService;
    private final CurrentUserService currentUserService;

    public DesignController(DesignService designService, CurrentUserService currentUserService) {
        this.designService = designService;
        this.currentUserService = currentUserService;
    }

    @PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    @ResponseStatus(HttpStatus.CREATED)
    public DesignView upload(@RequestParam("file") MultipartFile file, Authentication authentication) {
        try {
            return designService.upload(currentUserService.idOf(authentication), file.getOriginalFilename(),
                    file.getBytes());
        } catch (IOException exception) {
            throw new InvalidRequestException("No se pudo leer el archivo enviado", exception);
        }
    }

    @GetMapping("/{id}/image")
    public ResponseEntity<byte[]> image(@PathVariable Long id, Authentication authentication) {
        DesignImage image = designService.image(id, currentUserService.idOf(authentication),
                currentUserService.isAdmin(authentication));
        return ResponseEntity.ok()
                .contentType(MediaType.parseMediaType(image.contentType()))
                .cacheControl(CacheControl.maxAge(Duration.ofHours(1)).cachePrivate())
                .header("X-Content-Type-Options", "nosniff")
                .body(image.data());
    }
}
