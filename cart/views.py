from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product


def get_cart(request):
    return request.session.get('cart', {})


def cart_view(request):
    cart = get_cart(request)
    products_in_cart = []
    total = 0

    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * item['quantity']
        total += subtotal
        products_in_cart.append({
            'product': product,
            'quantity': item['quantity'],
            'subtotal': subtotal,
        })

    return render(request, 'cart/cart.html', {
        'cart_items': products_in_cart,
        'total': total,
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {'quantity': 1}

    request.session['cart'] = cart
    return redirect('cart')


def update_cart(request, product_id):
    cart = get_cart(request)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > 0:
        cart[str(product_id)]['quantity'] = quantity
    else:
        cart.pop(str(product_id), None)

    request.session['cart'] = cart
    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = get_cart(request)
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart')


def clear_cart(request):
    request.session['cart'] = {}
    return redirect('cart')