from django.shortcuts import render, HttpResponse, redirect
from math import ceil
from home.models import Contact
from django.contrib import messages 
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.auth  import authenticate,  login, logout
from blog.models import Post
from shop.models import Product

def home(request): 
    return render(request, "home/home.html")

def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content =request.POST['desc']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact=Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
    return render(request, "home/contact.html")



def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc_product.lower() or query in item.ad_titel.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('query')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    
    if len(allProds) == 0 or len(query) == 0:
        messages.warning(request, "No search results found. Please refine your query.")
    params = {'allProds': allProds, "query": query}    
    return render(request, 'home/search.html', params)






def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        if len(username)<5:
            messages.error(request, " Your user name must be under 5 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('home')
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your Account has been successfully created, now login to continue!")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")


def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/shop")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/")

    
   



def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')


def about(request): 
    return render(request, "home/about.html")



def sell(request):

    if request.method =="POST" and request.FILES['myfile']:
        category = request.POST.get('catogery', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc_product = request.POST.get('desc_product', '')
        ad_titel = request.POST.get('ad_titel', '')
        price = request.POST.get('price', '')
        wa_phone = request.POST.get('wa_phone', '')
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        url = fs.url(filename)
        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(desc_product) < 4:
            messages.error(request, "Please fill the form correctly")
        else:
            product = Product(name=name, email=email, phone=phone, desc_product= desc_product,ad_titel= ad_titel,category = category,price=price,wa_phone=wa_phone,
            image = url)
            product.save()
            messages.success(request, "Your add has been posted successfully, now just sit back and relax, wait for the buyers to contact you")
    return render(request, "home/sell.html")
