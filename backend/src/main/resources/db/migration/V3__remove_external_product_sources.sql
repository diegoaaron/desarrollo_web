-- Los productos base se cargan y configuran solo desde el panel de administración:
-- se retiran las columnas de origen externo que agregó la V2.
DROP INDEX IF EXISTS products_cj_product_id_unique;
DROP INDEX IF EXISTS variants_cj_variant_id_unique;

ALTER TABLE products DROP COLUMN IF EXISTS cj_product_id;
ALTER TABLE product_variants DROP COLUMN IF EXISTS cj_variant_id;
