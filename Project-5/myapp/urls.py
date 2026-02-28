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
    path('view_product/<int:pid>/',views.view_product,name='view_product'),
    path('edit_product/<int:pid>/',views.edit_product,name='edit_product'),
    path('delete_product/<int:pid>/',views.delete_product,name='delete_product'),
    path('all_product/',views.all_products,name='all_product'),
    path('buy_view_products/<int:pid>/',views.buy_view_products,name='buy_view_products'),
    # path('add_to_cart/<int:pid>/',views.add_to_cart,name='add_to_cart'),
    path('add_to_wishlist/<int:pid>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('wishlist/',views.wishlist,name='wishlist'),
    ]
