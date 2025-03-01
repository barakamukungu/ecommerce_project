from django.urls import path
from .views import clear_cart, home, filter_products, test_view, add_to_cart, update_cart, view_cart, remove_from_cart, checkout, payment_success, payment_cancel

app_name = "store"


urlpatterns = [
    path('', home, name='home'),  # Home page route at /
    path('filter-products/', filter_products, name='filter_products'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/<int:quantity>/', update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', clear_cart, name='clear_cart'),
    path('checkout/', checkout, name='checkout'),
    path('payment-success/', payment_success, name='payment_success'),
    path('payment-cancel/', payment_cancel, name='payment_cancel'),
    path('test/', test_view, name='test'),
]
