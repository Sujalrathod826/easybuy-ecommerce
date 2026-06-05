from django.contrib import admin
from .models import Product, Cart, Order, Profile, Wishlist, Review
from django.utils import timezone


# ================= PRODUCT =================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'category',
        'price',
        'stock',
         'image',
        'image2',
        'image3'
    )

    list_filter = (
        'category',
    )

    search_fields = (
        'name',
    )


# ================= CART =================
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'product',
        'quantity',
    )


# ================= ORDER =================
# ================= ORDER =================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'order_number',
        'user',
        'product',
        'quantity',
        'status',
        'payment_method',
        'created_at',
        'delivered_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'user__username',
        'product__name',
    )

    list_editable = (
        'status',
    )

    def save_model(self, request, obj, form, change):

        if obj.status == "Delivered" and not obj.delivered_at:
            obj.delivered_at = timezone.now()

        super().save_model(request, obj, form, change)    


# ================= PROFILE =================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'phone',
    )


# ================= WISHLIST =================
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'product',
        'created_at',
    )


# ================= REVIEW =================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'product',
        'rating',
        'created_at',
    )

    list_filter = (
        'rating',
        'created_at',
    )

    search_fields = (
        'user__username',
        'product__name',
    )