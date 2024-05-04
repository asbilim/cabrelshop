from http.client import HTTPResponse
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Product,Cart,CartItem
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

@login_required
def cart_items_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    total_price = cart_items.aggregate(Sum('quantity'))['quantity__sum']
    print(total_price)
    return render(request, 'listings/cart.html', {
        'cart_items': cart_items,
        'total_price': sum([item.quantity * item.product.price for item in cart_items]),
    })

@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)
   
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return JsonResponse({
        'success': True,
        'cart_item_id': cart_item.id,
        'quantity': cart_item.quantity,
        'total_price': cart_item.get_total_price(),
    })

@login_required
def update_cart_item(request, item_id, action):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()

    return cart_items_view(request)

@login_required
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()

    return cart_items_view(request)
def home(request):

    products = Product.objects.all()
    mixte_products = Product.objects.filter(category__name="mixte")
    food_products = Product.objects.filter(category__name="nourriture")
    boisson_products = Product.objects.filter(category__name="boisson")


    return render(request,"listings/index.html",{'products':products,"food":food_products,"drinks":boisson_products,"mixte":mixte_products})


def details(request,slug=None):

    product = get_object_or_404(Product.objects.all(), slug=slug)

    product_category= get_object_or_404(Category,name=product.category)

    related_products = Product.objects.filter(category__name=product_category)


    return render(request,"listings/details.html",{"product":product,"related_products":related_products})


def shop(request):

    products = Product.objects.all()

    return render(request,"listings/shop.html",{"products":products})

def signin(request):

    if request.user.is_authenticated:

        return redirect('/')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username,password)

        user = authenticate(request,username=username,password=password)
        print(user)
        if user:
            login(request,user)
            return JsonResponse(data={"status": "success", "message": "Redirecting..."})

        return JsonResponse(data={"status":"error","message":"<p class='text-red-500'>incorrect username or password</p>"})



    return render(request,"listings/signin.html")


def signup(request):

    if request.user.is_authenticated:

        return redirect('/')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        print(password)
        if not (password or confirm or username):
            return JsonResponse(data={"status":"error","message":"<p class='text-red-500'>all fields are required</p>"})
        if confirm != password:
            return JsonResponse(data={"status":"error","message":"<p class='text-red-500'>passwords must match</p>"})
            
        
        user,created = get_user_model().objects.get_or_create(username=username, password=password)

    
        user.is_active = True
        if not created:
            return JsonResponse(data={"status":"error","message":"<p class='text-red-500'>user already exists</p>"})


      
        return JsonResponse(data={"status": "success", "message": "Redirecting..."})



    return render(request,"listings/signup.html")


def signout(request):
    logout(request)

    if request.headers.get('HX-Request'):
        return JsonResponse(data={"status": "success", "redirect": True})

    return redirect("signin")