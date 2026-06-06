from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

from .models import Product, Cart, Order, Profile, Wishlist, Review
from .forms import ProfileForm, RegisterForm

import razorpay
# ================= HOME =================
def home(request):
    search = request.GET.get('search')
    category = request.GET.get('category')

    products = Product.objects.all()

    if search:
        products = products.filter(name__icontains=search)

    if category:
        products = products.filter(category=category)

    return render(request, 'home.html', {'products': products})


# ================= REGISTER =================
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {
        'form': form
    })

# ================= PROFILE =================
@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    return render(request, 'profile.html', {
        'profile': profile
    })


# ================= EDIT PROFILE =================
@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        city = request.POST.get('city')
        area = request.POST.get('area')
        house = request.POST.get('house')
        landmark = request.POST.get('landmark')

        full_address = f"""
House/Flat No: {house}
Area: {area}
Landmark: {landmark}
City: {city}
"""

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            profile = form.save(commit=False)
            profile.address = full_address
            profile.save()
            return redirect('profile')

    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {
        'form': form,
        'profile': profile
    })


# ================= DASHBOARD =================
@login_required
def dashboard(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    cart_items = Cart.objects.filter(user=request.user)

    return render(request, 'dashboard.html', {
        'profile': profile,
        'orders': orders,
        'cart_items': cart_items
    })


# ================= CART =================
@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# ================= ADD TO CART =================
@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    if product.stock <= 0:
        return redirect('product_detail', id=product.id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()

    return redirect('cart')


# ================= REMOVE FROM CART =================
@login_required
def remove_from_cart(request, id):
    item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    item.delete()
    return redirect('cart')


# ================= INCREASE =================
@login_required
def increase_quantity(request, id):
    item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    if item.quantity < item.product.stock:
        item.quantity += 1
        item.save()

    return redirect('cart')


# ================= DECREASE =================
@login_required
def decrease_quantity(request, id):
    item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')


# ================= CHECKOUT =================
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


# ================= PAYMENT =================
@login_required
def payment(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    amount = int(total * 100)

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        'payment': payment,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'amount': total,
        'total': total,
        'cart_items': cart_items
    }

    return render(request, 'payment.html', context)


# ================= PLACE ORDER =================
@login_required
def place_order(request):

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('cart')

    last_order = Order.objects.filter(
        user=request.user
    ).order_by('-order_number').first()

    next_number = (
        last_order.order_number + 1
        if last_order and last_order.order_number
        else 1
    )

    total_items = 0

    for item in cart_items:

        if item.product.stock < item.quantity:
            return redirect('cart')

        Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity,
            status="Pending",
            address=request.user.profile.address
            if hasattr(request.user, "profile")
            else "",
            order_number=next_number
        )

        item.product.stock -= item.quantity
        item.product.save()

        total_items += item.quantity
        next_number += 1

    try:

        if request.user.email:

            send_mail(
                subject="EasyBuy - Order Confirmation",
                message=(
                    f"Dear {request.user.username},\n\n"
                    f"Thank you for shopping with EasyBuy.\n\n"
                    f"Your order has been placed successfully.\n\n"
                    f"Total Items: {total_items}\n"
                    f"Order Status: Pending\n\n"
                    f"We will notify you once the order is shipped.\n\n"
                    f"Regards,\n"
                    f"EasyBuy Team"
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[request.user.email],
                fail_silently=False,
            )

    except Exception as e:
        print("EMAIL ERROR:", e)

    cart_items.delete()

    return redirect('success')
# ================= MY ORDERS =================
@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'orders.html', {
        'orders': orders
    })


# ================= SUCCESS =================
@login_required
def success(request):
    return render(request, 'success.html')


# ================= PRODUCT DETAIL =================
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    reviews = Review.objects.filter(
        product=product
    ).order_by('-created_at')

    if reviews.exists():
        average_rating = round(
            sum(review.rating for review in reviews) / reviews.count(),
            1
        )
    else:
        average_rating = 0

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
        'related_products': related_products
    })


# ================= CANCEL ORDER =================
@login_required
def cancel_order(request, id):
    order = get_object_or_404(
        Order,
        id=id,
        user=request.user
    )

    order.status = "Cancelled"
    order.save()

    return redirect('my_orders')


# ================= INVOICE =================
@login_required
def invoice(request, id):
    order = get_object_or_404(
        Order,
        id=id,
        user=request.user
    )

    return render(request, 'invoice.html',{
    'order': order
})
    


# ================= WISHLIST =================
@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'wishlist.html', {
        'wishlist_items': wishlist_items
    })


# ================= ADD TO WISHLIST =================
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    already_exists = Wishlist.objects.filter(
        user=request.user,
        product=product
    ).exists()

    if not already_exists:
        Wishlist.objects.create(
            user=request.user,
            product=product
        )

    return redirect('wishlist')


# ================= REMOVE FROM WISHLIST =================
@login_required
def remove_from_wishlist(request, wishlist_id):
    item = get_object_or_404(
        Wishlist,
        id=wishlist_id,
        user=request.user
    )

    item.delete()
    return redirect('wishlist')


# ================= ADD REVIEW =================
@login_required
def add_review(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id
    )

    already_reviewed = Review.objects.filter(
        user=request.user,
        product=product
    ).exists()

    if request.method == "POST" and not already_reviewed:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            user=request.user,
            product=product,
            rating=rating,
            comment=comment
        )

    return redirect('product_detail', id=product.id)