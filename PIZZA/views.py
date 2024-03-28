from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from PIZZA.models import *

from instamojo_wrapper import Instamojo
from django.conf import settings
api = Instamojo(api_key = settings.API_KEY, auth_token=settings.AUTH_TOKEN, endpoint="https://test.instamojo.com/api/1.1/")
# Create your views here.
def home(request):
    pizzas = Pizza.objects.all()
    context = {'pizzas': pizzas} 
    return render (request,'home.html', context)



@login_required(login_url='/login/')
def add_cart(request,pizza_uid):
    user = request.user
    pizza_obj = Pizza.objects.get(uid = pizza_uid)
    cart , _ = Cart.objects.get_or_create(user = user,is_paid=False)
    cart_items = CratItems.objects.create(
        cart = cart, 
        pizza = pizza_obj
        )
    return redirect('/')


def login_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username = username)
            if not  user_obj.exists():
                messages.warning(request,'Username not found')
                return redirect('/login/')
            
            user_obj = authenticate(username = username, password = password)
            if user_obj:
                login(request,user_obj)
                return redirect('/')
            messages.warning(request,'Invalid username or password')
            return redirect('/login/')
        except Exception as e:
            messages.warning(request,'Something went wrong')
            return redirect('/login/')
    return render(request , 'login.html')



def register_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username = username)
            if user_obj.exists():
                messages.warning(request,'Username is taken')
                return redirect('/register/')
            user_obj = User.objects.create(username = username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request,'Account created.')
            return redirect('/login/')
        except Exception as e:
            messages.warning(request,'SOmething went wrong')
            return redirect('/register/')
    return render(request , 'register.html')

from django.contrib import messages

@login_required(login_url='/login/')
def cart(request):
    try:
        cart = Cart.objects.get(is_paid=False, user=request.user)
        cart_items = cart.carts.all()
        if not cart_items:
            messages.warning(request, 'Your cart is empty. Please add items to your cart first.')
            return redirect('/')
        response = api.payment_request_create(
            amount=cart.get_cart_total(),
            purpose="Order",
            buyer_name=request.user.username,
            email="singhmurari655@gmail.com",
            redirect_url="http://127.0.0.1:8000/success/"
        )
        cart.in_id = response['payment_request']['id']
        cart.save()
        context = {'carts': cart, 'payment_url': response['payment_request']['longurl']}
        return render(request, 'cart.html', context)
    except Cart.DoesNotExist:
        messages.warning(request, 'Your cart is empty. Please add items to your cart first.')
        return redirect('/')


@login_required(login_url='/login/')
def remove_cart_items(request, cart_items_uid):
    try:
        cart_item = CratItems.objects.get(uid=cart_items_uid)
        cart_item.delete()
        return redirect('/cart/')
    except Exception as e:
        print(e)

@login_required(login_url='/login/')
def orders(request):
    orders = Cart.objects.filter(is_paid = True, user = request.user)
    context = {'orders': orders}
    return render(request,'orders.html', context)

@login_required(login_url='/login/')
def success(request):
    payment_request = request.GET.get('payment_request_id')
    cart = Cart.objects.get(in_id = payment_request)
    cart.is_paid = True
    cart.save()
    return redirect('/orders/')