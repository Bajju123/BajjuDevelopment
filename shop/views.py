from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from . models import Category,Product, feedback, Profile
from shopping_cart.forms import CartAddProductForm
from orders.models import Order, OrderItem
from datetime import datetime
from datetime import timedelta
from django.contrib import messages
from django.contrib.messages import get_messages
import re
from django.db.models import Q, Sum
from django.contrib.auth.models import User, auth
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
# Create your views here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-copyZ0-9._-]+\.[a-zA-Z]+$')



def register(request, category_slug= None):

    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        pwd1 = request.POST.get('pwd1')
        pwd2 = request.POST.get('pwd2')

        if len(email) < 1:
            messages.add_message( request, messages.ERROR, "Email is required!")

        if not EMAIL_REGEX.match( email ):
            messages.add_message(request, messages.ERROR, "Invalid email format! Ex: test@text.com")

        if len(pwd1) < 8:
            messages.add_message(request, messages.ERROR, "Password must be between 8-32 character!")

        if pwd1 != pwd2:
            messages.add_message(request, messages.ERROR, "Password and Confirm Password must match!")

        if User.objects.filter(email=email).count() > 0:
            messages.add_message(request, messages.ERROR, "A user with this email is already exists!")

        if User.objects.filter(username=uname).exists():
            messages.add_message(request, messages.ERROR, "A user with this user name is already exists!")

        if len(get_messages(request)) > 0:
            msg = get_messages(request)
            return render(request, 'reg_login/register.html', {'msg': msg})

        else:

            user = User.objects.create_user(first_name=fname, last_name=lname, username=uname, email=email, password=pwd1)
            user.save()

            subject = "Registration Successfull"
            msg = "Welcome and Thanks for Signing Up :-)"
            to = email
            res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
            if (res == 1):
                print("Mail Sent Successfuly")
            else:
                print("Mail could not sent")

        return render(request, 'reg_login/login.html')

    else:
        return render(request, 'reg_login/register.html')


def login(request, category_slug= None):

    if request.method == "POST":

        username = request.POST.get('login_uname')
        password = request.POST.get('login_pwd')

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)

            category = None
            categories = Category.objects.all()
            products = Product.objects.filter(available=True)

            if category_slug:
                category = get_object_or_404(Category, slug=category_slug)
                products = products.filter(category=category)


            return render(request, 'shop/products/list.html', {'category': category,
                                                               'categories': categories,
                                                               'products': products})

        else:
            messages.add_message(request, messages.ERROR, "Invalid UserName or Password !!")

            if len(get_messages(request)) > 0:
                msg = get_messages(request)
                return render(request, 'reg_login/login.html', {'msg': msg})

            return render(request, 'reg_login/login.html')



    else:
        return render(request, 'reg_login/login.html')

def logout(request, category_slug= None):
    auth.logout(request)

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/products/list.html', {'category': category,
                                                       'categories': categories,
                                                       'products': products})

def product_list(request, category_slug= None):

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/products/list.html', {'category': category,
                                                  'categories': categories,
                                                  'products': products})

def department(request, category_slug= None):

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/products/departments.html', {'category': category,
                                                  'categories': categories,
                                                  'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    return render(request, 'shop/products/detail.html',
                  {'product': product,
                   'cart_product_form':cart_product_form})

def about(request):
    return render(request, 'shop/ExtraPages/aboutus.html')

def contact(request):

    if request.method == "POST":
        name = request.POST.get('txtName')
        email = request.POST.get('txtEmail')
        phone_number = request.POST.get('txtPhone')
        message = request.POST.get('txtMsg')

        feedbackObj = feedback(name = name,email = email,p_nm = phone_number,msg =message)
        feedbackObj.save()

        return render(request, 'shop/ExtraPages/contactus.html')
    else:

        return render(request, 'shop/ExtraPages/contactus.html')

    return render(request, 'shop/ExtraPages/contactus.html')

@login_required(login_url='shop:login')
def check_order(request):
    u_name = get_object_or_404(Profile, user=request.user)
    return render(request, 'shop/ExtraPages/CheckOrder.html', {'u_name':u_name} )

@login_required(login_url='shop:login')
def order_detail(request):
    try:
        orderid = request.GET.get('orderid')
        u_name = get_object_or_404(Profile, user=request.user)
        order_detail = Order.objects.filter(user_name=u_name, id=orderid)[0]

        order_items = OrderItem.objects.filter(order=orderid)

        o_id = order_detail.id
        fullname = order_detail.fullname
        address = order_detail.address
        postal_code = order_detail.postal_code
        city = order_detail.city
        state = order_detail.state
        country = "India"
        updated = order_detail.updated

        total_price = list(OrderItem.objects.filter(order=orderid).aggregate(Sum('total')).values())[0]

        placeDate = updated + timedelta(days=5)

        return render(request, 'shop/ExtraPages/OrderDetail.html', {'o_id': o_id,
                                                                    'fullname': fullname,
                                                                    'address': address,
                                                                    'postal_code': postal_code,
                                                                    'city': city,
                                                                    'state': state,
                                                                    'country': country,
                                                                    'updated': updated,
                                                                    'placeDate' : placeDate,
                                                                    'order_items' : order_items,
                                                                    'total_price' :total_price})

    except Exception as e:
        u_name = get_object_or_404(Profile, user=request.user)
        return render(request, 'shop/ExtraPages/CheckOrder.html', {'u_name': u_name})

@login_required(login_url='shop:login')
def cancle_order(request):

    try:
        if request.method == "POST":
            orderID = request.POST.get('orderID')
            u_name = get_object_or_404(Profile, user=request.user)

            order_items = OrderItem.objects.filter(order=orderID)
            order_detail = Order.objects.filter(user_name=u_name, id=orderID)[0]

            o_id = order_detail.id
            fullname = order_detail.fullname
            email = order_detail.email

            subject = "Your order has been cancelled."
            msg = "Hello " + fullname + ", We're writing to let you know that your order has been successfully cancelled." + "Your Order id is = " +str(o_id)
            to = email
            res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
            if (res == 1):
                print("Mail Sent Successfuly")
            else:
                print("Mail could not sent")


            order_items.delete()
            order_detail.delete()


            return render(request, 'shop/ExtraPages/CancleOrder.html')

        return render(request, 'shop/ExtraPages/CancleOrder.html')
    except Exception as e:
        return render(request, 'shop/ExtraPages/CancleOrder.html')

def search(request, category_slug= None):

    query = request.GET.get('search')

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(Q(name__icontains=query) | Q(price__icontains=query) | Q(description__icontains=query))

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/ExtraPages/search.html', {'category': category,
                                                  'categories': categories,
                                                  'products': products})




