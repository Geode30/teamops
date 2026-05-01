from django.utils import timezone

from rest_framework import serializers

from project_management.models import Project
from project_management.utils import manila_to_utc

class ProjectSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['created_by', 'date_completed']

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError({
                "message": "Deadline cannot be in the past"
            })
        
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)
    
    def get_created_by_name(self, obj):
        return f"{obj.created_by.last_name}, {obj.created_by.first_name}"
    
class ProjectIDandNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name"]