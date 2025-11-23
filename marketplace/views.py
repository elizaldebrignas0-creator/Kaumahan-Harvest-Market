from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .decorators import buyer_required, seller_required, staff_required
from .forms import (
    CartAddForm,
    LoginForm,
    OrderStatusForm,
    ProductForm,
    RatingReviewForm,
    RegistrationForm,
)
from .models import CartItem, Order, OrderItem, Product, RatingReview


CustomUser = get_user_model()


def redirect_authenticated_user(user):
    if user.is_staff or user.is_superuser:
        return "admin_dashboard"
    if getattr(user, "is_seller", False):
        return "seller_dashboard"
    return "buyer_dashboard"


def register_view(request):
    if request.user.is_authenticated:
        return redirect(redirect_authenticated_user(request.user))

    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if user.is_buyer:
                messages.success(request, "Your account was successfully created.")
            elif user.is_seller:
                messages.success(
                    request, "Your seller account is pending admin approval."
                )
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "auth/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect(redirect_authenticated_user(request.user))

    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect(redirect_authenticated_user(user))
    else:
        form = LoginForm()
    return render(request, "auth/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")


@login_required
def dashboard_redirect(request):
    return redirect(redirect_authenticated_user(request.user))


@buyer_required
def buyer_dashboard(request):
    query = request.GET.get("q")
    products = Product.objects.filter(is_active=True)
    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__icontains=query)
        )

    sellers = CustomUser.objects.filter(
        user_type="seller",
        is_approved=True,
    ).exclude(latitude__isnull=True).exclude(longitude__isnull=True)

    cart_items = CartItem.objects.filter(buyer=request.user)
    cart_total = sum(item.total_price for item in cart_items)

    return render(
        request,
        "dashboard/buyer_dashboard.html",
        {
            "products": products,
            "sellers": sellers,
            "cart_items": cart_items,
            "cart_total": cart_total,
            "cart_add_form": CartAddForm(),
        },
    )


@seller_required
def seller_dashboard(request):
    products = Product.objects.filter(seller=request.user)
    orders = Order.objects.filter(seller=request.user).order_by("-created_at")[:10]
    reviews = RatingReview.objects.filter(product__seller=request.user)[:10]
    return render(
        request,
        "dashboard/seller_dashboard.html",
        {
            "products": products,
            "orders": orders,
            "reviews": reviews,
        },
    )


@staff_required
def admin_dashboard(request):
    buyers = CustomUser.objects.filter(user_type="buyer")
    sellers = CustomUser.objects.filter(user_type="seller")
    pending_sellers = sellers.filter(is_approved=False)
    products = Product.objects.all()
    orders = Order.objects.all()

    return render(
        request,
        "dashboard/admin_dashboard.html",
        {
            "buyers": buyers,
            "sellers": sellers,
            "pending_sellers": pending_sellers,
            "products": products,
            "orders": orders,
        },
    )


@buyer_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart_item, created = CartItem.objects.get_or_create(
        buyer=request.user, product=product
    )
    form = CartAddForm(request.POST or None, instance=cart_item)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Product added to cart.")
    return redirect("buyer_dashboard")


@buyer_required
def cart_view(request):
    cart_items = CartItem.objects.filter(buyer=request.user)
    cart_total = sum(item.total_price for item in cart_items)
    return render(
        request,
        "orders/cart.html",
        {"cart_items": cart_items, "cart_total": cart_total},
    )


@buyer_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, buyer=request.user)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect("cart")


@require_POST
@login_required
@buyer_required
def checkout_direct(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id, is_active=True)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity < 1:
            messages.error(request, "Invalid quantity.")
            return redirect("product_detail", pk=product_id)
        
        # Get seller from product or use a default admin user
        seller = product.seller
        if not seller:
            seller = get_user_model().objects.filter(is_staff=True).first()
            if not seller:
                messages.error(request, "No seller found for this product.")
                return redirect("product_detail", pk=product_id)
        
        # Create a new order
        order = Order.objects.create(
            buyer=request.user,
            seller=seller,
            shipping_address=getattr(request.user, 'address', 'Please update your address in profile'),
            payment_method="cod",
            total_amount=product.price * quantity,
            status="pending"
        )
        
        # Create order item
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )
        
        messages.success(request, "Your order has been created. Please complete the checkout process.")
        return redirect("checkout_order", order_id=order.id)
        
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("product_detail", pk=product_id)


