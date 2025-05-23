from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('change-theme/<str:theme_name>/', views.change_theme, name='change_theme'),
] 