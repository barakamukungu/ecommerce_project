from django import forms
from store.models import Product

class ProductFilterForm(forms.Form):
    category = forms.ChoiceField(choices=[('', 'All Categories')] + Product.CATEGORY_CHOICES, required=False)
    min_price = forms.DecimalField(required=False, min_value=0, label="Min Price")
    max_price = forms.DecimalField(required=False, min_value=0, label="Max Price")
    search = forms.CharField(required=False, max_length=100, label="Search")
