package com.coralshop.catalog.service;

import com.coralshop.catalog.dto.CatalogOptionsResponse;
import com.coralshop.catalog.dto.CreateProductRequest;
import com.coralshop.catalog.dto.ProductView;
import com.coralshop.catalog.dto.UpdateProductRequest;
import com.coralshop.catalog.model.NewProduct;
import com.coralshop.catalog.model.ProductUpdate;
import com.coralshop.catalog.repository.CatalogOptionRepository;
import com.coralshop.catalog.repository.ProductRepository;
import com.coralshop.common.exception.BusinessRuleException;
import com.coralshop.common.exception.ConflictException;
import com.coralshop.common.exception.NotFoundException;
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

    /** Detalle para el formulario de edición: incluye también las variantes inactivas. */
    @Transactional(readOnly = true)
    public ProductView product(Long id) {
        ProductView product = productRepository.findById(id)
                .orElseThrow(() -> new NotFoundException("Producto no encontrado"));
        return product.withVariants(productRepository.findAllVariants(id));
    }

    @Transactional(readOnly = true)
    public CatalogOptionsResponse catalogOptions() {
        return new CatalogOptionsResponse(optionRepository.findSizes(), optionRepository.findColors(),
                optionRepository.findActiveProductTypes());
    }

    /** Registra el producto con su imagen principal y variantes en una sola transacción. */
    @Transactional
    public long create(CreateProductRequest request) {
        List<NewProduct.Variant> variants = request.variants().stream()
                .map(variant -> new NewProduct.Variant(variant.sizeId(), variant.colorId(), variant.sku().trim(),
                        variant.stock()))
                .toList();
        NewProduct product = new NewProduct(request.name().trim(), request.description(), request.basePrice(),
                request.categoryId(), request.productTypeId(), request.isCustomizable(), request.imageUrl().trim(),
                request.isActive(), variants);

        validateClassification(product.categoryId(), product.productTypeId(), product.customizable());
        validateVariants(product.variants().stream()
                .map(variant -> new VariantKey(variant.sizeId(), variant.colorId(), variant.sku()))
                .toList());
        try {
            return productRepository.insert(product);
        } catch (DataIntegrityViolationException exception) {
            throw new ConflictException("Alguno de los SKU ya está registrado", exception);
        }
    }

    @Transactional
    public ProductView update(Long id, UpdateProductRequest request) {
        if (!productRepository.exists(id)) {
            throw new NotFoundException("Producto no encontrado");
        }
        List<ProductUpdate.Variant> variants = request.variants().stream()
                .map(variant -> new ProductUpdate.Variant(variant.id(), variant.sizeId(), variant.colorId(),
                        variant.sku().trim(), variant.stock(), variant.isActive()))
                .toList();
        ProductUpdate product = new ProductUpdate(request.name().trim(), request.description(), request.basePrice(),
                request.categoryId(), request.productTypeId(), request.isCustomizable(), request.imageUrl().trim(),
                request.isActive(), variants);

        validateClassification(product.categoryId(), product.productTypeId(), product.customizable());
        validateVariants(product.variants().stream()
                .map(variant -> new VariantKey(variant.sizeId(), variant.colorId(), variant.sku()))
                .toList());
        Set<Long> ownVariants = new HashSet<>(productRepository.findVariantIds(id));
        for (ProductUpdate.Variant variant : product.variants()) {
            if (variant.id() != null && !ownVariants.contains(variant.id())) {
                throw new BusinessRuleException("La variante " + variant.id() + " no pertenece a este producto");
            }
        }
        try {
            productRepository.update(id, product);
        } catch (DataIntegrityViolationException exception) {
            throw new ConflictException("Ya existe una variante con ese SKU o con esa talla y color", exception);
        }
        return product(id);
    }

    @Transactional
    public void changeStatus(Long id, boolean active) {
        if (productRepository.setActive(id, active) == 0) {
            throw new NotFoundException("Producto no encontrado");
        }
    }

    private void validateClassification(Long categoryId, Long productTypeId, boolean customizable) {
        if (!optionRepository.isActiveCategory(categoryId)) {
            throw new BusinessRuleException("Selecciona una categoría activa");
        }
        if (productTypeId != null && !optionRepository.isActiveProductType(productTypeId)) {
            throw new BusinessRuleException("Selecciona un tipo de producto válido");
        }
        if (customizable && productTypeId == null) {
            throw new BusinessRuleException("Un producto personalizable necesita un tipo de producto");
        }
    }

    private void validateVariants(List<VariantKey> variants) {
        Set<String> combinations = new HashSet<>();
        Set<String> skus = new HashSet<>();
        for (VariantKey variant : variants) {
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
    }

    private record VariantKey(Long sizeId, Long colorId, String sku) {
    }
}
