from django.shortcuts import render,redirect
from .models import User,Product,Wishlist

# Create your views here.
def index(request):
    try:
        user=User.objects.get(email=request.session['email'])
        
        if user.usertype=="buyer":   
            return render(request,'index.html')
        else:
            seller = User.objects.get(email=request.session['email'])
            product_count = Product.objects.filter(seller=seller).count()

            return render(request, 'seller_index.html', {
            'product_count': product_count
    })

    except:
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
                    return render(request,'seller_index.html')
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
    try:
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
        if user.usertype=="buyer":
            return render(request,'profile.html',{'user':user,'msg':msg})
        else:
            return render(request,'seller_profile.html',{'user':user,'msg':msg})
    except:
        return render(request,'index.html')
def otp(request):
    return render(request,'otp.html',)
def change_password(request):
    return render(request,'change_password.html',)
def seller_index(request):
    user = User.objects.get(email=request.session['email'])
    return render(request,'seller_index.html',{'user':user})
def add_product(request):
    seller=User.objects.get(email=request.session['email'])
    if request.method=='POST':
        Product.objects.create(
            seller=seller,
            Product_name=request.POST['Product_name'],
            Product_category=request.POST['Product_category'],
            Product_price=request.POST['Product_price'],
            Product_desc=request.POST['Product_desc'],
            Product_image=request.FILES['Product_image'],
            # sstock=request.POST['stock'],
        )
        msg='Product added successfully'
        return render(request,'add_product.html',{'msg':msg})
    else:
        return render(request,'add_product.html')
def products(request):
    seller=User.objects.get(email=request.session['email'])
    products=Product.objects.filter(seller=seller)
    return render(request,'products.html',{'products':products})
def orders(request):
    return render(request,'orders.html',)
def view_product(request,pid):
    product=Product.objects.get(id=pid)
    return render(request,'view_product.html',{'product':product})
def delete_product(request,pid):
    seller = User.objects.get(email=request.session['email'])
    product = Product.objects.get(id=pid, seller=seller)
    product.delete()
    
    return redirect('products')
def edit_product(request,pid):
    products=Product.objects.get(id=pid)
    if request.method=='POST':
        products.Product_name=request.POST['Product_name']
        products.Product_category=request.POST['Product_category']
        products.Product_price=request.POST['Product_price']
        products.Product_desc=request.POST['Product_desc']
        try:
            products.Product_image=request.FILES['Product_image']
        except:
            pass
        products.save()
        msg='Product updated successfully'
        return render(request,'edit_product.html',{'products':products,'msg':msg})
    return render(request,'edit_product.html',{'products':products})
def all_products(request):
    products=Product.objects.all()
    return render(request,'all_product.html',{'products':products})

def buy_view_products(request,pid):
    product=Product.objects.get(id=pid)
    return render(request,'buy_view_products.html',{'product':product})
# def add_to_cart(request,pid):
#     return redirect('buy_view_products',id=pid)
def add_to_wishlist(request,pid):
    products=Product.objects.get(id=pid)
    user=User.objects.get(email=request.session['email'])
    Wishlist.objects.create(user=user,product=products)
    return render(request,'index.html')
def wishlist(request):
    user=User.objects.get(email=request.session['email'])
    wishlist_items=Wishlist.objects.filter(user=user)
    return render(request,'wishlist.html',{'wishlist_items':wishlist_items})