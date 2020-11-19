from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Product
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User 
from django.contrib.auth  import authenticate,  login, logout


def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)



def productview(request, myid):

    # Fetch the product using the id
    product = Product.objects.filter(id=myid).first()
    product.popularity += 1
    product.save()
    
    return render(request, 'shop/prodview.html', {'product':product})

