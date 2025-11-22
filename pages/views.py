from django.contrib import messages
from django.shortcuts import redirect, render

from marketplace.models import Product

from .forms import ContactForm


def home(request):
    featured_products = Product.objects.filter(is_active=True).order_by("-created_at")[:6]
    return render(request, "pages/home.html", {"featured_products": featured_products})


def about(request):
    return render(request, "pages/about.html")


def faq(request):
    return render(request, "pages/faq.html")


def terms(request):
    return render(request, "pages/terms.html")


def privacy(request):
    return render(request, "pages/privacy.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Your message has been sent to the administrator.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "pages/contact.html", {"form": form})
