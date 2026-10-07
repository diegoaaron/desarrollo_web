package com.coralshop.catalog.service;

import com.coralshop.catalog.dto.CategoryView;
import com.coralshop.catalog.dto.OptionView;
import com.coralshop.catalog.dto.ProductTypeView;
import com.coralshop.catalog.dto.ProductView;
import com.coralshop.catalog.model.ProductFilter;
import com.coralshop.catalog.repository.CatalogOptionRepository;
import com.coralshop.catalog.repository.ProductRepository;
import com.coralshop.common.dto.PageRequest;
import com.coralshop.common.dto.PageResponse;
import com.coralshop.common.exception.NotFoundException;
import java.util.List;
import java.util.Locale;
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

    public PageResponse<ProductView> activeProducts(String type, Long categoryId, String text, PageRequest page) {
        ProductFilter filter = new ProductFilter(
                type == null || type.isBlank() ? null : type.trim().toUpperCase(Locale.ROOT),
                categoryId,
                text == null || text.isBlank() ? null : text.trim());
        List<ProductView> items = productRepository.findActive(filter, page.size(), page.offset());
        return PageResponse.of(items, page.page(), page.size(), productRepository.countActive(filter));
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

    public List<ProductTypeView> activeProductTypes() {
        return optionRepository.findActiveProductTypes();
    }
}
