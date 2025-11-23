from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
import os

from .models import CartItem, Order, Product, RatingReview


CustomUser = get_user_model()


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = [
            "full_name",
            "email",
            "phone_number",
            "address",
            "user_type",
            "business_name",
            "business_permit",
            "latitude",
            "longitude",
        ]
        widgets = {
            "user_type": forms.Select(attrs={"class": "form-select", "id": "id_user_type"}),
            "latitude": forms.HiddenInput(attrs={"id": "id_latitude"}),
            "longitude": forms.HiddenInput(attrs={"id": "id_longitude"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        user_type = cleaned_data.get("user_type")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        if user_type == "seller":
            business_name = cleaned_data.get("business_name")
            business_permit = cleaned_data.get("business_permit")
            if not business_name or not business_permit:
                raise forms.ValidationError(
                    "Business name and business permit are required for sellers."
                )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        user.is_approved = user.user_type == "buyer"
        user.set_password(password)
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(self.request, username=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password.")
            if user.is_seller and not user.is_approved:
                raise forms.ValidationError(
                    "Your seller account is pending admin approval."
                )
            self.user_cache = user
        return cleaned_data

    def get_user(self):
        return self.user_cache


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "unit", "category", "image"]
        widgets = {
            'unit': forms.Select(attrs={
                'class': 'form-select',
                'style': 'max-width: 200px;',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
            }),
        }
        labels = {
            'unit': 'Unit of Measurement',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make image field optional for updates, but show as required for new products
        if self.instance and self.instance.pk:
            self.fields['image'].required = False
            self.fields['image'].help_text = "Leave empty to keep current image"
        else:
            self.fields['image'].required = True
            self.fields['image'].help_text = "Required: Upload a product image"

    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        # For new products, image is required
        if not self.instance or not self.instance.pk:
            if not image:
                raise forms.ValidationError("Product image is required for new products")
        
        # Validate file size (max 5MB)
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Image file size must be less than 5MB")
        
        # Validate file type
        if image:
            valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            file_extension = os.path.splitext(image.name)[1].lower()
            if file_extension not in valid_extensions:
                raise forms.ValidationError(
                    f"Invalid file type. Allowed types: {', '.join(valid_extensions)}"
                )
        
        return image


class CartAddForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ["quantity"]


class RatingForm(forms.Form):
    """Form for handling star ratings"""
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.HiddenInput()
    )

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating not in [1, 2, 3, 4, 5]:
            raise forms.ValidationError("Invalid rating value")
        return rating


class RatingReviewForm(forms.ModelForm):
    """Form for handling product reviews with ratings"""
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
        label='Rating'
    )

    class Meta:
        model = RatingReview
        fields = ["rating", "comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]
