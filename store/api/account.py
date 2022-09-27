# from typing import List
# from ninja import Router
# from rest_framework import status
# from store.models import Account
# from store.schemas import AccountOut, FourOFourOut
#
#
# account_router = Router(tags=['account'])
#
#
# @account_router.get("/get_all", response=List[AccountOut])
# def get_all(request):
#     return status.HTTP_200_OK, Account.objects.order_by('user_id')
#
#
# @account_router.get('/get_one/{account_id}/', response={
#     200: AccountOut,
#     404: FourOFourOut,
# })
# def get_one(request, account_id: int):
#     try:
#         account = Account.objects.get(id=account_id)
#         return account
#     except Account.DoesNotExist:
#         return 404, {'detail': f'Account with id {account_id} does not exist'}
