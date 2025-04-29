from django.contrib import admin
from .models import LessonLevel, Lesson, Question, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    fields = ('answer_text', 'answer_text_ru', 'is_correct')

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3
    fields = ('question_text', 'question_text_ru', 'order')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'question_text', 'order')
    list_filter = ('lesson',)
    search_fields = ('question_text', 'question_text_ru', 'lesson__title_en', 'lesson__title_ru')
    inlines = [AnswerInline]
    fieldsets = (
        (None, {
            'fields': ('lesson', 'order')
        }),
        ('Content', {
            'fields': ('question_text', 'question_text_ru')
        }),
    )

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'title_kz', 'title_ru', 'level', 'order', 'is_published')
    list_filter = ('level', 'is_published')
    search_fields = ('title_en', 'title_kz', 'title_ru', 'description', 'description_ru')
    prepopulated_fields = {'slug': ('title_en',)}
    inlines = [QuestionInline]
    fieldsets = (
        (None, {
            'fields': ('level', 'slug', 'order', 'is_published')
        }),
        ('English Content', {
            'fields': ('title_en', 'description', 'content')
        }),
        ('Kazakh Content', {
            'fields': ('title_kz',)
        }),
        ('Russian Content', {
            'fields': ('title_ru', 'description_ru', 'content_ru')
        }),
        ('Media', {
            'fields': ('video_url', 'image')
        }),
    )

class LessonLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_ru', 'order')
    list_editable = ('order',)
    fieldsets = (
        (None, {
            'fields': ('order',)
        }),
        ('English Content', {
            'fields': ('name', 'description')
        }),
        ('Russian Content', {
            'fields': ('name_ru', 'description_ru')
        }),
    )

admin.site.register(LessonLevel, LessonLevelAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin) 