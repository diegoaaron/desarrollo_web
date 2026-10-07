package com.coralshop.catalog.service;

import com.coralshop.catalog.dto.CatalogOptionsResponse;
import com.coralshop.catalog.dto.CreateProductRequest;
import com.coralshop.catalog.dto.ProductView;
import com.coralshop.catalog.model.NewProduct;
import com.coralshop.catalog.repository.CatalogOptionRepository;
import com.coralshop.catalog.repository.ProductRepository;
import com.coralshop.common.exception.BusinessRuleException;
import com.coralshop.common.exception.ConflictException;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/** Mantenimiento del catálogo por el administrador. */
@Service
public class ProductAdminService {

    private final ProductRepository productRepository;
    private final CatalogOptionRepository optionRepository;

    public ProductAdminService(ProductRepository productRepository, CatalogOptionRepository optionRepository) {
        this.productRepository = productRepository;
        this.optionRepository = optionRepository;
    }

    @Transactional(readOnly = true)
    public List<ProductView> allProducts() {
        return productRepository.findAll();
    }

    @Transactional(readOnly = true)
    public CatalogOptionsResponse catalogOptions() {
        return new CatalogOptionsResponse(optionRepository.findSizes(), optionRepository.findColors());
    }

    /** Registra el producto con su imagen principal y variantes en una sola transacción. */
    @Transactional
    public long create(CreateProductRequest request) {
        List<NewProduct.Variant> variants = request.variants().stream()
                .map(variant -> new NewProduct.Variant(variant.sizeId(), variant.colorId(), variant.sku().trim(),
                        variant.stock()))
                .toList();
        NewProduct product = new NewProduct(request.name().trim(), request.description(), request.basePrice(),
                request.categoryId(), request.imageUrl().trim(), request.isActive(), variants);

        if (!optionRepository.isActiveCategory(product.categoryId())) {
            throw new BusinessRuleException("Selecciona una categoría activa");
        }
        Set<String> combinations = new HashSet<>();
        Set<String> skus = new HashSet<>();
        for (NewProduct.Variant variant : product.variants()) {
            if (!combinations.add(variant.sizeId() + ":" + variant.colorId())) {
                throw new BusinessRuleException("Hay variantes repetidas con la misma talla y color");
            }
            if (!skus.add(variant.sku())) {
                throw new BusinessRuleException("Hay variantes con el mismo SKU");
            }
            if (!optionRepository.sizeExists(variant.sizeId()) || !optionRepository.colorExists(variant.colorId())) {
                throw new BusinessRuleException("Selecciona una talla y un color válidos");
            }
        }
        try {
            return productRepository.insert(product);
        } catch (DataIntegrityViolationException exception) {
            throw new ConflictException("Alguno de los SKU ya está registrado", exception);
        }
    }
}
