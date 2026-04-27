from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated
from .models import StudentRecord, CourseClass, GradingTimeframe, Grade
from .serializers import (StudentRecordSerializer, CourseClassSerializer, 
                          GradingTimeframeSerializer, GradeSerializer,
                          StudentProfileUpdateSerializer, ChangePasswordSerializer)

class IsAdminOrFaculty(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name__in=['Admin', 'Faculty']).exists()

class IsAssignedFaculty(BasePermission):
    """Allows access only to faculty assigned to the specific class."""
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'course_class'):
            return obj.course_class.faculty == request.user
        return False

class IsGradingPeriodOpen(BasePermission):
    """Prevents grading operations if outside allowed timeframes."""
    message = "The grading timeframe is currently closed."

    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH']:
            return GradingTimeframe.is_currently_open()
        return True

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.validated_data['old_password']):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentRecordViewSet(ModelViewSet):
    def get_serializer_class(self):
        user = self.request.user
        if self.action in ['update', 'partial_update'] and user.groups.filter(name='Student').exists():
            return StudentProfileUpdateSerializer
        return StudentRecordSerializer

    def get_queryset(self):
        user = self.request.user
        # Admins can see all records
        if user.is_staff or user.is_superuser or user.groups.filter(name='Admin').exists():
            return StudentRecord.objects.all()
        # Faculty can see students in their classes
        if user.groups.filter(name='Faculty').exists():
            return StudentRecord.objects.filter(enrolled_classes__faculty=user).distinct()
        # Students can only see their own records
        if user.is_authenticated:
            return StudentRecord.objects.filter(owner=user)
        return StudentRecord.objects.none()

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class CourseClassViewSet(ModelViewSet):
    serializer_class = CourseClassSerializer
    queryset = CourseClass.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAdminOrFaculty]
        return [permission() for permission in permission_classes]

class GradingTimeframeViewSet(ModelViewSet):
    serializer_class = GradingTimeframeSerializer
    queryset = GradingTimeframe.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAdminOrFaculty]
        return [permission() for permission in permission_classes]

class GradeViewSet(ModelViewSet):
    serializer_class = GradeSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Faculty').exists():
            return Grade.objects.filter(course_class__faculty=user)
        if user.is_staff or user.is_superuser or user.groups.filter(name='Admin').exists():
            return Grade.objects.all()
        if user.is_authenticated:
            return Grade.objects.filter(student__owner=user)
        return Grade.objects.none()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsAssignedFaculty, IsGradingPeriodOpen]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]