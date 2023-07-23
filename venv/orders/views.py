# from urllib import request
from django.shortcuts import render,redirect
from django.contrib import messages
from django.utils import timezone
from products.models import Product
from orders.models import Order,OrderDetails,Payment
# Create your views here.

def add_to_cart(request):
    if 'pro_id' in request.GET and 'qt' in request.GET and 'price' in request.GET and request.user.is_authenticated and not request.user.is_anonymous:

        qty = request.GET['qt']
        pro_id = request.GET['pro_id']
        order = Order.objects.all().filter(user=request.user,is_finished=False)
        if not Product.objects.all().filter(id=pro_id).exists():
            return redirect('products')
        pro = Product.objects.get(id=pro_id)
        if order:
            old_order =Order.objects.get(user=request.user,is_finished=False)
            if OrderDetails.objects.all().filter(order=old_order,product=pro).exists():
                order_details=OrderDetails.objects.get(order=old_order,product=pro)
                order_details.quantity+=int(qty)
                order_details.save()
            else:
                order_details = OrderDetails.objects.create(product=pro,order=old_order,price=pro.price,quantity=qty)
                messages.success(request,'Was added to cart for old order ')
        else:
            new_order = Order()
            new_order.user = request.user
            new_order.order_date = timezone.now()
            new_order.is_finished = False
            new_order.save()
            order_details = OrderDetails.objects.create(product=pro,order=new_order,price=pro.price,quantity=qty)
            messages.success(request,'Was added to cart for new order ')
        return redirect('/products/' + request.GET['pro_id'])
    else:
        if 'pro_id' in request.GET:
            messages.error(request,'you must be logged in ')
            return redirect('/products/' + request.GET['pro_id'])
        else:
            return redirect('products')
    
def cart(request):
    context=None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user=request.user,is_finished=False):
            order= Order.objects.get(user=request.user,is_finished=False)
            orderdetails=OrderDetails.objects.all().filter(order=order)
            total =0
            for sum in orderdetails:
                total+=sum.price*sum.quantity
            context = {
                'order':order,
                'orderdetails':orderdetails,
                'total':total,
            }

    return render(request,'order/cart.html',context)

def remove_from_cart(request,orderdetail_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetail_id:
        orderdetail = OrderDetails.objects.get(id=orderdetail_id)
        if orderdetail.order.user.id == request.user.id:
            orderdetail.delete()
    return redirect('cart')

def add_qty(request,orderdetail_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetail_id:
        orderdetails=OrderDetails.objects.get(id=orderdetail_id)
        if orderdetails.order.user.id == request.user.id:
            orderdetails.quantity+=1
            orderdetails.save()
    return redirect('cart')

def sub_qty(request,orderdetail_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetail_id:
        orderdetails=OrderDetails.objects.get(id=orderdetail_id)
        if orderdetails.order.user.id == request.user.id:
            if orderdetails.quantity>1:
                orderdetails.quantity-=1
                orderdetails.save()
    return redirect('cart')

def payment(request):
    context=None
    Shipmentaddress =None
    shipmentphone =None
    cardnumber =None
    expire =None
    securitycode =None
    is_add =None
    if request.method == 'POST' and 'btnpayment' in request.POST and 'btnpayment' in request.POST and 'Shipmentaddress' in request.POST and 'shipmentphone' in request.POST and 'cardnumber' in request.POST and 'expire' in request.POST and 'securitycode' in request.POST:
        context ={
            'Shipmentaddress':Shipmentaddress,
            'shipmentphone':shipmentphone,
            'cardnumber':cardnumber,
            'expire':expire,
            'securitycode':securitycode,
            'is_add':is_add,
        }
        Shipmentaddress =request.POST['Shipmentaddress']
        shipmentphone =request.POST['shipmentphone']
        cardnumber =request.POST['cardnumber']
        expire =request.POST['expire']
        securitycode =request.POST['securitycode']
        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user,is_finished=False):
                order= Order.objects.get(user=request.user,is_finished=False)
                payment = Payment(order=order 
                ,shipment_address=Shipmentaddress,shipment_phone=shipmentphone,card_number=cardnumber,exiper=expire,security_code=securitycode)
                payment.save()
                order.is_finished =True
                order.save()
                is_add=True
                messages.success(request,'Your order is finshed ')
    else:
        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user=request.user,is_finished=False):
                order= Order.objects.get(user=request.user,is_finished=False)
                orderdetails=OrderDetails.objects.all().filter(order=order)
                total =0
                for sum in orderdetails:
                    total+=sum.price*sum.quantity
                totalquantity =0
                for sum in orderdetails:
                    totalquantity+=sum.quantity
                context = {
                    'order':order,
                    'orderdetails':orderdetails,
                    'total':total,
                    'totalquantity':totalquantity,
                }
    return render(request,'order/payment.html',context)
def show_orders(request):
    context = None
    all_orders= None
    if request.user.is_authenticated and not request.user.is_anonymous:
            all_orders =Order.objects.all().filter(user=request.user)
            if all_orders:
                for x in all_orders:
                    order= Order.objects.get(id=x.id)
                    orderdetails=OrderDetails.objects.all().filter(order=order)
                    total =0
                    for sum in orderdetails:
                        total+=sum.price*sum.quantity
                    x.total=total
                    x.items_count = orderdetails.count
                    
    context =  {'all_orders':all_orders}        
    return render(request,'order/show_orders.html',context)