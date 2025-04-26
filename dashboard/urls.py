# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # Plants
    path('plants/', views.plant_list, name='plant-list'),
    path('plants/<str:plant_id>/', views.plant_detail, name='plant-detail'),
    
    # Users
    path('users/', views.user_list, name='user-list'),
    path('users/<str:user_email>/', views.user_detail, name='user-detail'),
    
    # User Plants
    path('user-plants/', views.user_plant_list, name='user-plant-list'),
    path('user-plants/<str:plant_id>/', views.user_plant_detail, name='user-plant-detail'),
    
    # Communities
    path('communities/', views.community_list, name='community-list'),
    path('communities/<str:community_id>/', views.community_detail, name='community-detail'),
    
    # Diseases
    path('diseases/', views.disease_list, name='disease-list'),
    path('diseases/<str:disease_id>/', views.disease_detail, name='disease-detail'),
]