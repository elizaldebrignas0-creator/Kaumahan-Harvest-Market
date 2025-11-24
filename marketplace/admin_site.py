from django.contrib.admin import AdminSite
from django.urls import path
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


class KaumahanAdminSite(AdminSite):
    """Custom admin site for Kaumahan Harvest Market"""
    
    site_header = "Kaumahan Harvest Market Administration"
    site_title = "KHM Admin"
    index_title = "Welcome to Kaumahan Harvest Market Admin Portal"
    
    def get_urls(self):
        from .admin_views import admin_dashboard, admin_chart_data
        
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', admin_dashboard, name='dashboard'),
            path('chart-data/', admin_chart_data, name='chart_data'),
        ]
        return custom_urls + urls
    
    def index(self, request, extra_context=None):
        """Redirect to custom dashboard"""
        from django.shortcuts import redirect
        return redirect('dashboard')
    
    def each_context(self, request):
        context = super().each_context(request)
        context.update({
            'site_dashboard_url': 'dashboard/',
            'custom_stats': self.get_admin_stats(),
        })
        return context
    
    def get_admin_stats(self):
        """Get quick stats for admin header"""
        from .models import Product, CustomUser, Order, RatingReview
        
        return {
            'total_products': Product.objects.filter(is_active=True).count(),
            'pending_sellers': CustomUser.objects.filter(user_type='seller', is_approved=False).count(),
            'pending_orders': Order.objects.filter(status='PENDING').count(),
            'pending_reviews': RatingReview.objects.filter(is_approved=False).count(),
        }


# Create custom admin site instance
kaumahan_admin_site = KaumahanAdminSite(name='kaumahan_admin')
