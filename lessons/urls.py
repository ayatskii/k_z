from django.urls import path
from . import views

urlpatterns = [
    path('', views.lesson_list, name='lesson_list'),
    path('<slug:slug>/', views.lesson_detail, name='lesson_detail'),
    path('<slug:slug>/test/', views.lesson_test, name='lesson_test'),
    path('<slug:slug>/test/submit/', views.submit_test, name='submit_test'),
    path('<slug:slug>/save/', views.save_lesson, name='save_lesson'),
]
 