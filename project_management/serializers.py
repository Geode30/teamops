from django.utils import timezone

from rest_framework import serializers

from project_management.models import Project, Task, ProgressNote

class ProjectSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['created_by', 'date_completed']

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Deadline cannot be in the past")
        
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

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_full_name = serializers.ReadOnlyField(source='assigned_to.full_name')
    created_by_full_name = serializers.ReadOnlyField(source='created_by.full_name')
    
    class Meta:
        fields = "__all__"
        model = Task
        read_only_fields = ['created_by', 'date_completed']

    def validate(self, data):
        if data.get('project'):
            project:Project = data["project"]

            if project.date_completed:
                raise serializers.ValidationError({
                    "message": "Cannot assign task to a completed project"
                }) 

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)
    
class ProgressNoteSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.filter(date_deleted__isnull=True))
    created_by_full_name = serializers.ReadOnlyField(source='created_by.full_name')

    class Meta:
        fields = "__all__"
        model = ProgressNote
        read_only_fields = ['created_by']

    def validate(self, data):
        project:Project = data["task"].project

        if project.date_completed:
            raise serializers.ValidationError({
                "message": "Cannot add a note to a completed project"
            }) 

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)