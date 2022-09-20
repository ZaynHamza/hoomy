from ninja import Router
from store.models import Product
from store.schemas import ProductSchema
from typing import List


product_router = Router(tags=['product'])


@product_router.get("/get-all-products", response=List[ProductSchema])
def get_all(request):
    products = Product.objects.all()
    return 200, products



