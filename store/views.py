from django.shortcuts import render
from .models import *

# Create your views here.
def store(request):
    products = Product.objects.all()
    content = {'products': products}
    return render(request, 'store/store.html', content)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}

    content = {'items': items, 'order':order}
    return render(request, 'store/cart.html', content) 


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else: 
        # it will create an empty for now none-logged in users
        order = {'get_cart_total': 0, 'get_cart_items':0}
        items = []
    content = {'items':items, 'order':order}
    return render(request, 'store/checkout.html', content)


