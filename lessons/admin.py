from django.contrib import admin
from .models import LessonLevel, Lesson, Question, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'question_text', 'order')
    list_filter = ('lesson',)
    search_fields = ('question_text', 'lesson__title_en')
    inlines = [AnswerInline]

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'title_kz', 'level', 'order', 'is_published')
    list_filter = ('level', 'is_published')
    search_fields = ('title_en', 'title_kz', 'description')
    prepopulated_fields = {'slug': ('title_en',)}
    inlines = [QuestionInline]

class LessonLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'order')
    list_editable = ('order',)

admin.site.register(LessonLevel, LessonLevelAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin) 