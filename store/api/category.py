from ninja import Router
from store.models import Category
from store.schemas import CategorySchema
from typing import List


category_router = Router(tags=['category'])


@category_router.get("/get-all-categories", response=List[CategorySchema])
def get_all(request):
    categories = Category.objects.all()
    return 200, categories


