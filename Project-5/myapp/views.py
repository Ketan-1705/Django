
from django.shortcuts import render,redirect
from .models import User,Product,Wishlist,Cart
import random
from django.core.mail import send_mail
from django.conf import settings
import requests
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import stripe

YOUR_DOMAIN = 'http://localhost:8000'
stripe.api_key = settings.STRIPE_PRIVATE_KEY

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
                    wishlist=Wishlist.objects.filter(user=user)
                    request.session['wishlist_count']=len(wishlist)
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
        del request.session['wishlist_count']
        del request.session['cart_count']
        msg='Logout successful'
    except:
        msg='Logout successful'
    return render(request,'login.html',{'msg':msg})
def contact(request):
    return render(request,'contact.html',)
def forgot_password(request):
    if request.method=='POST':
        try:
            user=User.objects.get(email=request.POST['email'])
            otp=random.randint(100000,999999)
            subject='Forgot Password OTP'
            message='Your OTP is :' +str(otp)
            send_mail(subject,message,settings.EMAIL_HOST_USER,[user.email,])
            request.session['otp']=otp
            request.session['email2']=user.email
            return render(request,'otp.html')
        except:
            msg='Email Not Found'
            return render(request,'forgot_password.html',{'msg':msg})
    else:
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
    otp1=int(request.POST['otp'])
    otp2=request.session['otp']
    if otp1==otp2:
        msg='OTP verified successfully..'
        return render(request,'new_password.html',{'msg':msg})
    else:
        msg='OTP verified successfully..'
        return render(request,'otp.html',{'msg':msg})
def new_password(request):
    if request.POST['new_password']==request.POST['c_new_password']:
        user=User.objects.get(email=request.session['email2'])
        if user.password!=request.POST['new_password']:
            user.password=request.POST['new_password']
            user.save()
            del request.session['email2']
            msg='Your password change successfully Please login again..'
            return render(request,'login.html',{'msg':msg})
        else:
            msg='New Password and Courent Password Both are Same'
            return render(request,'new_password.html',{'msg':msg})
    else:
        msg="New password and conform New password Both are same..."
        return render(request,'new_password.html')
def change_password(request):
    if request.method=='POST':
        user=User.objects.get(email=request.session['email'])
        if user.password==request.POST['old_password']:
            if request.POST['new_password']==request.POST['c_new_passwoed']:
                if user.password!=request.POST['new_password']:
                    user.password=request.POST['new_password']
                    user.save()
                    del request.session['email']
                    
                    msg='Password Changed Successfully.Please login again..'
                    return render(request,'login.html',{'msg':msg})
                else:
                    msg='New Password and Courent Password Both are Same'
                    return render(request,'change_password.html',{'msg':msg})
            else:
                msg='Password And Conform Password does not match...'
                return render(request,'change_password.html',{'msg':msg})
        else:
            msg='Invalid Old Password..'
            return render(request,'change_password.html',{'msg':msg})
    else:
        return render(request,'change_password.html')
    
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
def orders(request,pid):
    products=Product.objects.get(id=pid)
    user=User.objects.get(email=request.session['email'])
    Wishlist.objects.create(user=user,product=products)
    return render(request, 'orders.html')

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
    wishlist_flag = False
    cart_flag=False
    product=Product.objects.get(id=pid)
    user=User.objects.get(email=request.session['email'])
    try:
        Wishlist.objects.get(user=user,product=product)
        wishlist_flag = True
    except:
        pass
    try:
        Cart.objects.get(user=user,product=product)
        cart_flag = True
    except:
        pass
    return render(request,'buy_view_products.html',{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})

    

def add_to_wishlist(request,pid):
    products=Product.objects.get(id=pid)
    user=User.objects.get(email=request.session['email'])
    Wishlist.objects.create(user=user,product=products)
    return redirect('wishlist')
def wishlist(request):
    user=User.objects.get(email=request.session['email'])
    wishlist_items=Wishlist.objects.filter(user=user)
    request.session['wishlist_count']=len(wishlist_items)
    return render(request,'wishlist.html',{'wishlist_items':wishlist_items})
def remove_from_wishlist(request,pid):
    product=Product.objects.get(id=pid)
    user=User.objects.get(email=request.session['email'])
    wishlist=Wishlist.objects.get(user=user,product=product)
    wishlist.delete()
    return redirect('wishlist')
def add_to_cart(request,pid):
    products=Product.objects.get(id=pid)
    user=User.objects.get(email=request.session['email'])
    Cart.objects.create(
        user=user,
        product=products,
        Product_price=products.Product_price,
        total_price=products.Product_price,
        product_qty=1,
        payment_status=False)
    return redirect('cart')
def cart(request):
    net_price=0
    user=User.objects.get(email=request.session['email'])
    cart_items=Cart.objects.filter(user=user)
    request.session['cart_count']=len(cart_items)
    for i in cart_items:
        net_price=net_price+i.total_price
    return render(request,'cart.html',{'cart_items':cart_items,'net_price':net_price})
def remove_from_cart(request,pid):
    product=Product.objects.get(id=pid)
    user=User.objects.get(email=request.session['email'])
    cart=Cart.objects.get(user=user,product=product)
    cart.delete()
    return redirect('cart')
def change_qty(request):
    pid=int(request.POST['id'])
    product_qty=int(request.POST['product_qty'])
    cart=Cart.objects.get(pk=pid)
    cart.product_qty=product_qty
    cart.total_price=cart.Product_price*product_qty
    cart.save()
    return redirect('cart')
@csrf_exempt
def create_checkout_session(request):
	amount = int(json.load(request)['post_data'])
	final_amount=amount*100
	user=User.objects.get(email=request.session['email'])
	user_name=f"{user.fname} {user.lname}"
	user_address=f"{user.address}"
	user_mobile=f"{user.phone}"
	session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'price_data': {
				'currency': 'inr',
				'unit_amount': final_amount,
				'product_data': {
					'name': 'Checkout Session Data',
					'description':f'''Customer:{user_name},\n\n
					Address:{user_address},\n
					Mobile:{user_mobile}''',
				},
			},
			'quantity': 1,
			}],
		mode='payment',
		success_url=YOUR_DOMAIN + '/success.html',
		cancel_url=YOUR_DOMAIN + '/cancel.html',
		customer_email=user.email,
		shipping_address_collection={
			'allowed_countries':['IN'],
		}
		)
	return JsonResponse({'id': session.id})

def success(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=False)
	for i in carts:
		i.payment_status=True
		i.save()
	carts=Cart.objects.filter(user=user,payment_status=False)
	request.session['cart_count']=len(carts)
	return render(request,'success.html')

def cancel(request):
	return render(request,'cancel.html')
def myorder(request):
    user=User.objects.get(email=request.session['email'])
    orders=Cart.objects.filter(user=user,payment_status=True)
    return render(request,'myorder.html',{'orders':orders})