from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('category/', views.category, name='category'),
    path('category_products/<str:category>', views.category_products, name='category_products'),
    path('product/<int:product_id>/<str:product_category>/', views.fetch_product, name='fetch_product'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('view_wish_list/', views.view_wish_list, name='view_wish_list'),
    path('remove_from_cart/<int:product_id>', views.remove_from_cart, name='remove_from_cart'),
    path('remove_wish_list/<int:product_id>/', views.remove_wish_list, name='remove_wish_list'),
    path('search/', views.item_search, name='search'),
    path('cart_search/', views.cart_item_search, name='cart_search'),
    path('wish_list_search/', views.wish_list_item_search, name='wish_list_item_search'),
    path('category_search/', views.category_search, name='category_search'),
    path('category_products_search/<str:category_name>', views.category_products_search,
         name='category_products_search'),
    path('checkout/', views.checkout_page, name='checkout'),
    path('order_update/', views.add_to_order, name='order_update'),
    path('orders_view/', views.order_view, name='order_view'),
]
