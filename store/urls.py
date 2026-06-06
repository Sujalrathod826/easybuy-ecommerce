from django.urls import path
from . import views
from django.contrib import admin
from .views import create_admin

urlpatterns = [
    path('create-admin/', views.create_admin),
    

    # HOME
    path('', views.home, name='home'),

    # CART
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:id>/', views.decrease_quantity, name='decrease_quantity'),

    # AUTH
    path('register/', views.register, name='register'),

    # PROFILE + DASHBOARD
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # ORDER FLOW
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('place-order/', views.place_order, name='place_order'),
    path('success/', views.success, name='success'),

    # ORDERS (ONLY ONE)
    path('my-orders/', views.my_orders, name='my_orders'),

    # PRODUCT DETAIL
    path('product/<int:id>/', views.product_detail, name='product_detail'),

    # ORDER ACTIONS
    path('cancel-order/<int:id>/', views.cancel_order, name='cancel_order'),
    path('invoice/<int:id>/', views.invoice, name='invoice'),
    path('payment/', views.payment, name='payment'),

    path(
    'wishlist/',
    views.wishlist,
    name='wishlist'
),

path(
    'add-to-wishlist/<int:product_id>/',
    views.add_to_wishlist,
    name='add_to_wishlist'
),

path(
    'remove-wishlist/<int:wishlist_id>/',
    views.remove_from_wishlist,
      name='remove_from_wishlist'
),
path(
    'add-review/<int:product_id>/',
    views.add_review,
    name='add_review'
),
]