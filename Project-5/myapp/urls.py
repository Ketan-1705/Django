from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('contact/',views.contact,name='contact'),
    path('logout/',views.logout,name='logout'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('otp/',views.otp,name='otp'),
    path('profile/',views.profile,name='profile'),
    path('change_password/',views.change_password,name='change_password'),
    path('seller_index/',views.seller_index,name='seller_index'),
    path('add_product/',views.add_product,name='add_product'),
    path('products/',views.products,name='products'),
    path('orders/',views.orders,name='orders'),
    path('seller_profile/',views.seller_profile,name='seller_profile'),
]
