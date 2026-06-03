from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from products.models import Product
from cart.views import get_cart


@login_required
def checkout_view(request):
    cart = get_cart(request)

    if not cart:
        messages.error(request, 'Кошик порожній!')
        return redirect('cart')

    if request.method == 'POST':
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        order = Order.objects.create(
            user=request.user,
            phone=phone,
            address=address,
            status='pending',
            total_price=0
        )

        total = 0
        for product_id, item in cart.items():
            product = get_object_or_404(Product, id=product_id)
            quantity = item['quantity']
            price = product.price
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )
            total += price * quantity

        order.total_price = total
        order.save()

        request.session['cart'] = {}
        messages.success(request, f'Замовлення №{order.id} оформлено!')
        return redirect('order_list')

    return render(request, 'orders/checkout.html')


@login_required
def order_list_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.user != request.user:
        return redirect('order_list')
    return render(request, 'orders/order_detail.html', {'order': order})