from ninja import Schema
from typing import List
from .models import Color


class FourOFourOut(Schema):
    detail: str


class AccountOut(Schema):
    id: int
    profile_pic: str = None


class CategorySchema(Schema):
    title: str


class ColorSchema(Schema):
    color_code: str


class ProductImageSchema(Schema):
    images: str


class ProductSchema(Schema):
    id: int
    title: str
    banner: str
    description: str = None
    category: CategorySchema
    colors: List[ColorSchema]
    price: int
    is_available: bool = True
    show_hide: bool = True
    is_featured: bool = False
    product_image: List[ProductImageSchema]


# class ProductImageSchema(Schema):
#     post: ProductSchema
#     images: List[str]


class ItemSchema(Schema):
    product: ProductSchema
    quantity: int


class Cart(Schema):
    id: int
    item: List[ItemSchema]
    is_ordered: bool = False


# There must be CartIn and CartOut
class CartIn(Schema):
    id: int
    item: List[ItemSchema]
    is_ordered: bool = False


class CartOut(Schema):
    id: int
    item: List[ItemSchema]
    is_ordered: bool = False

