from django.contrib.auth import get_user_model, authenticate
from ninja import Router

from store.schemas import FourOFourOut
from hoomy import status
from .authorization import create_token_for_user, AuthBearer
from .schemas import AccountIn, AuthOut, SigninIn


User = get_user_model()

auth_router = Router(tags=['auth'])


@auth_router.post('signup', response={
    201: AuthOut,
    400: FourOFourOut,
})
def signup(request, account_in: AccountIn):
    if account_in.password1 != account_in.password2:
        return status.BAD_REQUEST_400, {'detail': 'Passwords should look alike'}

    try:
        User.objects.get(email=account_in.email)
    except User.DoesNotExist:
        new_user = User.objects.create_user(
            first_name=account_in.first_name,
            last_name=account_in.last_name,
            email=account_in.email,
            password=account_in.password1,
            profile_pic=account_in.profile_pic
        )

        token = create_token_for_user(new_user)

        return status.CREATED_201, {
            'token': token,
            'account': new_user
        }

    return status.BAD_REQUEST_400, {'detail': 'Email is taken'}


@auth_router.post('signin', response={
    200: AuthOut,
    404: FourOFourOut
})
def signin(request, signin_in: SigninIn):
    try:
        user = User.objects.get(email=signin_in.email)
        # user = authenticate(email=signin_in.email, password=signin_in.password)

    except User.DoesNotExist:
        user = None

    else:
        if user.check_password(signin_in.password):
            token = create_token_for_user(user)

            return {
                'token': token,
                'account': user
            }

    if not user:
        return status.NOT_FOUND_404, {'detail': 'User is not registered'}

# from django.contrib.auth import get_user_model, authenticate
# from django.shortcuts import get_object_or_404
# from ninja import Router
#
#
# from .authorization import AuthBearer, create_token_for_user
# from .schemas import AccountIn, AuthOut, SigninIn, AccountOut
# from hoomy.utils.schemas import MessageOut
#
# from hoomy.utils.decorators import check_pk
#
# User = get_user_model()
#
# auth_router = Router(tags=['auth'])
#
#
# @auth_router.post('signup', response={
#     400: MessageOut,
#     201: AuthOut,
# })
# def signup(request, account_in: AccountIn):
#     if account_in.password1 != account_in.password2:
#         return 400, {'detail': 'Passwords do not match!'}
#
#     try:
#         User.objects.get(email=account_in.email)
#     except User.DoesNotExist:
#         new_user = User.objects.create_user(
#             first_name=account_in.first_name,
#             last_name=account_in.last_name,
#             email=account_in.email,
#             password=account_in.password1,
#             profile_pic=account_in.profile_pic
#         )
#
#         token = create_token_for_user(new_user)
#
#         return 201, {
#             'token': token,
#             'account': new_user,
#         }
#
#     return 400, {'detail': 'User already registered!'}
#
#
# @auth_router.post('signin', response={
#     200: AuthOut,
#     404: MessageOut,
# })
# def signin(request, signin_in: SigninIn):
#     user = authenticate(email=signin_in.email, password=signin_in.password)
#
#     if not user:
#         return 404, {'detail': 'User does not exist'}
#
#     token = create_token_for_user(user)
#
#     return {
#         'token': token,
#         'account': user
#     }
