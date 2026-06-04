from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product


def get_cart(request):
    return request.session.get('cart', {})


def cart_view(request):
    cart = get_cart(request)
    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'cart/cart.html', {
        'products': products,
        'total': total,
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    product_id_str = str(product_id)

    if product.stock <= 0:
        return redirect('cart:cart_view')

    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    request.session['cart'] = cart
    return redir

def update_cart(request, product_id):
    cart = get_cart(request)
    product_id_str = str(product_id)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > 0:
        cart[product_id_str] = quantity
    else:
        cart.pop(product_id_str, None)

    request.session['cart'] = cart
    return redirect('cart:cart_view')


def remove_from_cart(request, product_id):
    cart = get_cart(request)
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart:cart_view')


def clear_cart(request):
    request.session['cart'] = {}
    return redirect('cart:cart_view')