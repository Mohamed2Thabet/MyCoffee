from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product
# Create your views here.

def index(requeset):
    context = {
        'Product':Product.objects.all()
    }
    return render(requeset,'pages/index.html',context)
def about(requeset):
    return render(requeset,'pages/about.html')
def cooffee(requeset):
    return render(requeset,'pages/coffee.html')