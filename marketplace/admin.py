from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.db.models import Avg

from .models import CartItem, CustomUser, Order, OrderItem, Product, RatingReview


class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ("email", "full_name", "user_type", "is_approved", "is_staff", "date_joined")
    list_filter = ("user_type", "is_approved", "is_staff", "date_joined")
    ordering = ("-date_joined",)
    search_fields = ("email", "full_name", "phone_number", "business_name")
    
    # Add custom actions
    actions = ['approve_sellers', 'disapprove_sellers', 'make_staff', 'remove_staff']
    
    def approve_sellers(self, request, queryset):
        queryset.filter(user_type='seller').update(is_approved=True)
        self.message_user(request, "Selected sellers have been approved.")
    approve_sellers.short_description = "Approve selected sellers"
    
    def disapprove_sellers(self, request, queryset):
        queryset.filter(user_type='seller').update(is_approved=False)
        self.message_user(request, "Selected sellers have been disapproved.")
    disapprove_sellers.short_description = "Disapprove selected sellers"
    
    def make_staff(self, request, queryset):
        queryset.update(is_staff=True)
        self.message_user(request, "Selected users are now staff.")
    make_staff.short_description = "Make selected users staff"
    
    def remove_staff(self, request, queryset):
        queryset.update(is_staff=False)
        self.message_user(request, "Staff privileges removed from selected users.")
    remove_staff.short_description = "Remove staff privileges"

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "full_name",
                    "phone_number",
                    "address",
                    "user_type",
                    "business_name",
                    "business_permit",
                    "latitude",
                    "longitude",
                )
            },
        ),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "is_approved", "groups", "user_permissions")},
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "user_type", "is_staff", "is_superuser"),
            },
        ),
    )

    filter_horizontal = ("groups", "user_permissions")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price_at_time')
    
    def product_name(self, obj):
        return obj.product.name if obj.product else "Deleted Product"
    
    def price_at_time(self, obj):
        return f"₱{obj.price}" if obj.price else "N/A"


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", "seller", "status", "total_amount", "item_count", "created_at")
    list_filter = ("status", "created_at", "buyer", "seller")
    search_fields = ("buyer__email", "buyer__full_name", "seller__email", "seller__full_name")
    readonly_fields = ("created_at", "updated_at", "total_amount")
    inlines = [OrderItemInline]
    
    # Add custom actions
    actions = ['mark_pending', 'mark_confirmed', 'mark_shipped', 'mark_delivered', 'mark_cancelled']
    
    def mark_pending(self, request, queryset):
        queryset.update(status='PENDING')
        self.message_user(request, "Orders marked as pending.")
    mark_pending.short_description = "Mark as pending"
    
    def mark_confirmed(self, request, queryset):
        queryset.update(status='CONFIRMED')
        self.message_user(request, "Orders marked as confirmed.")
    mark_confirmed.short_description = "Mark as confirmed"
    
    def mark_shipped(self, request, queryset):
        queryset.update(status='SHIPPED')
        self.message_user(request, "Orders marked as shipped.")
    mark_shipped.short_description = "Mark as shipped"
    
    def mark_delivered(self, request, queryset):
        queryset.update(status='DELIVERED')
        self.message_user(request, "Orders marked as delivered.")
    mark_delivered.short_description = "Mark as delivered"
    
    def mark_cancelled(self, request, queryset):
        queryset.update(status='CANCELLED')
        self.message_user(request, "Orders marked as cancelled.")
    mark_cancelled.short_description = "Mark as cancelled"
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = "Items"


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "seller", "price", "category", "unit", "is_active", "rating_display", "created_at")
    list_filter = ("category", "is_active", "unit", "created_at", "seller")
    search_fields = ("name", "description", "seller__email", "seller__full_name")
    readonly_fields = ("created_at", "updated_at", "rating_display", "image_preview")
    
    # Add custom actions
    actions = ['activate_products', 'deactivate_products', 'featured_products']
    
    def activate_products(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected products have been activated.")
    activate_products.short_description = "Activate selected products"
    
    def deactivate_products(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected products have been deactivated.")
    deactivate_products.short_description = "Deactivate selected products"
    
    def rating_display(self, obj):
        avg_rating = obj.average_rating
        if avg_rating:
            stars = "⭐" * int(avg_rating)
            return format_html(f"{stars} {avg_rating:.1f}")
        return "No ratings"
    rating_display.short_description = "Rating"
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Image Preview"
    
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "description", "seller")
        }),
        ("Pricing & Category", {
            "fields": ("price", "category", "unit")
        }),
        ("Media", {
            "fields": ("image", "image_preview")
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at", "rating_display"),
            "classes": ("collapse",)
        }),
    )


class RatingReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "buyer", "rating_display", "is_approved", "created_at")
    list_filter = ("rating", "is_approved", "created_at")
    search_fields = ("product__name", "buyer__email", "buyer__full_name", "comment")
    readonly_fields = ("created_at",)
    
    # Add custom actions
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected reviews have been approved.")
    approve_reviews.short_description = "Approve selected reviews"
    
    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, "Selected reviews have been disapproved.")
    disapprove_reviews.short_description = "Disapprove selected reviews"
    
    def rating_display(self, obj):
        stars = "⭐" * obj.rating
        return f"{stars} ({obj.rating}/5)"
    rating_display.short_description = "Rating"


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity", "added_at")
    list_filter = ("added_at", "user")
    search_fields = ("user__email", "user__full_name", "product__name")
    readonly_fields = ("added_at",)
    
    # Add custom actions
    actions = ['clear_cart_items']
    
    def clear_cart_items(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"Cleared {count} cart items.")
    clear_cart_items.short_description = "Clear selected cart items"


# Register all admin classes
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(RatingReview, RatingReviewAdmin)

# Customize admin site
admin.site.site_header = "Kaumahan Harvest Market Administration"
admin.site.site_title = "KHM Admin"
admin.site.index_title = "Welcome to Kaumahan Harvest Market Admin Portal"
