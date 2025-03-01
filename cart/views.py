from django.shortcuts import get_object_or_404, render, redirect
from store.models import Product  # Import your Product model
from django.http import JsonResponse
from .models import CartItem
from django.contrib.auth.decorators import login_required

from store.models import Product
print(Product.objects.all())  # Check if products exist

cart = {'1': 2, '2': 1}  # Example cart
for product_id in cart.keys():
    try:
        product = Product.objects.get(id=int(product_id))
        print(f"Product {product_id} exists: {product.name}")
    except Product.DoesNotExist:
        print(f"ERROR: Product {product_id} does not exist!")

def update_cart(request, product_id, quantity):
    cart = request.session.get('cart', {})
    
    if quantity > 0:
        cart[str(product_id)] = quantity  # Update quantity
    else:
        cart.pop(str(product_id), None)  # Remove item if quantity is 0

    request.session['cart'] = cart  # Save updated cart to session
    return redirect('view_cart')  # Redirect back to cart page

def clear_cart(request):
    request.session['cart'] = {}  # Clear cart session
    request.session.save()
    return redirect('view_cart')


def view_cart(request):
    cart = request.session.get('cart', {})  # Get cart from session
    cart_items = []
    total = 0

    print("\n🔍 DEBUGGING CART FUNCTION")
    print("🛒 SESSION CART DATA:", cart)  

    if not cart:
        print("❌ No items in cart!")
    
    for product_id, quantity in cart.items():
        print(f"🔍 Checking product ID: {product_id}")  # Debugging product ID
        
        try:
            product = Product.objects.get(id=int(product_id))
            print(f"✅ Found product: {product.name} (ID: {product.id})")  # Debugging product fetch

            subtotal = product.price * quantity
            total += subtotal

            cart_items.append({
                'product': product,  
                'quantity': quantity,
                'subtotal': subtotal
            })
        
        except Product.DoesNotExist:
            print(f"❌ ERROR: Product with ID {product_id} NOT FOUND!")

    print("📋 FINAL CART ITEMS:", cart_items)  # Debugging cart items list
 
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'cart/cart.html', {'cart': cart, 'total_price': total_price})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    product = get_object_or_404(Product, id=product_id)

    if str(product_id) in cart and isinstance(cart[str(product_id)], dict):
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': float(product.price),  # Ensure it's a float
            'quantity': 1,
            'image': product.image.url if product.image else '',
        }

    request.session['cart'] = cart
    request.session.modified = True  # Ensure Django saves the session

    return redirect('view_cart')

    cart = request.session.get('cart', {})

    product = Product.objects.get[str(id=product_id)]  # ✅ Fetch product

    if product_id not in cart:
        cart[product_id] = {
            'name': product.name,  # ✅ Store name
            'price': float(product.price),  # ✅ Store price
            'quantity': 1,
            'image': product.image.url if product.image else '/static/default.png'  # ✅ Add image URL
        }
    else:
        cart[product_id]['quantity'] += 1

    request.session['cart'] = cart  # ✅ Save cart back to session
    return redirect('view_cart')

    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1  # Increment quantity
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': float(product.price),  # Convert Decimal to float
            'quantity': 1,
            'image_url': product.image.url if product.image else None  # Ensure image is displayed
        }

    request.session['cart'] = cart  # Save cart back to session
    request.session.modified = True

    print("Cart Data:", request.session['cart'])

    return redirect('view_cart')  # Redirect to cart page

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]  # Remove product from cart
        request.session['cart'] = cart
        request.session.modified = True

    return redirect('view_cart')

from decimal import Decimal  # Import Decimal

def checkout(request):
    print("Checkout view accessed!")  # Debugging output
    
    cart = request.session.get('cart', {})  # Get cart from session
    print("Session Cart Data:", cart)  # Debugging output

    cart_items = []
    subtotal = Decimal("0.00")  # Use Decimal instead of float

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))  # Ensure int ID
            total_price = product.price * quantity
            subtotal += total_price
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': total_price,
            })
        except Product.DoesNotExist:
            print(f"Product with ID {product_id} not found.")  # Debugging output

    tax = subtotal * Decimal("0.10")  # ✅ Convert float to Decimal
    shipping_fee = Decimal("5.00") if subtotal > Decimal("0.00") else Decimal("0.00")
    total = subtotal + tax + shipping_fee

    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'shipping_fee': shipping_fee,
        'total': total
    })

def process_checkout(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        # Simulate order processing (later, save to database)
        cart_items = CartItem.objects.all()
        total = sum(item.product.price * item.quantity for item in cart_items)

        # Here, you would save the order and clear the cart
        cart_items.delete()  # Clear cart after checkout

        return JsonResponse({'status': 'success', 'message': 'Order placed successfully!', 'total': total})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def process_payment(request):
    return render(request, 'cart/payment.html')