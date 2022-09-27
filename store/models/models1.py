import uuid

from PIL import Image
from django.db import models
from hoomy.utils.models import Entity
from django.contrib.auth import get_user_model


"""
=================================
Account 
    - user*
    - profile pic*
=================================
Product
    - title
    - banner
    - images
    - description
    - category (fk)
    - colors (fk)
    - price
    - is available (bool) (if false, puts out of stock label)
    - show/hide (bool) 
    - is featured (bool)
=================================
Category
    - name
=================================
Color
    - name
    - color code (hex)
=================================
Cart
    - product (fk)
    - user (fk)
    - is ordered boolean
=================================
"""


User = get_user_model()


# class Account(models.Model):
#     user = models.OneToOneField(to=User, on_delete=models.CASCADE)
#     profile_pic = models.ImageField(upload_to="profile_pics/", blank=True)


class Category(models.Model):
    title = models.CharField(max_length=25)

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=50)
    color_code = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=50)
    banner = models.ImageField(upload_to="banners/")
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    colors = models.ManyToManyField('store.Color', verbose_name='colors', related_name='products')
    price = models.IntegerField()
    is_available = models.BooleanField(default=True)
    show_hide = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, related_name='product_image')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.product.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Item(models.Model):
    user = models.ForeignKey(to=User, verbose_name='user', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField('is ordered', default=False)

    def __str__(self):
        # return self.product.title
        return f''


class Cart(models.Model):
    user = models.ForeignKey(to=User, verbose_name='user', related_name='carts', on_delete=models.CASCADE)
    items = models.ManyToManyField('store.Item', verbose_name='items', related_name='carts')
    is_ordered = models.BooleanField('is ordered', default=False)
    # newly added / 26-9-2022
    total = models.IntegerField('total', blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} + {self.total}"

    @property
    def cart_total(self):
        return sum(i.product.price * i.quantity for i in self.items.all())


# class Wishlist(models.Model):
#     user = models.ForeignKey(to=User, verbose_name='user', related_name='favs', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, )