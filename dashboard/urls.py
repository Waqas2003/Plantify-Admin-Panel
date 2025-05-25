# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # Plants
    path('plants/', views.plant_list, name='plant-list'),
    # path('plants/<str:plant_id>/', views.plant_detail, name='plant-detail'),
    path('plants/create/', views.plant_create, name='plant-create'),
    path('plants/<str:plant_id>/edit/', views.plant_update, name='plant-update'),
    path('plants/<str:plant_id>/delete/', views.plant_delete, name='plant-delete'),

    # Users
    path('users/', views.user_list, name='user-list'),
    path('users/create/', views.user_create, name='user-create'),
    path('users/<str:user_email>/edit/', views.user_update, name='user-update'),
    path('users/<str:user_email>/delete/', views.user_delete, name='user-delete'),
    path('users/<str:user_email>/block/', views.user_block, name='user-block'),
    path('users/<str:user_email>/unblock/', views.user_unblock, name='user-unblock'),


    # User Plants
    path('user-plants/', views.user_plant_list, name='user-plant-list'),
    path('user-plants/create/', views.user_plant_create, name='user-plant-create'),
    path('user-plants/update/<str:user_email>/', views.user_plant_update, name='user-plant-update'),
    path('user-plants/delete/<str:user_email>/', views.user_plant_delete, name='user-plant-delete'),

    
    # Communities
    # path('communities/', views.community_list, name='community-list'),
    # path('communities/<str:community_id>/', views.community_detail, name='community-detail'),

 # Community URLs
    path('communities/', views.community_list, name='community-list'),
    path('communities/create/', views.community_create, name='community-create'),
    path('communities/<str:community_id>/edit/', views.community_update, name='community-update'),
    path('communities/<str:community_id>/delete/', views.community_delete, name='community-delete'),
    path('communities/<str:community_id>/', views.community_detail, name='community-detail'),
    path('communities/<str:community_id>/add-member/', views.add_member, name='add-member'),
    path('communities/<str:community_id>/block-member/', views.block_member, name='block-member'),
    path('communities/<str:community_id>/unblock-user/', views.unblock_user, name='unblock-user'),
    path('communities/<str:community_id>/remove-member/', views.remove_member, name='remove-member'),
    path('communities/<str:community_id>/unblock/', views.unblock_community, name='unblock-community'),
    path('communities/<str:community_id>/block/', views.block_community, name='block-community'),
    # Member Management
    # path('<str:community_id>/members/', views.community_members, name='community-members'),
    # path('<str:community_id>/members/add/', views.add_member, name='add-member'),
    # path('<str:community_id>/members/<str:user_id>/remove/', views.remove_member, name='remove-member'),
    
    # Banned Users
    # path('<str:community_id>/banned-users/', views.banned_users_list, name='banned-users'),
    # path('<str:community_id>/ban-user/<str:user_id>/', views.ban_user, name='ban-user'),
    # path('<str:community_id>/unban-user/<str:user_id>/', views.unban_user, name='unban-user'),

    
    
    
    # Diseases
    path('diseases/', views.disease_list, name='disease-list'),
    path('diseases/add/', views.disease_create, name='disease-create'),
    path('diseases/<str:disease_id>/edit/', views.disease_update, name='disease-update'),
    path('diseases/<str:disease_id>/delete/', views.disease_delete, name='disease-delete'),

    # path('diseases/', views.disease_list, name='disease-list'),
    # path('diseases/<str:disease_id>/', views.disease_detail, name='disease-detail'),
]