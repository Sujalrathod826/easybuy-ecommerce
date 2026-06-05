from django.db import models
from django.contrib.auth.models import User


# --------------------
# PRODUCT MODEL
# --------------------
class Product(models.Model):

    CATEGORY_CHOICES = (

        ('Fashion', 'Fashion'),

        ('Mobiles', 'Mobiles'),

        ('Electronics', 'Electronics'),

        ('Beauty', 'Beauty'),

        ('Appliances', 'Appliances'),

    )

    name = models.CharField(max_length=100)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    # MAIN IMAGE

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    # EXTRA PRODUCT IMAGES

    image2 = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    image3 = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    image4 = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    # CATEGORY

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default='Fashion'
    )

    # STOCK

    stock = models.IntegerField(default=10)

    def __str__(self):
        return self.name


# --------------------
# CART MODEL
# --------------------
class Cart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(default=1)

    def __str__(self):

        return f"{self.user.username} - {self.product.name}"


# --------------------
# ORDER MODEL
# --------------------
class Order(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('Online Payment', 'Online Payment'),
        ('Cash on Delivery', 'Cash on Delivery'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(default=1)

    address = models.TextField()

    order_number = models.IntegerField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_CHOICES,
        default='Online Payment'
    )

    delivered_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"Order #{self.order_number} - {self.user.username}"
# --------------------
# PROFILE MODEL
# --------------------
class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    address = models.TextField(blank=True)

    profile_pic = models.ImageField(
        upload_to='profiles/',
        default='default.jpg'
    )

    def __str__(self):

        return self.user.username


# --------------------
# WISHLIST MODEL
# --------------------
class Wishlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.username} - {self.product.name}"


# --------------------
# REVIEW MODEL
# --------------------
class Review(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.username} - {self.product.name}"