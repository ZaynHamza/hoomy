from ninja import Router
from ninja.security import django_auth
from django.shortcuts import get_object_or_404
from store.models import Cart
from store.schemas import CartIn, CartOut, CartSchema
from store.schemas import AccountOut, FourOFourOut
from typing import List
from django.db.models import Sum, Avg
from rest_framework import status


cart_router = Router(tags=['cart'])
# show cart
# checkout is ordered


# @cart_router.post('/get_cart/', response={
#     200: CartOut,
#     # 404: FourOFourOut,
# })
# def get_cart(request, cart_in: CartIn):
#     cart = Cart.objects.get(id=cart_in.id)
#     if not cart.is_ordered:
#         return cart
#     else:
#         cart = Cart.objects.create()
#         return cart

@cart_router.post('/to_cart')
def add_to_cart(request, cart: CartSchema):
    return cart

