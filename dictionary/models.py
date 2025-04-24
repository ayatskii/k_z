from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name

class Word(models.Model):
    word_kz = models.CharField(max_length=255)
    word_en = models.CharField(max_length=255)
    pronunciation = models.CharField(max_length=255, blank=True)
    definition = models.TextField()
    example_kz = models.TextField(blank=True)
    example_en = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, related_name='words', blank=True)
    audio = models.FileField(upload_to='word_audio/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['word_kz']
    
    def __str__(self):
        return f"{self.word_kz} - {self.word_en}" 