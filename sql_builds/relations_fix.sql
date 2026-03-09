ALTER TABLE public.products
ADD COLUMN supplier_id INTEGER;

ALTER TABLE public.products
ADD CONSTRAINT fk_products_suppliers
FOREIGN KEY (supplier_id)
REFERENCES public.suppliers (id);

