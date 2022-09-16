from ninja import Router
from store.models import Account
from store.schemas import AccountOut, FourOFourOut


account_router = Router(tags=['account'])


@account_router.get('/get_account/{account_id}/', response={
    200: AccountOut,
    404: FourOFourOut,
})
def get_account(request, account_id: int):
    try:
        account = Account.objects.get(id=account_id)
        return account
    except Account.DoesNotExist:
        return 404, {'detail': f'Account with id {account_id} does not exist'}
