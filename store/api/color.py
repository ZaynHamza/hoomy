from ninja import Router
from ninja.security import django_auth
from django.shortcuts import get_object_or_404
from store.models import Color
from store.schemas import ColorSchema, ColorIn
from typing import List
from django.db.models import Sum, Avg
from rest_framework import status


color_router = Router(tags=['color'])


@color_router.get("/get-all-colors", response=List[ColorSchema])
def get_all(request):
    colors = Color.objects.all()
    return 200, colors


@color_router.post('add_color/')
def add_color(request, color_in: ColorIn):
    return ColorIn
