from django.urls import path, include

urlpatterns = [
    path('calculator/', include('api.modules.calculator.urls')),
    path('todos/', include('api.modules.todos.urls')),
] 