from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from .models import Todo, Tag
from .serializers import TodoSerializer, TagSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    
    def get_queryset(self):
        queryset = Todo.objects.all()
        
        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
            
        # Filter by priority
        priority = self.request.query_params.get('priority', None)
        if priority:
            queryset = queryset.filter(priority=priority)
            
        # Filter by tag
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(tags__name=tag)
            
        # Search in title and description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
            
        # Filter by due date
        due_before = self.request.query_params.get('due_before', None)
        if due_before:
            queryset = queryset.filter(due_date__lte=due_before)
            
        return queryset.order_by('-priority', 'due_date', '-created_at')
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        todo = self.get_object()
        if todo.status == 'completed':
            todo.status = 'pending'
        else:
            todo.status = 'completed'
        todo.save()
        return Response(TodoSerializer(todo).data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        todos = Todo.objects.filter(
            due_date__lt=timezone.now(),
            status__in=['pending', 'in_progress']
        )
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        today = timezone.now().date()
        todos = Todo.objects.filter(due_date__date=today)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
