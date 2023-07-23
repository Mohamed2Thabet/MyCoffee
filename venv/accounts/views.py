from urllib import request
from django.shortcuts import render ,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from .models import UserProfile
from products.models import Product
import re
from django.contrib.auth.decorators import login_required


# Create your views here.
def singnin(request):
    
    if request.method =="POST" and 'btnsignin' in request.POST:
        username=request.POST['user']
        password=request.POST['pass']
        user =auth.authenticate(username=username,password=password)
        if user is not None:
            if 'remember' not in  request.POST:
                request.session.set_expiry(0)
            auth.login(request,user)
            # messages.success(request,'you are now logged in')
        else:
            messages.error(request,'Username or Password Invalid')
        return redirect('signin')
    else:
        return render(request,'accounts/signin.html')
def signup(request):
    if request.method =="POST" and 'btnsignup' in request.POST:
        # variable for fields

        fname=None
        lname=None
        address=None
        address2=None
        city = None
        state =None
        zip_number=None
        email=None
        username=None
        password=None
        terms =None
        is_add=False

        #Get value from the form
        if 'fname' in request.POST: fname=request.POST['fname']
        else : messages.error(request,"Error in first name")
        if 'lname' in request.POST: lname=request.POST['lname']
        else : messages.error(request,"Error in last name")
        if 'address' in request.POST: address=request.POST['address']
        else : messages.error(request,"Error in address")
        if 'address2' in request.POST: address2=request.POST['address2']
        else : messages.error(request,"Error in address 2")
        if 'city' in request.POST: city=request.POST['city']
        else : messages.error(request,"Error in city")
        if 'state' in request.POST: state=request.POST['state']
        else : messages.error(request,"Error in state")
        if 'zip_number' in request.POST: zip_number=request.POST['zip_number']
        else : messages.error(request,"Error in zip_number")
        if 'email' in request.POST: email=request.POST['email']
        else : messages.error(request,"Error in email")
        if 'username' in request.POST: username=request.POST['username']
        else : messages.error(request,"Error in username")
        if 'password' in request.POST: password=request.POST['password']
        else : messages.error(request,"Error in password")
        if 'terms' in request.POST: terms=request.POST['terms']
    
        if fname and lname and address and address2 and city and state and zip_number and email and username and password:
            if  terms == 'on':
                #Check username is taken
                if User.objects.filter(username=username).exists():
                    messages.error(request,'this username is taken')
                else :  #Check email is taken
                    if User.objects.filter(email=email).exists():
                        messages.error(request,'this email is taken')
                    else :
                        patt="^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                        if re.match(patt,email):
                            #add user
                            user=User.objects.create_user(first_name=fname,last_name=lname,email=email,username=username,password=password)
                            user.save()
                            #add userprofile
                            userprofile=UserProfile(user=user,address=address,address2=address2,city=city,state=state,zip_number=zip_number)
                            userprofile.save()
                            #claer 
                            fname=''
                            lname=''
                            address=''
                            address2=''
                            city = ''
                            state =''
                            zip_number=''
                            email=''
                            username=''
                            password=''
                            terms =None
                            messages.success(request,'Your account is created')
                            is_add=True
                        else:
                            messages.error(request,'Invalid email')
            else: messages.error(request,'you must agree to the terms')
        else: messages.error(request,'check empty fields')
        
        
        return render(request,'accounts/signup.html',context={'fname':fname,
        'lname':lname,
        'address':address,
        'address2':address2,
        'city':city,
        'state':state,
        'zip_number':zip_number,
        'email':email,
        'username':username,
        'password':password,
        'is_add':is_add })
    else:
        return render(request,'accounts/signup.html')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')

def profile(request):
    
    if request.method =="POST" and 'btnprofile' in request.POST:
        if request.user is not None and request.user.id != None:
            userprofile=UserProfile.objects.get(user=request.user)

            if request.POST['fname'] and request.POST['lname'] and request.POST['address'] and request.POST['address2'] and request.POST['city'] and request.POST['state']  and request.POST['zip_number'] and request.POST['email'] and request.POST['user'] and request.POST['pass']:
                request.user.frist_name = request.POST['fname']
                request.user.last_name = request.POST['lname']
                UserProfile.address =request.POST['address']
                UserProfile.address2 =request.POST['address2']
                UserProfile.city =request.POST['city']
                # UserProfile.zip_number =request.POST['zip_number']
                UserProfile.state =request.POST['address']
                # request.user.email = request.POST['email']
                # request.user.username = request.POST['user']
                if not request.POST['pass'].startswith('pbkdf2_sha256$'):
                    request.user.set_password(request.POST['pass'])
                request.user.save()
                userprofile.save()
                auth.login(request,request.user)
                messages.success(request,'Your data has been saved ')
        else:
            messages.error(request,'check your value and elements')    
        return redirect('profile')
    else:
        if request.user is not None:
            context=None
            if not request.user.is_anonymous:
                userprofile=UserProfile.objects.get(user=request.user)
                context = {
                    'fname':request.user.first_name,
                    'lname':request.user.last_name,
                    'address':userprofile.address,
                    'address2':userprofile.address2,
                    'city':userprofile.city,
                    'state':userprofile.state,
                    'zip_number':userprofile.zip_number,
                    'email':request.user.email,
                    'user':request.user.username,
                    'pass':request.user.password,
                }
            return render(request,'accounts/profile.html',context)
        else:
            return redirect('profile')


def product_favorites(request,pro_id):
    if request.user.is_authenticated and  not request.user.is_anonymous:
        pro_fav = Product.objects.get(pk=pro_id)
        if UserProfile.objects.filter(user=request.user,product_favorites=pro_fav).exists():
            messages.success(request,'Alreedy product in the favorite list')
        else:   
            userprofile=UserProfile.objects.get(user=request.user)
            userprofile.product_favorites.add(pro_fav)
            messages.success(request,'product has been favorited')
    else:
        messages.error('you must be logged in')
    return redirect('/products/'+str(pro_id))
            
def show_product_favorites(request):
    context=None
    if request.user.is_authenticated and  not request.user.is_anonymous:
        proInfo=UserProfile.objects.get(user=request.user)
        pro= proInfo.product_favorites.all()
        context = {'Product':pro}
    return render(request,'products/products.html',context)


