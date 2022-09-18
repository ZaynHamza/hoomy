from ninja import Router
from store.models import Product, ProductImage
from store.schemas import ProductSchema, ProductImageSchema
from typing import List


product_router = Router(tags=['product'])


@product_router.get("/get-all-products", response=List[ProductSchema])
def get_all(request):
    # products = ProductImage.objects.all()
    # products = list(ProductImage.objects.get().related_name.values_list('product', flat=True))
    products = Product.objects.all()
    return 200, products



