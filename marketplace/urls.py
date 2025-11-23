from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve

from . import views


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("dashboard/", views.dashboard_redirect, name="dashboard"),

    path("buyer/", views.buyer_dashboard, name="buyer_dashboard"),
    path("seller/", views.seller_dashboard, name="seller_dashboard"),
    path("admin-panel/", views.admin_dashboard, name="admin_dashboard"),

    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout_view, name="checkout"),
    path("checkout/order/<int:order_id>/", views.checkout_view, name="checkout_order"),
    path("checkout/direct/<int:product_id>/", views.checkout_direct, name="checkout_direct"),
    path("orders/buyer/", views.buyer_orders, name="buyer_orders"),
    path("orders/seller/", views.seller_orders, name="seller_orders"),

    path("products/create/", views.product_create, name="product_create"),
    path("products/<int:pk>/edit/", views.product_update, name="product_update"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),

    path("sellers/<int:user_id>/approve/", views.approve_seller, name="approve_seller"),
    path("sellers/<int:user_id>/reject/", views.reject_seller, name="reject_seller"),
]

# Serve media files in both development and production
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
