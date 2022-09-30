from ninja import Router
from hoomy.utils.schemas import MessageOut
from store.models import Wishlist
from typing import List
from django.contrib.auth import get_user_model
from store.schemas import FavoriteProductIn, FavoriteProductOut
from hoomy.utils.decorators import check_pk


User = get_user_model()

wishlist_router = Router(tags=['wishlist'])


@wishlist_router.get('wishlist/', response={
    200: List[FavoriteProductOut],
    404: MessageOut,
    401: MessageOut
})
@check_pk
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=User.objects.get(id=request.auth['pk']))

    if wishlist_items:
        return wishlist_items

    return 404, {'detail': 'Your wishlist is empty, go browse our products!'}


@wishlist_router.post('add-to-wishlist/', response={
    200: MessageOut,
    204: MessageOut,
    400: MessageOut,
    401: MessageOut
})
@check_pk
def add_remove_favorite(request, fav_in: FavoriteProductIn):
    try:
        fav_prod = Wishlist.objects.get(product_id=fav_in.product_id, user=User.objects.get(id=request.auth['pk']),
                                        is_fav=True)

        if fav_in.product_id == fav_prod.product_id:
            fav_prod.is_fav = False
            fav_prod.delete()
        return 204, {'detail': 'Removed product from wishlist.'}
    except Wishlist.DoesNotExist:
        fav_prod = Wishlist.objects.create(**fav_in.dict(), user=User.objects.get(id=request.auth['pk']))
        fav_prod.is_fav = True
        fav_prod.save()
    return 200, {'detail': 'Added to wishlist successfully'}



