# from django.contrib.auth import get_user_model
# from ninja.security import HttpBearer
# from jose import jwt, JWTError
#
# from hoomy import settings
#
# User = get_user_model()
#
#
# # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InVzZXJAZXhhbXBsZS5jb20ifQ.X9-RqWLql-9n6NrkFVjXETHv2BRcVBaCXiQmXK3Nwws
#
# class AuthBearer(HttpBearer):
#     def authenticate(self, request, token):
#         try:
#             user_email = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms='HS256')
#         except JWTError:
#             return {'token': 'unauthorized'}
#
#         if user_email:
#             return {'email': str(user_email['email'])}
#
#
# def create_token_for_user(user):
#     token = jwt.encode({'email': str(user.email)}, key=settings.SECRET_KEY, algorithm='HS256')
#     return {
#         'access': str(token)
#     }


from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from jose import jwt, JWTError
from ninja.security import HttpBearer

User = get_user_model()

TIME_DELTA = timedelta(days=120)


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            user_pk = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        except JWTError:
            return {'token': 'unauthorized'}
        if user_pk:
            return {'pk': str(user_pk['pk'])}


def create_token_for_user(user):
    token = jwt.encode({'pk': str(user.pk)}, key=settings.SECRET_KEY, algorithm='HS256')
    return {
        'access': str(token),
    }


