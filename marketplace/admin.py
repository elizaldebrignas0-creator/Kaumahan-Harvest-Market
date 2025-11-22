from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CartItem, CustomUser, Order, OrderItem, Product, RatingReview


class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ("email", "full_name", "user_type", "is_approved", "is_staff")
    list_filter = ("user_type", "is_approved", "is_staff")
    ordering = ("email",)
    search_fields = ("email", "full_name", "phone_number")

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


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", "seller", "status", "total_amount", "created_at")
    list_filter = ("status", "created_at")
    inlines = [OrderItemInline]


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "seller", "price", "category", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")


class RatingReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "buyer", "rating", "is_approved", "created_at")
    list_filter = ("rating", "is_approved")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(RatingReview, RatingReviewAdmin)
