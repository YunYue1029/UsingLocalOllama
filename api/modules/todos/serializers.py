from rest_framework import serializers
from .models import Todo, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color']

class TodoSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        write_only=True, 
        source='tags',
        queryset=Tag.objects.all(),
        required=False
    )
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Todo
        fields = [
            'id', 'title', 'description', 'created_at', 'updated_at',
            'due_date', 'priority', 'priority_display', 'status',
            'status_display', 'tags', 'tag_ids', 'completed'
        ]
        read_only_fields = ['created_at', 'updated_at']
