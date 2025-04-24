from django.db import models
from django.utils.text import slugify

class LessonLevel(models.Model):
    """Model for lesson levels (A1, A2, B1, etc.)"""
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name

class Lesson(models.Model):
    """Model for individual lessons"""
    level = models.ForeignKey(LessonLevel, on_delete=models.CASCADE, related_name='lessons')
    title_kz = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='lessons/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    class Meta:
        ordering = ['level__order', 'order']
        unique_together = ['level', 'order']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.level} - {self.title_en}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('lesson_detail', kwargs={'slug': self.slug})

class Question(models.Model):
    """Model for test questions"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.lesson.title_en} - Q{self.order}"

class Answer(models.Model):
    """Model for answers to test questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.answer_text} ({'Correct' if self.is_correct else 'Incorrect'})" 