from ninja import Router
from ninja.security import django_auth
from django.shortcuts import get_object_or_404
from store.models import Cart
from store.schemas import CartIn, CartOut, CartSchema
from store.schemas import AccountOut, FourOFourOut
from typing import List
from django.db.models import Sum, Avg
from rest_framework import status
from django.contrib.auth import get_user_model


User = get_user_model()

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

@cart_router.post('/to_cart', response={201: CartSchema})
def create_cart(request, data: CartSchema):
    # cart = Cart.objects.create(user_id=request.user.id)
    cart = Cart.objects.set(**data.dict())
    # for attribute, value in data.dict().items():
    #     setattr(cart, attribute, value)
    # cart.save()
    return cart


@cart_router.put('/update_cart/{cart_id}', response={200: CartSchema, 404: FourOFourOut})
def update_cart(request, cart_id: int, data: CartSchema):
    try:
        cart = Cart.objects.get(pk=cart_id)
        for attribute, value in data.dict().items():
            setattr(cart, attribute, value)
        cart.save()
        return 200, cart
    except Cart.DoesNotExist as e:
        return 404, {"message": "Cart does not exist"}
