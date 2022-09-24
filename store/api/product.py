from ninja import Router
from store.models import Product
from store.schemas import ProductSchema, FourOFourOut
from typing import List


product_router = Router(tags=['product'])


@product_router.get("/get-all-products", response={200: List[ProductSchema], 404: FourOFourOut})
def get_all(request):
    products = Product.objects.filter(show_hide=True)

    if not products:
        return 404, {'detail': 'No products found'}

    return 200, products



