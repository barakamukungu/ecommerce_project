import stripe
from django.conf import settings
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from .forms import ProductFilterForm
from django.db.models import Q

def add_to_cart(request, product_id):
    # Retrieve the product by id
    product = get_object_or_404(Product, id=product_id)
    
    # Get the cart from session (initialize as empty dict if not present)
    cart = request.session.get('cart', {})

    # Use string keys because session data is serialized to JSON
    product_key = str(product_id)
    if product_key in cart:
        # Increase the quantity if product already exists
        cart[product_key] += 1
    else:
        # Add the product with a quantity of 1
        cart[product_key] = 1

    # Save the updated cart in the session
    request.session['cart'] = cart

    # Optionally add a success message here
    return redirect('store:view_cart')  # or redirect to a different page

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('view_cart')

    # Calculate total in cents
    total_amount = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_amount += int(product.price * 100) * quantity

    # Create a Stripe Checkout Session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'unit_amount': total_amount,  # total_amount in cents
                'product_data': {
                    'name': 'Your Cart Purchase',
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/payment-success/'),
        cancel_url=request.build_absolute_uri('/payment-cancel/'),
    )

    return JsonResponse({'session_id': session.id})

def payment_success(request):
    # Clear the cart after successful payment
    request.session['cart'] = {}
    return render(request, 'store/payment_success.html')

def payment_cancel(request):
    return render(request, 'store/payment_cancel.html')


def add_to_cart(request, product_id):
    """Add a product to the cart session."""
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1  # Increase quantity if already in cart
    else:
        cart[str(product_id)] = 1  # Add new item

    request.session['cart'] = cart  # Save cart back to session
    request.session.modified = True  # Mark session as modified

    return redirect('view_cart')  # Redirect to cart page

def update_cart(request, product_id, quantity):
    """Update quantity of a product in the cart."""
    cart = request.session.get('cart', {})

    if str(product_id) in cart and int(quantity) > 0:
        cart[str(product_id)] = int(quantity)
    elif str(product_id) in cart:
        del cart[str(product_id)]  # Remove item if quantity is zero

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('view_cart')

def view_cart(request):
    """Display the cart with all items."""
    cart = request.session.get('cart', {})  # Retrieve the cart from session
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        except Product.DoesNotExist:
            pass  # Ignore missing products

    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total': total})

def remove_from_cart(request, product_id):
    """Remove a product from the cart."""
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]  # Remove item

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('view_cart')

def clear_cart(request):
    """Clear the entire cart."""
    request.session['cart'] = {}
    request.session.modified = True

    return redirect('view_cart')

def home(request):
    products = Product.objects.all() 
    return render(request, 'store/home.html', {'products': products})

def sales_report(request):
    sales_data = [
        {"date": "2024-02-19", "totalSales": 5000},
        {"date": "2024-02-20", "totalSales": 3000}
    ]
    return render(request, "admin/sales_report.html", {"sales_data": json.dumps(sales_data)})

def filter_products(request):
    category = request.GET.get('category', None)
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    search_query = request.GET.get('search', None)
    min_rating = request.GET.get('min_rating', None)
    in_stock = request.GET.get('in_stock', None)

    products = Product.objects.all()

    if category:
        products = products.filter(category__name=category)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    if min_rating:
        products = products.filter(rating__gte=min_rating)

    if in_stock == "true":
        products = products.filter(stock__gt=0)  # Assuming stock is an integer field

    data = list(products.values('id', 'name', 'price', 'rating', 'stock'))
    return JsonResponse({'products': data})


def filter_products(request):
    category = request.GET.get('category', None)
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    search_query = request.GET.get('search', None)

    products = Product.objects.all()

    if category:
        products = products.filter(category__name=category)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    data = list(products.values('id', 'name', 'price'))
    return JsonResponse({'products': data})


def filter_products(request):
    category = request.GET.get('category', None)
    products = Product.objects.all()
    
    if category:
        products = products.filter(category__name=category)

    data = list(products.values('id', 'name', 'price'))  # Convert to JSON format
    return JsonResponse({'products': data})

def product_list(request):
    products = Product.objects.all()
    form = ProductFilterForm(request.GET)

    if form.is_valid():
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        search = form.cleaned_data.get('search')

        if category:
            products = products.filter(category=category)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        if search:
            products = products.filter(name__icontains=search)

    return render(request, "store/product_list.html", {"products": products, "form": form})

from django.http import HttpResponse

def test_view(request):
    return HttpResponse("Test view works!")
