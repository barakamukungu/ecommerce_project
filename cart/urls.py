from django.urls import path
from .views import clear_cart, view_cart, add_to_cart, remove_from_cart
from .views import checkout, process_checkout
from cart import views
from .views import process_payment

urlpatterns = [
    path('', view_cart, name='view_cart'),
    path('', view_cart, name='cart'), 
    path('cart/update/<int:product_id>/<int:quantity>/', views.update_cart, name='update_cart'), 
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', clear_cart, name='clear_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('process_checkout/', process_checkout, name='process_checkout'),
    path('process-payment/', process_payment, name='process_payment'),
]
