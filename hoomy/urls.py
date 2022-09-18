"""hoomy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from restauth.api import auth_router
from store.api import account_router, category_router, product_router, cart_router, color_router
# from store.api.color import color_router

api = NinjaAPI(
    title='Hoomy Furniture Store',
    version='0.1',
    csrf=True,
)
api.add_router('account/', account_router)
api.add_router('category/', category_router)
api.add_router('product/', product_router)
api.add_router('cart/', cart_router)
# api.add_router('item/', item_router)
api.add_router('auth/', auth_router)
api.add_router('color/', color_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]
