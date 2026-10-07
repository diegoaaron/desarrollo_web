package com.coralshop.catalog.controller;

import com.coralshop.catalog.dto.CjImportRequest;
import com.coralshop.catalog.dto.CjProductResponse;
import com.coralshop.catalog.dto.CjSearchResponse;
import com.coralshop.catalog.dto.CreatedResponse;
import com.coralshop.catalog.service.CjImportService;
import jakarta.validation.Valid;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

/** Importación selectiva desde CJ Dropshipping (solo ADMIN). */
@RestController
@RequestMapping("/api/admin/cj")
public class CjImportController {

    private final CjImportService cjImportService;

    public CjImportController(CjImportService cjImportService) {
        this.cjImportService = cjImportService;
    }

    @GetMapping("/search")
    public CjSearchResponse search(@RequestParam @Size(min = 2, max = 100) String keyword,
                                   @RequestParam(defaultValue = "1") @Min(1) @Max(1000) int page) {
        return cjImportService.search(keyword, page);
    }

    @GetMapping("/product")
    public CjProductResponse product(@RequestParam @Pattern(regexp = "[A-Za-z0-9-]{1,80}") String pid) {
        return cjImportService.product(pid);
    }

    @PostMapping("/import")
    @ResponseStatus(HttpStatus.CREATED)
    public CreatedResponse importProduct(@Valid @RequestBody CjImportRequest request) {
        return new CreatedResponse(cjImportService.importProduct(request));
    }
}
