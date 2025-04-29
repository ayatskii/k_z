from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('saved-words/', views.saved_words, name='saved_words'),
    path('saved-words/remove/<int:word_id>/', views.remove_saved_word, name='remove_saved_word'),
    path('progress/', views.user_progress, name='user_progress'),
    path('theme/<str:theme>/', views.change_theme, name='change_theme'),
] 