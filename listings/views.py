from django.shortcuts import render

def home(request):

    return render(request,"listings/index.html")


def details(request):

    return render(request,"listings/details.html")


def shop(request):

    return render(request,"listings/shop.html")