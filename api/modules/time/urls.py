from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_current_time, name='get_current_time'),
] 