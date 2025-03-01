import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from store.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request, product_id):
    product = Product.objects.get(id=product_id)
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': product.name},
                'unit_amount': int(product.price * 100),  # Convert dollars to cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url="http://localhost:8000/payments/success/",
        cancel_url="http://localhost:8000/payments/cancel/",
    )
    
    return JsonResponse({'session_id': session.id})

def payment_success(request):
    return render(request, "payments/success.html")

def payment_cancel(request):
    return render(request, "payments/cancel.html")
