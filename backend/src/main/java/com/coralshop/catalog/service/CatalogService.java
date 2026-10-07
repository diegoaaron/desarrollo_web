package com.coralshop.catalog.service;

import com.coralshop.catalog.dto.CategoryView;
import com.coralshop.catalog.dto.OptionView;
import com.coralshop.catalog.dto.ProductView;
import com.coralshop.catalog.repository.CatalogOptionRepository;
import com.coralshop.catalog.repository.ProductRepository;
import com.coralshop.common.exception.NotFoundException;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/** Consultas del catálogo público: solo productos y categorías activos. */
@Service
@Transactional(readOnly = true)
public class CatalogService {

    private final ProductRepository productRepository;
    private final CatalogOptionRepository optionRepository;

    public CatalogService(ProductRepository productRepository, CatalogOptionRepository optionRepository) {
        this.productRepository = productRepository;
        this.optionRepository = optionRepository;
    }

    public List<ProductView> activeProducts() {
        return productRepository.findActive();
    }

    public ProductView productDetail(Long id) {
        ProductView product = productRepository.findActiveById(id)
                .orElseThrow(() -> new NotFoundException("Producto no encontrado"));
        return product.withVariants(productRepository.findActiveVariants(id));
    }

    public List<CategoryView> activeCategories() {
        return optionRepository.findActiveCategories();
    }

    public List<OptionView> activeBrands() {
        return optionRepository.findActiveBrands();
    }
}
