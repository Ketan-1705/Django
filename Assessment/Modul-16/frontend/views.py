from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from api.models import Course, Student, UserProfile

def index(request):
    total_courses = Course.objects.count()
    total_students = Student.objects.count()
    recent_courses = Course.objects.order_by('-created_at')[:3]
    return render(request, 'index.html', {
        'total_courses': total_courses,
        'total_students': total_students,
        'recent_courses': recent_courses
    })

def courses_list(request):
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'courses.html', {'courses': courses})

def students_list(request):
    students = Student.objects.all().order_by('last_name', 'first_name')
    return render(request, 'students.html', {'students': students})

@login_required
def add_course(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'faculty':
        return redirect('courses_list')
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:
            Course.objects.create(title=title, description=description)
            return redirect('courses_list')
    return render(request, 'add_course.html')

@login_required
def delete_course(request, course_id):
    if hasattr(request.user, 'profile') and request.user.profile.role == 'faculty':
        course = get_object_or_404(Course, id=course_id)
        course.delete()
    return redirect('courses_list')

@login_required
def enroll_course(request, course_id):
    if hasattr(request.user, 'profile') and request.user.profile.role == 'student':
        course = get_object_or_404(Course, id=course_id)
        if hasattr(request.user, 'student_record'):
            student = request.user.student_record
            student.courses.add(course)
    return redirect('courses_list')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            UserProfile.objects.create(user=user, role=role)
            if role == 'student':
                Student.objects.create(user=user, first_name=first_name, last_name=last_name, email=email)
            login(request, user)
            return redirect('index')
    return render(request, 'signup.html')

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error = "Invalid credentials"
    return render(request, 'login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('index')
