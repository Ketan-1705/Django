from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.courses_list, name='courses_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('students/', views.students_list, name='students_list'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
