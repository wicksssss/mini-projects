from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Order, OrderItem


class OrderForm(forms.Form):
    phone = forms.CharField(
        max_length=20,
        validators=[
            __import__('django.core.validators', fromlist=['RegexValidator']).RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Enter a valid phone number'
            )
        ]
    )
    address = forms.CharField(max_length=500)
    comment = forms.CharField(required=False, widget=forms.Textarea)


def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Your cart is empty')
        return redirect('product_list')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                comment=form.cleaned_data.get('comment', ''),
                status='new'
            )
            from products.models import Product
            total = 0
            for product_id, quantity in cart.items():
                product = get_object_or_404(Product, pk=product_id)
                price = product.discount_price or product.price
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
            messages.success(request, f'Order #{order.pk} created successfully!')
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm()

    return render(request, 'orders/checkout.html', {'form': form, 'cart': cart})


@login_required
def order_list_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.user != request.user:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    return render(request, 'orders/order_detail.html', {'order': order})