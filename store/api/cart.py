from ninja import Router
from django.shortcuts import get_object_or_404
from hoomy.utils.schemas import MessageOut
from store.models import Cart, Item
from typing import List
from django.contrib.auth import get_user_model
from store.schemas import ItemOut, ItemCreate
from hoomy.utils.decorators import check_pk


User = get_user_model()

cart_router = Router(tags=['cart'])


@cart_router.get('cart/', response={
    200: List[ItemOut],
    404: MessageOut,
    401: MessageOut
})
@check_pk
def view_cart(request):
    cart_items = Item.objects.filter(user=User.objects.get(id=request.auth['pk']), is_ordered=False)

    if cart_items:
        return cart_items

    return 404, {'detail': 'Your cart is empty, go shop like crazy!'}


@cart_router.post('add-to-cart/', response={
    200: MessageOut,
    400: MessageOut,
    401: MessageOut
})
@check_pk
def add_update_cart(request, item_in: ItemCreate):
    try:
        item = Item.objects.get(product_id=item_in.product_id, user=User.objects.get(id=request.auth['pk']),
                                is_ordered=False)
        return 400, {'detail': 'Item is already in cart.'}
    except Item.DoesNotExist:
        if item_in.quantity < 1:
            return 400, {'detail': 'Quantity Value Must be Greater Than Zero'}
        item = Item.objects.create(**item_in.dict(), user=User.objects.get(id=request.auth['pk']))
    return 200, {'detail': 'Added to cart successfully'}


@cart_router.post('item/{id}/reduce-quantity', response={
    200: MessageOut,
    400: MessageOut,
    401: MessageOut
})
@check_pk
def reduce_item_quantity(request, id: int):
    item = get_object_or_404(Item, id=id, user=User.objects.get(id=request.auth['pk']), is_ordered=False)
    if item.quantity <= 1:
        item.quantity = 1
        return 400, {'detail': 'Item quantity cannot be less than 1!'}
    item.quantity -= 1
    item.save()

    return 200, {'detail': 'Item quantity reduced successfully!'}


@cart_router.post('item/{id}/increase-quantity', response={
    200: MessageOut,
    401: MessageOut
})
@check_pk
def increase_item_quantity(request, id: int):
    item = get_object_or_404(Item, id=id, user=User.objects.get(id=request.auth['pk']), is_ordered=False)
    item.quantity += 1
    item.save()
    return 200, {'detail': 'Item quantity increased successfully!'}


@cart_router.delete('item/{id}', response={
    204: MessageOut,
    401: MessageOut
})
@check_pk
def delete_item(request, id: int):
    item = get_object_or_404(Item, id=id, user=User.objects.get(id=request.auth['pk']), is_ordered=False)
    item.delete()
    return 204, {'detail': 'Item deleted!'}


@cart_router.post('create', response={
    200: MessageOut,
    404: MessageOut,
    401: MessageOut
})
@check_pk
def create_update_order(request):
    user = User.objects.prefetch_related('items', 'carts').get(id=request.auth['pk'])
    user_items = user.items.filter(is_ordered=False)
    if not user_items:
        return 404, {'detail': 'No Items Found To added to Order'}

    try:
        cart = user.carts.prefetch_related('items').get(is_ordered=False)
        list_of_product_id_in_order = [item['product_id'] for item in cart.items.values('product_id')]
        list_of_difference_items = []
        list_of_intersection_items = [
            (item, item.quantity) if item.product_id in list_of_product_id_in_order else list_of_difference_items.append(
                item.id) for item in user_items]
        Item.objects.filter(id__in=list_of_difference_items).update(is_ordered=True)

        for item, qty in list(filter(None, list_of_intersection_items)):
            item_duplicated = cart.items.get(product_id=item.product_id)
            item_duplicated.quantity = item_duplicated.quantity + qty
            item_duplicated.save()
            item.delete()

        cart.items.add(*list_of_difference_items)
        cart.total = cart.cart_total
        cart.save()
        return 200, {'detail': 'order updated successfully!'}
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user, is_ordered=False)
        cart.items.set(user_items)
        cart.total = cart.cart_total
        user_items.update(is_ordered=True)
        cart.save()
        return 200, {'detail': 'Order Created Successfully!'}


@cart_router.post('checkout', response={
    200: MessageOut,
    404: MessageOut,
    400: MessageOut,
    401: MessageOut
})
@check_pk
def checkout_order(request):
    try:
        cart = Cart.objects.get(user=User.objects.get(id=request.auth['pk']),
                                is_ordered=False)
    except Cart.DoesNotExist:
        return 404, {'detail': 'Order Doesn\'t Found'}
    cart.is_ordered = True
    cart.save()
    return 200, {'detail': 'checkout successfully!'}
