from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_donor, name='register'),
    path('search/', views.search_donor, name='search'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('request-blood/', views.request_blood, name='request_blood'),
    path('approve/<int:pk>/', views.approve_request, name='approve_request'),
    path('register-user/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
]