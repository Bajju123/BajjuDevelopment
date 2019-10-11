from django.shortcuts import render, get_object_or_404
from .models import OrderItem, Order
from shopping_cart.models import cartItem
from shop.models import Profile
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required



def get_total(request):
    user_id = get_object_or_404(Profile, user=request.user)

    cart = cartItem.objects.filter(user_name=user_id)

    tot = 0

    for item in cart:
        tot = tot + item.total

    return tot


def order_create(request):

    u_name = get_object_or_404(Profile, user=request.user)

    cart = cartItem.objects.filter(user_name=u_name)

    get_cart_total = get_total(request)

    if request.method == 'POST':
        username = u_name
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        postal_code = request.POST.get('pincode')
        city = request.POST.get('city')
        state = request.POST.get('state')

        addOrder = Order(user_name= username,fullname= fullname,email= email,address= address,postal_code= postal_code,city= city,state= state)
        addOrder.save()

        for i in cartItem.objects.filter(user_name=u_name):
            addOrderItem = OrderItem(user_name=username, order=addOrder, product=i.product, price=i.price, total=i.total, quantity=i.quantity)
            addOrderItem.save()

        clear_cart = cartItem.objects.filter(user_name=u_name).delete()

        subject = "Your The Furniture Shop order."
        msg = "Hello " + fullname + ", Thank you for your order." + "Your order has been successfully completed. Your order number is = " + str(addOrder.id)
        to = email
        res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
        if (res == 1):
            print("Mail Sent Successfuly")
        else:
            print("Mail could not sent")

        return render(request, 'orders/order/created.html', {'addOrder': addOrder})

    else:
        return render(request, 'orders/order/create.html', {'cart': cart, 'get_cart_total':get_cart_total})


    return render(request, 'orders/order/create.html', {'cart': cart, 'get_cart_total':get_cart_total})

