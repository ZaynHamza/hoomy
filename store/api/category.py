from ninja import Router
from ninja.security import django_auth
from django.shortcuts import get_object_or_404
from store.models import Category
from store.schemas import CategorySchema
from typing import List
from django.db.models import Sum, Avg
from rest_framework import status


category_router = Router(tags=['category'])


@category_router.get("/get-all-categories", response=List[CategorySchema])
def get_all(request):
    categories = Category.objects.all()
    return 200, categories


