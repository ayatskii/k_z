from django.urls import path
from . import views

urlpatterns = [
    path('', views.dictionary_home, name='dictionary_home'),
    path('search/', views.search_word, name='search_word'),
    path('word/<int:word_id>/', views.word_detail, name='word_detail'),
    path('word/<int:word_id>/save/', views.save_word, name='save_word'),
    path('word/<int:word_id>/remove/', views.remove_saved_word, name='remove_saved_word'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
] 