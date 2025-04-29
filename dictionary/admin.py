from django.contrib import admin
from .models import Category, Word

class WordAdmin(admin.ModelAdmin):
    list_display = ('word_kz', 'word_en', 'word_ru', 'created_at')
    list_filter = ('categories',)
    search_fields = ('word_kz', 'word_en', 'word_ru', 'definition', 'definition_ru')
    filter_horizontal = ('categories',)
    fieldsets = (
        (None, {
            'fields': ('word_kz', 'word_en', 'word_ru', 'pronunciation', 'audio')
        }),
        ('Content', {
            'fields': ('definition', 'definition_ru', 'example_kz', 'example_en', 'example_ru')
        }),
        ('Categorization', {
            'fields': ('categories',)
        }),
    )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_ru')
    search_fields = ('name', 'name_ru')
    fieldsets = (
        (None, {
            'fields': ('name', 'name_ru')
        }),
        ('Description', {
            'fields': ('description', 'description_ru')
        }),
    )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Word, WordAdmin) 