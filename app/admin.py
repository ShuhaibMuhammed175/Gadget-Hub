from django.contrib import admin
from .models import Category, Product, Cart, Wishlist, Order, OrderDetail, Review


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'desc')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Review)
