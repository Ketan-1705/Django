from django.db import models

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