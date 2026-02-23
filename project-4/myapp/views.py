from django.shortcuts import render
from .models import Contact,User
from django.core.mail import send_mail
from django.conf import settings
import random
# Create your views here.
def index(request):
    return render(request,'index.html')
def contact(request):
    if request.method == 'POST':
        Contact.objects.create(
        name=request.POST['name'],
        email=request.POST['email'],
        phone=request.POST['phone'],
        message=request.POST['message']
        )
        msg = 'Your message has been sent successfully'
        contact=Contact.objects.all().order_by('-id')[:3]
        return render(request,'contact.html',{'msg':msg,'contact':contact})
    else:
        contact=Contact.objects.all().order_by('-id')[:3]
        return render(request,'contact.html',{'contact':contact})
def signup(request):
    if request.method == 'POST':
        try:
            User.objects.get(email=request.POST['email'])
            msg  = 'Email already exists'
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password'] == request.POST['c_password']:
                User.objects.create(
                    name=request.POST['name'],
                    email=request.POST['email'],
                    phone=request.POST['phone'],
                    password=request.POST['password'],
                    address=request.POST['address']
                    )
                msg = 'Your account has been created successfully'
                return render(request,'signup.html',{'msg':msg})
            else:
                msg = 'Password and confirm password does not match'
                return render(request,'signup.html',{'msg':msg})
    else:
        return render(request,'signup.html')
def login(request):
    if request.method == 'POST':
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password == request.POST['password']:
                request.session['email']=user.email
                request.session['name']=user.name
                return render(request,'index.html')
            else:
                msg = 'Invalid password'
                return render(request,'login.html',{'msg':msg})
        except:
            msg = 'Email does not exist'
            return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'login.html')

def change_password(request):
    if request.method == 'POST':
        user=User.objects.get(email=request.session['email'])
        if user.password == request.POST['old_password']:
            if request.POST['new_password']==request.POST['cn_password']:
                if user.password != request.POST['new_password']:
                    user.password=request.POST['new_password']
                    user.save()
                    del request.session['email']
                    del request.session['name']
                    msg = 'Your password has been changed successfully please login again'
                    return render(request,'login.html',{'msg':msg})
                else:
                    msg = 'Your current password and new password should not be same'
                    return render(request,'change_password.html',{'msg':msg})
            else:
                msg = 'New password and confirm new password does not match'
                return render(request,'change_password.html',{'msg':msg})
        else:
            msg = 'Invalid old password'
            return render(request,'change_password.html',{'msg':msg})
    else:
        return render(request,'change_password.html')
    
def profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method == 'POST':
        user.name=request.POST['name']
        user.phone=request.POST['phone']
        user.address=request.POST['address']
        user.save()
        request.session['name']=user.name
        msg = 'Your profile has been updated successfully'
        return render(request,'profile.html',{'msg':msg,'user':user})
    else:
        return render(request,'profile.html',{'user':user})
def logout(request):
    try:
        del request.session['email']
        del request.session['name']
        msg = 'You have been logged out successfully'
        return render(request,'login.html',{'msg':msg})
    except:
        msg = 'You have been logged out successfully'
        return render(request,'login.html',{'msg':msg})
def forgot_password(request):
    if request.method == 'POST':
        try:
            user=User.objects.get(email=request.POST['email'])
            otp=random.randint(1000,9999)
            subject = 'Forgot Password OTP'
            message = 'Your OTP for forgot password is' +str(otp)
            send_mail (subject,message,settings.EMAIL_HOST_USER,[user.email,])
            request.session['otp']=otp
            request.session['email2']=user.email
            return render(request,'otp.html')
        except:
            msg = 'Email does not exist'
            return render(request,'forgot_password.html',{'msg':msg})
    else:
         return render(request,'forgot_password.html')
def otp(request):
    otp1=int (request.POST['otp'])
    otp2=request.session['otp']
    if otp1 == otp2:
        del request.session['otp']
        msg = 'OTP verified successfully'
        return render(request,'new_password.html',{'msg':msg})
    else:
        msg = 'Invalid OTP'
        return render(request,'otp.html',{'msg':msg})
def new_password(request):
    if request.POST['new_password'] == request.POST['cn_password']:
        user=User.objects.get(email=request.session['email2'])
        if user.password != request.POST['new_password']:
            user.password=request.POST['new_password']
            user.save()
            del request.session['email2']
            msg = 'Your password has been changed successfully please login again'
            return render(request,'login.html',{'msg':msg})
        else:
            msg = 'Your current password and new password should not be same'
            return render(request,'new_password.html',{'msg':msg})
    else:
        msg = 'New password and confirm new password does not match'
        return render(request,'new_password.html',{'msg':msg})