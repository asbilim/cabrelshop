from http.client import HTTPResponse
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Product
from django.contrib.auth import login,authenticate,logout
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


    return render(request,"listings/shop.html")

def signin(request):

    if request.user.is_authenticated:

        return redirect('/')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
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

        if not (password or confirm or username):
            return JsonResponse(data={"status":"error","message":"<p class='text-red-500'>all fields are required</p>"})
        if confirm != password:
            return JsonResponse(data={"status":"error","message":"<p class='text-red-500'>passwords must match</p>"})
            
        
        user,created = get_user_model().objects.get_or_create(username=username, password=password)

        if not created:
            return JsonResponse(data={"status":"error","message":"<p class='text-red-500'>user already exists</p>"})


      
        return JsonResponse(data={"status": "success", "message": "Redirecting..."})



    return render(request,"listings/signup.html")


def signout(request):

    logout(request)

    return JsonResponse(data={"status": "success", "message":"logout successful"})