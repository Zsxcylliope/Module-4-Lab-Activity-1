from rest_framework import serializers
from .models import StudentRecord, CourseClass, GradingTimeframe, Grade

class StudentRecordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='owner.email', read_only=True)
    enrolled_subjects = serializers.StringRelatedField(many=True, source='enrolled_classes', read_only=True)

    class Meta:
        model = StudentRecord
        fields = ['id', 'owner', 'full_name', 'course', 'year_level', 'contact_number', 'email', 'enrolled_subjects']

class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='owner.email')

    class Meta:
        model = StudentRecord
        fields = ['contact_number', 'email']

    def update(self, instance, validated_data):
        owner_data = validated_data.pop('owner', {})
        if 'email' in owner_data:
            instance.owner.email = owner_data['email']
            instance.owner.save()
        
        instance.contact_number = validated_data.get('contact_number', instance.contact_number)
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class CourseClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseClass
        fields = '__all__'

class GradingTimeframeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradingTimeframe
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'