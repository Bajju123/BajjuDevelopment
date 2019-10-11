from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product, Profile
from . forms import CartAddProductForm
from . models import cartItem
from django.contrib.auth.decorators import login_required

@login_required(login_url='shop:login')
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data

        u_name = get_object_or_404(Profile, user=request.user)

        price = product.price
        quantity = cd['quantity']
        total = price * quantity

        addCart = cartItem(product=product, quantity=quantity, price=price, total=total, user_name=u_name)
        addCart.save()

    return redirect('shopping_cart:cart_detail')

def update_cart(request, product_id):

    if request.method == "POST":
        u_name = get_object_or_404(Profile, user=request.user)
        product = get_object_or_404(Product, id=product_id)
        price = product.price
        update_quantity = request.POST.get('update_quantity')
        total = price * int(update_quantity)

        if update_quantity:
            addCart = cartItem.objects.filter(user_name=u_name, product=product).update(quantity=update_quantity, total=total)

        return redirect('shopping_cart:cart_detail')

def cart_remove(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    u_name = get_object_or_404(Profile, user=request.user)
    removeCartItem = cartItem.objects.filter(product=product, user_name=u_name).delete()

    return redirect('shopping_cart:cart_detail')

def get_total(request):
    user_id = get_object_or_404(Profile, user=request.user)

    cart = cartItem.objects.filter(user_name=user_id)

    tot = 0

    for item in cart:
        tot = tot + item.total

    return tot

@login_required(login_url='shop:login')
def cart_detail(request):

    user_id = get_object_or_404(Profile, user=request.user)

    cart = cartItem.objects.filter(user_name=user_id)

    get_cart_total = get_total(request)

    # print("total ============ ",get_cart_total)


    return render(request, 'shopping_cart/cart_detail.html', {'cart': cart, 'get_cart_total': get_cart_total })