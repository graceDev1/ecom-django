from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import datetime
import json
from .utils import cookieCart, cartData

# Create your views here.
def store(request):
   data = cartData(request)
   cartItems = data['cartItems']
   
   products = Product.objects.all()

   content = {'products': products, 'cartItems': cartItems, 'shipping': True}
   return render(request, 'store/store.html', content)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    content = {'items': items, 'order':order, 'cartItems': cartItems, 'shipping': True}
    return render(request, 'store/cart.html', content) 


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    content = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', content)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action', action)
    print('Product', data)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem , created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)



def processOrder(request):
    print('Data',request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        if total == order.get_cart_total:
            order.complete = True
        order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
        
    else:
        print("user ins not logged in")
    return JsonResponse('Payment complite...', safe=False)


