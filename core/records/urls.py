from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentRecordViewSet, CourseClassViewSet, GradingTimeframeViewSet, GradeViewSet, ChangePasswordView

router = DefaultRouter()
router.register(r'student-records', StudentRecordViewSet, basename='studentrecord')
router.register(r'classes', CourseClassViewSet, basename='courseclass')
router.register(r'timeframes', GradingTimeframeViewSet, basename='gradingtimeframe')
router.register(r'grades', GradeViewSet, basename='grade')

urlpatterns = [
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('', include(router.urls)),
]