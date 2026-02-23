from django.db import models

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.PositiveIntegerField()
    message=models.TextField()

    def __str__(self):
        return self.name
class User(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.PositiveIntegerField()
    address=models.TextField()
    password=models.CharField(max_length=100)

    def __str__(self):
        return self.name