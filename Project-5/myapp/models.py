from django.db import models
from django.utils import timezone
# Create your models here.
class User(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone=models.PositiveBigIntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics/')
    usertype=models.CharField(max_length=100,default='buyer')

    def __str__(self):
        return self.fname + ' ' + self.lname

class Product(models.Model):
    chategory=(
        ("Laptop","Laptop"),  
        ("Mobile","Mobile"),
        ("Headphones","Headphones"),
        ("Smart Watch","Smart Watch"),
    )
    seller=models.ForeignKey(User,on_delete=models.CASCADE)
    Product_category=models.CharField(max_length=100,choices=chategory)
    Product_name=models.CharField(max_length=100)
    Product_price=models.PositiveIntegerField()
    Product_desc=models.TextField()
    Product_image=models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.seller.fname + ' - ' + self.Product_name
    
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.fname + ' - ' + self.product.Product_name
