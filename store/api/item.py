from ninja import Router
from ninja.security import django_auth
from django.shortcuts import get_object_or_404
from store.models import Item, Account
from store.schemas import AccountOut, FourOFourOut, ItemSchema
from typing import List
from django.db.models import Sum, Avg
from rest_framework import status


item_router = Router(tags=['item'])


@item_router.get("/get-all-items", response=List[ItemSchema])
def get_all(request):
    items = Item.objects.all()

    return 200, items
