from rest_framework import serializers
from .models import Course, Student

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    # Depending on requirements, we can embed course details or just use PrimaryKeyRelatedField.
    # The default for ManyToMany is a list of Primary Keys.
    # To provide more detail on read, we could nest them, but we'll keep it simple:
    
    class Meta:
        model = Student
        fields = '__all__'
