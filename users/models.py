from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    
    THEME_CHOICES = [
        ('light', _('Light Theme')),
        ('dark', _('Dark Theme')),
    ]
    
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    dark_mode = models.BooleanField(default=False)
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    
    def __str__(self):
        return self.email
    
class UserProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey('lessons.Lesson', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)
    date_completed = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'lesson']
        
    def __str__(self):
        return f"{self.user.email} - {self.lesson.title} - {self.score}%"
        
class SavedWord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='saved_words')
    word = models.ForeignKey('dictionary.Word', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'word']
        
    def __str__(self):
        return f"{self.user.email} - {self.word.word_kz}" 