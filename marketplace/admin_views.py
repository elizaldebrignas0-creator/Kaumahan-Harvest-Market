from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count, Sum, Avg
from django.utils.timezone import now, timedelta
from django.http import JsonResponse
from .models import Product, CustomUser, Order, RatingReview, CartItem


@staff_member_required
def admin_dashboard(request):
    """Enhanced admin dashboard with comprehensive statistics"""
    
    # Time periods
    today = now().date()
    this_month_start = today.replace(day=1)
    last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
    last_month_end = this_month_start - timedelta(days=1)
    
    # User Statistics
    total_users = CustomUser.objects.count()
    total_sellers = CustomUser.objects.filter(user_type='seller').count()
    total_buyers = CustomUser.objects.filter(user_type='buyer').count()
    approved_sellers = CustomUser.objects.filter(user_type='seller', is_approved=True).count()
    pending_sellers = CustomUser.objects.filter(user_type='seller', is_approved=False).count()
    
    # Product Statistics
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    inactive_products = Product.objects.filter(is_active=False).count()
    
    # Order Statistics
    total_orders = Order.objects.count()
    orders_this_month = Order.objects.filter(created_at__gte=this_month_start).count()
    orders_last_month = Order.objects.filter(created_at__gte=last_month_start, created_at__lt=last_month_end).count()
    
    # Revenue Statistics
    total_revenue = Order.objects.filter(status='DELIVERED').aggregate(total=Sum('total_amount'))['total'] or 0
    revenue_this_month = Order.objects.filter(
        status='DELIVERED', 
        created_at__gte=this_month_start
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Recent Orders
    recent_orders = Order.objects.select_related('buyer', 'seller').order_by('-created_at')[:10]
    
    # Top Products
    top_products = Product.objects.annotate(
        order_count=Count('orderitem')
    ).order_by('-order_count')[:10]
    
    # Top Sellers
    top_sellers = CustomUser.objects.filter(
        user_type='seller', 
        is_approved=True
    ).annotate(
        product_count=Count('products'),
        total_revenue=Sum('products__orderitem__price')
    ).order_by('-total_revenue')[:10]
    
    # Recent Reviews
    recent_reviews = RatingReview.objects.select_related('product', 'buyer').order_by('-created_at')[:10]
    
    # Pending Reviews
    pending_reviews = RatingReview.objects.filter(is_approved=False).count()
    
    # Cart Statistics
    active_carts = CartItem.objects.values('user').distinct().count()
    total_cart_items = CartItem.objects.count()
    
    context = {
        'page_title': 'Admin Dashboard',
        
        # User Stats
        'total_users': total_users,
        'total_sellers': total_sellers,
        'total_buyers': total_buyers,
        'approved_sellers': approved_sellers,
        'pending_sellers': pending_sellers,
        'seller_approval_rate': (approved_sellers / total_sellers * 100) if total_sellers > 0 else 0,
        
        # Product Stats
        'total_products': total_products,
        'active_products': active_products,
        'inactive_products': inactive_products,
        'product_activation_rate': (active_products / total_products * 100) if total_products > 0 else 0,
        
        # Order Stats
        'total_orders': total_orders,
        'orders_this_month': orders_this_month,
        'orders_last_month': orders_last_month,
        'order_growth': ((orders_this_month - orders_last_month) / orders_last_month * 100) if orders_last_month > 0 else 0,
        
        # Revenue Stats
        'total_revenue': total_revenue,
        'revenue_this_month': revenue_this_month,
        'avg_order_value': (total_revenue / total_orders) if total_orders > 0 else 0,
        
        # Recent Data
        'recent_orders': recent_orders,
        'top_products': top_products,
        'top_sellers': top_sellers,
        'recent_reviews': recent_reviews,
        
        # Other Stats
        'pending_reviews': pending_reviews,
        'active_carts': active_carts,
        'total_cart_items': total_cart_items,
        
        # Quick Actions
        'pending_sellers_list': CustomUser.objects.filter(user_type='seller', is_approved=False)[:5],
        'pending_reviews_list': RatingReview.objects.filter(is_approved=False)[:5],
    }
    
    return render(request, 'admin/dashboard.html', context)


@staff_member_required
def admin_chart_data(request):
    """Provide data for admin charts"""
    
    # Get last 30 days order data
    end_date = now().date()
    start_date = end_date - timedelta(days=30)
    
    orders_by_day = []
    for i in range(30):
        date = start_date + timedelta(days=i)
        order_count = Order.objects.filter(created_at__date=date).count()
        orders_by_day.append({
            'date': date.strftime('%Y-%m-%d'),
            'orders': order_count
        })
    
    # Category distribution
    category_data = Product.objects.values('category').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # User growth
    user_growth = []
    for i in range(12):  # Last 12 months
        month_start = (end_date.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        user_count = CustomUser.objects.filter(
            date_joined__gte=month_start,
            date_joined__lte=month_end
        ).count()
        user_growth.append({
            'month': month_start.strftime('%Y-%m'),
            'users': user_count
        })
    
    data = {
        'orders_by_day': orders_by_day,
        'category_data': list(category_data),
        'user_growth': list(reversed(user_growth)),
    }
    
    return JsonResponse(data)
