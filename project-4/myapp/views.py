from django.shortcuts import render
from .models import Contact
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
    return render(request,'signup.html')
def login(request):
    return render(request,'login.html')