@login_required
@buyer_required
def checkout_view(request, order_id=None):
    order = None
    cart_items = []
    cart_total = 0
    
    if order_id:
        # Handle direct order checkout
        order = get_object_or_404(Order, id=order_id, buyer=request.user)
        if request.method == 'POST':
            shipping_address = request.POST.get('shipping_address')
            if not shipping_address:
                messages.error(request, 'Please provide a shipping address')
                return redirect('checkout_order', order_id=order_id)
            
            order.shipping_address = shipping_address
            order.save()
            messages.success(request, 'Your order has been placed successfully!')
            return redirect('buyer_orders')
    else:
        # Handle cart checkout
        cart_items = CartItem.objects.filter(buyer=request.user)
        cart_total = sum(item.total_price for item in cart_items)
        
        if request.method == 'POST':
            shipping_address = request.POST.get('shipping_address')
            payment_method = request.POST.get('payment_method', 'cod')
            
            if not shipping_address:
                messages.error(request, 'Please provide a shipping address')
                return redirect('checkout')
            
            # Create order
            order = Order.objects.create(
                buyer=request.user,
                shipping_address=shipping_address,
                payment_method=payment_method,
                total_amount=cart_total,
                status='pending'
            )
            
            # Create order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            
            # Clear cart
            cart_items.delete()
            
            messages.success(request, 'Your order has been placed successfully!')
            return redirect('buyer_orders')
    
    context = {
        'order': order,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'order_id': order_id
    }
    return render(request, 'checkout/checkout.html', context)
    cart_total = sum(item.total_price for item in cart_items)
    return render(
        request,
        "orders/checkout.html",
        {"cart_items": cart_items, "cart_total": cart_total},
    )


@buyer_required
def buyer_orders(request):
    orders = Order.objects.filter(buyer=request.user).order_by("-created_at")
    return render(request, "orders/order_history.html", {"orders": orders})


@seller_required
def seller_orders(request):
    orders = Order.objects.filter(seller=request.user).order_by("-created_at")
    if request.method == "POST":
        order = get_object_or_404(orders, pk=request.POST.get("order_id"))
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order status updated.")
            return redirect("seller_orders")
    return render(
        request,
        "orders/seller_orders.html",
        {"orders": orders, "status_form": OrderStatusForm()},
    )


@seller_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, "Product created successfully.")
            return redirect("seller_dashboard")
    else:
        form = ProductForm()
    return render(request, "products/product_form.html", {"form": form})


@seller_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect("seller_dashboard")
    else:
        form = ProductForm(instance=product)
    return render(request, "products/product_form.html", {"form": form})


@seller_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted.")
        return redirect("seller_dashboard")
    return render(request, "products/product_confirm_delete.html", {"product": product})


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    reviews = product.reviews.filter(is_approved=True)
    form = None
    if request.user.is_authenticated and getattr(request.user, "is_buyer", False):
        try:
            existing = RatingReview.objects.get(product=product, buyer=request.user)
            form = RatingReviewForm(instance=existing)
        except RatingReview.DoesNotExist:
            form = RatingReviewForm()

        if request.method == "POST":
            form = RatingReviewForm(request.POST, instance=existing if "existing" in locals() else None)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.buyer = request.user
                review.save()
                messages.success(request, "Thank you for your review.")
                return redirect("product_detail", pk=product.pk)

    return render(
        request,
        "products/product_detail.html",
        {"product": product, "reviews": reviews, "form": form},
    )


@require_POST
@login_required
def rate_product(request):
    """Handle AJAX request to save a product rating"""
    form = RatingReviewForm(request.POST)
    if form.is_valid():
        product_id = form.cleaned_data['product_id']
        rating = form.cleaned_data['rating']
        
        # Get or create the rating
        rating_obj, created = RatingReview.objects.update_or_create(
            user=request.user,
            product_id=product_id,
            defaults={'rating': rating}
        )
        
        # Calculate new average rating
        product = get_object_or_404(Product, id=product_id)
        avg_rating = product.reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        
        return JsonResponse({
            'status': 'success',
            'avg_rating': round(avg_rating, 1),
            'rating_count': product.reviews.count()
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid form data'}, status=400)


@staff_required
def approve_seller(request, user_id):
    seller = get_object_or_404(CustomUser, pk=user_id, user_type="seller")
    seller.is_approved = True
    seller.save()
    messages.success(request, f"Seller {seller.full_name} approved.")
    return redirect("admin_dashboard")


@staff_required
def reject_seller(request, user_id):
    seller = get_object_or_404(CustomUser, pk=user_id, user_type="seller")
    seller.is_active = False
    seller.is_approved = False
    seller.save()
    messages.success(request, f"Seller {seller.full_name} rejected.")
    return redirect("admin_dashboard")


def serve_media(request, path):
    """
    Serve media files in production (for platforms like Render)
    This is a workaround for production deployments where static file serving is limited
    """
    import os
    from django.conf import settings
    from django.http import HttpResponse, Http404
    from mimetypes import guess_type
    
    # Security check - prevent directory traversal
    if '..' in path or path.startswith('/'):
        raise Http404("File not found")
    
    # Construct the full file path
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    # Normalize path for cross-platform compatibility
    file_path = os.path.normpath(file_path)
    
    # Check if file exists and is within media root
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise Http404("File not found")
    
    # Additional security check
    if not os.path.abspath(file_path).startswith(os.path.abspath(settings.MEDIA_ROOT)):
        raise Http404("File not found")
    
    # Guess MIME type
    mime_type, encoding = guess_type(file_path)
    mime_type = mime_type or 'application/octet-stream'
    
    # Serve the file
    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=mime_type)
            
            # Set proper headers for caching and display
            response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
            response['Cache-Control'] = 'public, max-age=3600'  # Cache for 1 hour
            
            # Add CORS headers if needed
            response['Access-Control-Allow-Origin'] = '*'
            
            return response
    except Exception:
        raise Http404("File not found")
