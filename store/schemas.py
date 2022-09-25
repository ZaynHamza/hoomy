from ninja import Schema
from typing import List
from pydantic import UUID4


class FourOFourOut(Schema):
    detail: str


class UUIDSchema(Schema):
    id: UUID4


class AccountOut(Schema):
    id: int
    profile_pic: str = None


class CategorySchema(Schema):
    title: str


class ColorSchema(Schema):
    color_code: str


class ColorIn(Schema):
    title: str
    color_code: str


class ProductImageSchema(Schema):
    image: str


class ProductSchema(Schema):
    # id: int
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


class ItemSchema(Schema):
    product: ProductSchema
    quantity: int


# Newly added
class ItemCreate(Schema):
    product_id: UUID4
    item_qty: int


class ItemOut(UUIDSchema, ItemSchema):
    pass
# End


class CartSchema(Schema):
    item: List[ItemSchema]
    is_ordered: bool = False


# There must be CartIn and CartOut
class CartIn(Schema):
    item: List[ItemSchema]
    is_ordered: bool = False


class CartOut(Schema):
    id: int
    item: List[ItemSchema]
    is_ordered: bool = False

