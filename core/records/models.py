from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class StudentRecord(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    course = models.CharField(max_length=50)
    year_level = models.IntegerField()
    contact_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.full_name

class CourseClass(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_classes')
    students = models.ManyToManyField(StudentRecord, related_name='enrolled_classes')

    def __str__(self):
        return self.name

class GradingTimeframe(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    @classmethod
    def is_currently_open(cls):
        now = timezone.now()
        return cls.objects.filter(start_date__lte=now, end_date__gte=now).exists()

    def __str__(self):
        return self.name

class Grade(models.Model):
    student = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='grades')
    course_class = models.ForeignKey(CourseClass, on_delete=models.CASCADE)
    grade = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.student.full_name} - {self.course_class.name}: {self.grade}"