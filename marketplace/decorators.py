from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def buyer_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated or not getattr(user, "is_buyer", False):
            messages.error(request, "Buyer access required.")
            return redirect("login")
        return view_func(request, *args, **kwargs)

    return _wrapped


def seller_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated or not getattr(user, "is_seller", False):
            messages.error(request, "Seller access required.")
            return redirect("login")
        if not user.is_approved:
            messages.error(request, "Your seller account is pending admin approval.")
            return redirect("home")
        return view_func(request, *args, **kwargs)

    return _wrapped


def staff_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated or not user.is_staff:
            messages.error(request, "Admin access required.")
            return redirect("login")
        return view_func(request, *args, **kwargs)

    return _wrapped
