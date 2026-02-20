from django.shortcuts import render
from .models import Contact,User
# Create your views here.
def index(request):
    return render(request,'index.html')
def contact(request):
    if request.method == 'POST':
        Contact.objects.create(
        name=request.POST['name'],
        email=request.POST['email'],
        mobile=request.POST['mobile'],
        remark=request.POST['remark']
        )
        msg="Contact saved successfully"
        contact=Contact.objects.all().order_by('-id')[:3]
        return render(request,'contact.html',{'msg':msg,'contact':contact})
    else:
        contact=Contact.objects.all().order_by('-id')[:3]
        return render(request,'contact.html',{'contact':contact})

def signup(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg="Email already exist"
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['c_password']:
                User.objects.create(
                fname=request.POST['fname'],
                lname=request.POST['lname'],
                mobile=request.POST['mobile'],
                email=request.POST['email'],
                address=request.POST['address'],
                password=request.POST['password']
                )
                msg="Signup Successfully"
                return render(request,'signup.html',{'msg':msg})
            else:
                msg="Password and Confirm Password does not match"
                return render(request,'signup.html',{'msg':msg})
    else:
        return render(request,'signup.html')
        
def login(request):
    if request.method == 'POST':
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password==request.POST['password']:
                request.session['email']=user.email
                request.session['fname']=user.fname
                return render(request,'index.html')
            else:
                msg="Invalid password"
                return render(request,'login.html',{'msg':msg})
        except:
            msg="Email does not exist"
            return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'login.html')
def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        msg="Logout Successfully"
        return render(request,'login.html',{'msg':msg})
    except: 
        msg="Logout Successfully"
        return render(request,'login.html',{'msg':msg})
def change_password(request):
    if request.method == 'POST':
        user=User.objects.get(email=request.session['email'])
        if user.password==request.POST['password']:
            if request.POST['new_password']==request.POST['c_new_password']:
                if user.password!=request.POST['new_password']:
                    user.password=request.POST['new_password']
                    user.save()
                    del request.session['email']
                    del request.session['fname']
                    msg="Password Changed Successfully.Please login again"
                    return render(request,'login.html',{'msg':msg})
                else:
                    msg="New Password Can't Be From Old Password"
                    return render(request,'change_password.html',{'msg':msg})
            else:
                msg="New Password & Confirm New Password does not match "
                return render(request,'change_password.html',{'msg':msg})
        else:
            msg="Invalid Old Password"
            return render(request,'change_password.html',{'msg':msg})
    else:
        return render(request,'change_password.html')
def profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method == 'POST':
        user.fname=request.POST['fname']
        user.lname=request.POST['lname']
        user.mobile=request.POST['mobile']
        user.address=request.POST['address']
        user.save()
        request.session['fname']=user.fname
        msg="Profile Updated Successfully"
        return render(request,'profile.html',{'msg':msg,'user':user})
    return render(request,'profile.html',{'user':user})