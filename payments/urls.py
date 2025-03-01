from django.urls import path
from .views import checkout, payment_success, payment_cancel

urlpatterns = [
    path('checkout/<int:product_id>/', checkout, name="checkout"),
    path('success/', payment_success, name="success"),
    path('cancel/', payment_cancel, name="cancel"),
]
