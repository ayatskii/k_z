from django.db import models
from django.utils.text import slugify
from django.utils.translation import get_language

class LessonLevel(models.Model):
    """Model for lesson levels (A1, A2, B1, etc.)"""
    name = models.CharField(max_length=50)
    name_ru = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name
    
    def get_name(self):
        language = get_language()
        if language == 'ru' and self.name_ru:
            return self.name_ru
        return self.name
    
    def get_description(self):
        language = get_language()
        if language == 'ru' and self.description_ru:
            return self.description_ru
        return self.description

class Lesson(models.Model):
    """Model for individual lessons"""
    level = models.ForeignKey(LessonLevel, on_delete=models.CASCADE, related_name='lessons')
    title_kz = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    content = models.TextField()
    content_ru = models.TextField(blank=True)
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
    
    def get_title(self):
        language = get_language()
        if language == 'ru' and self.title_ru:
            return self.title_ru
        elif language == 'kz':
            return self.title_kz
        return self.title_en
    
    def get_description(self):
        language = get_language()
        if language == 'ru' and self.description_ru:
            return self.description_ru
        return self.description
    
    def get_content(self):
        language = get_language()
        if language == 'ru' and self.content_ru:
            return self.content_ru
        return self.content
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('lesson_detail', kwargs={'slug': self.slug})

class Question(models.Model):
    """Model for test questions"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_text_ru = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.lesson.title_en} - Q{self.order}"
    
    def get_question_text(self):
        language = get_language()
        if language == 'ru' and self.question_text_ru:
            return self.question_text_ru
        return self.question_text

class Answer(models.Model):
    """Model for answers to test questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.CharField(max_length=255)
    answer_text_ru = models.CharField(max_length=255, blank=True)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.answer_text} ({'Correct' if self.is_correct else 'Incorrect'})"
    
    def get_answer_text(self):
        language = get_language()
        if language == 'ru' and self.answer_text_ru:
            return self.answer_text_ru
        return self.answer_text 