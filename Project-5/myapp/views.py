from django.shortcuts import render
from .models import User

# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    if request.method =='POST':
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password==request.POST['password']:
                request.session['email']=user.email
                request.session['name']=user.fname
                request.session['profile_pic']=user.profile_pic.url
                if user.usertype=="buyer":
                    return render(request,'index.html')
                else:
                    return render(request,'seller_index.html',{'user':user})
            else:
                msg='Invalid password'
                return render(request,'login.html',{'msg':msg})
        except Exception as e:
            print(e)
            msg='Email Not registered'
            return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'login.html')
def signup(request):
    if request.method == 'POST':
        try:
            User.objects.get(email=request.POST['email'])
            msg='Email already exists'
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['c_password']:
                User.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    address=request.POST['address'],
                    phone=request.POST['phone'],
                    email=request.POST['email'],
                    password=request.POST['password'],
                    profile_pic=request.FILES['profile_pic'],
                    usertype=request.POST['user_type'],
                )
                msg="signup successful"
                return render(request,'login.html',{'msg':msg})
            else:
                msg="password and confirm password does not match"
                return render(request,'signup.html',{'msg':msg})
    else:
        return render(request,'signup.html')
def logout(request):
    try:
        del request.session['email']
        del request.session['name']
        del request.session['profile_pic']
        msg='Logout successful'
    except:
        msg='Logout successful'
    return render(request,'login.html',{'msg':msg})
def contact(request):
    return render(request,'contact.html',)
def forgot_password(request):
    return render(request,'forgot_password.html',)
def profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=='POST':
        user.fname=request.POST['fname']
        user.lname=request.POST['lname']
        user.address=request.POST['address']   
        user.phone=request.POST['phone']
        try:
            user.profile_pic=request.FILES['profile_pic']
        except:
            pass
        user.save()
        request.session['profile_pic']=user.profile_pic.url
        msg="Profile updated successfully"
        return render(request,'profile.html',{'user':user,'msg':msg})
    else:
        return render(request,'profile.html',{'user':user})
def otp(request):
    return render(request,'otp.html',)
def change_password(request):
    return render(request,'change_password.html',)
def seller_index(request):
    return render(request,'seller_index.html',)
def add_product(request):
    return render(request,'add_product.html',)
def products(request):
    return render(request,'products.html',)
def orders(request):
    return render(request,'orders.html',)
def seller_profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=='POST':
        user.fname=request.POST['fname']
        user.lname=request.POST['lname']
        user.address=request.POST['address']   
        user.phone=request.POST['phone']
        try:
            user.profile_pic=request.FILES['profile_pic']
        except:
            pass
        user.save()
        request.session['profile_pic']=user.profile_pic.url
        msg="Profile updated successfully"
        return render(request,'seller_profile.html',{'user':user,'msg':msg})
    else:
        return render(request,'seller_profile.html',{'user':user})
