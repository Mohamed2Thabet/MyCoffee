from django.shortcuts import get_object_or_404,render
from .models import Product

# Create your views here.
def products(requeset):
    pro=Product.objects.all()
    sc =None
    if 'sc' in requeset.GET:
        sc = requeset.GET['sc']
        if not sc:
            sc ='off'
    if 'searchname' in requeset.GET:
        name=requeset.GET['searchname']
        if name:
            if sc=='on':
                pro=pro.filter(name__contains=name)
            else:
                pro=pro.filter(name__icontains=name)
    if 'searchdesc' in requeset.GET:
        desc = requeset.GET['searchdesc']
        if desc:
            if sc=='on':
                pro=pro.filter(description__contains=desc)
            else:    
                pro=pro.filter(description__icontains=desc)
    if 'pricefrom' in requeset.GET and 'priceto' in requeset.GET:
        prFrom = requeset.GET['pricefrom']
        prTo = requeset.GET['priceto']
        if prFrom.isdigit() and prTo.isdigit():
            pro =pro.filter(price__gte=prFrom ,price__lte=prTo)
    context = {
        'Product':pro
    }
    return render(requeset,'products/products.html',context)
def product(requeset,pro_id):
    context= {
        'pro':get_object_or_404(Product,id=pro_id)
    }
    return render(requeset,'products/product.html',context)
def search(requeset):
    return render(requeset,'products/search.html')