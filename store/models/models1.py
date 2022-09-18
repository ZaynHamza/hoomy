from django.db import models
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


class Account(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True)


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


class ProductImage(models.Model):
    post = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, related_name='product_image')
    images = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.post.title


class Item(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    item = models.ManyToManyField('store.Item', verbose_name='items', related_name='carts')
    is_ordered = models.BooleanField(default=False)
