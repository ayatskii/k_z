from django.db import models
from django.utils.translation import get_language

class Category(models.Model):
    name = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "categories"
    
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

class Word(models.Model):
    word_kz = models.CharField(max_length=255)
    word_en = models.CharField(max_length=255)
    word_ru = models.CharField(max_length=255, blank=True)
    pronunciation = models.CharField(max_length=255, blank=True)
    definition = models.TextField()
    definition_ru = models.TextField(blank=True)
    example_kz = models.TextField(blank=True)
    example_en = models.TextField(blank=True)
    example_ru = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, related_name='words', blank=True)
    audio = models.FileField(upload_to='word_audio/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['word_kz']
    
    def __str__(self):
        return f"{self.word_kz} - {self.word_en}"
    
    def get_word(self):
        language = get_language()
        if language == 'ru' and self.word_ru:
            return self.word_ru
        elif language == 'kz':
            return self.word_kz
        return self.word_en
    
    def get_definition(self):
        language = get_language()
        if language == 'ru' and self.definition_ru:
            return self.definition_ru
        return self.definition
    
    def get_example(self):
        language = get_language()
        if language == 'ru' and self.example_ru:
            return self.example_ru
        elif language == 'kz':
            return self.example_kz
        return self.example_en 