from ninja import Router
from ninja.security import django_auth
from django.shortcuts import get_object_or_404
from store.models import Account, Color
from store.schemas import ColorSchema
from typing import List
from django.db.models import Sum, Avg
from rest_framework import status


color_router = Router(tags=['color'])


@color_router.get("/get-all-colors", response=List[ColorSchema])
def get_all(request):
    colors = Color.objects.all()
    return 200, colors


