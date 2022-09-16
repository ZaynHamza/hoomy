from django.contrib import admin
from .models import Product, ProductImage, Category, Color


admin.site.register(Color)
admin.site.register(Category)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    def get_colors(self, obj):
        return ", ".join([c.title for c in obj.color.all()])

    inlines = [ProductImageAdmin]
    list_display = ["title", "category", "price", "get_colors", "is_available", "show_hide", "is_featured"]
    list_editable = ["is_available", "show_hide", "is_featured"]


admin.site.register(Product, ProductAdmin)
