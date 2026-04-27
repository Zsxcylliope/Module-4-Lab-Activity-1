from django.contrib import admin
from .models import StudentRecord, CourseClass, GradingTimeframe, Grade

admin.site.register(StudentRecord)
admin.site.register(CourseClass)
admin.site.register(GradingTimeframe)
admin.site.register(Grade)
