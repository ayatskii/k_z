from django.contrib import admin
from .models import Category, Word

class WordAdmin(admin.ModelAdmin):
    list_display = ('word_kz', 'word_en', 'created_at')
    list_filter = ('categories',)
    search_fields = ('word_kz', 'word_en', 'definition')
    filter_horizontal = ('categories',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Word, WordAdmin) 