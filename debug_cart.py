from django.contrib.sessions.models import Session
from store.models import Product

# Get the first session
s = Session.objects.first()

if s:
    data = s.get_decoded()
    print("Session Data:", data)

    cart = data.get('cart', {})
    print("Raw Cart Items:", cart)

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            print(f"✅ Found Product: {product.name}, Quantity: {quantity}")
        except Product.DoesNotExist:
            print(f"❌ ERROR: Product with ID {product_id} NOT FOUND!")

else:
    print("No active session found!")
