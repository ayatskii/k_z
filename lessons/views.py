from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Lesson, Question, Answer
from users.models import UserProgress

def lesson_list(request):
    # Get all published lessons grouped by level
    levels = {}
    for lesson in Lesson.objects.filter(is_published=True).select_related('level').order_by('level__order', 'order'):
        if lesson.level not in levels:
            levels[lesson.level] = []
        levels[lesson.level].append(lesson)
    
    context = {
        'levels': levels,
    }
    return render(request, 'lessons/lesson_list.html', context)

def lesson_detail(request, slug):
    # Get the lesson details
    lesson = get_object_or_404(Lesson, slug=slug, is_published=True)
    user_progress = None
    
    if request.user.is_authenticated:
        # Get or create user progress for this lesson
        user_progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson,
        )
    
    context = {
        'lesson': lesson,
        'user_progress': user_progress,
    }
    return render(request, 'lessons/lesson_detail.html', context)

@login_required
def lesson_test(request, slug):
    # Get the lesson and questions for the test
    lesson = get_object_or_404(Lesson, slug=slug, is_published=True)
    questions = Question.objects.filter(lesson=lesson).prefetch_related('answers').order_by('order')
    
    context = {
        'lesson': lesson,
        'questions': questions,
    }
    return render(request, 'lessons/lesson_test.html', context)

@login_required
def submit_test(request, slug):
    if request.method != 'POST':
        return redirect('lesson_detail', slug=slug)
    
    lesson = get_object_or_404(Lesson, slug=slug, is_published=True)
    questions = Question.objects.filter(lesson=lesson).prefetch_related('answers')
    
    score = 0
    total_questions = questions.count()
    
    # Calculate the score
    for question in questions:
        correct_answers = Answer.objects.filter(question=question, is_correct=True).values_list('id', flat=True)
        user_answer = request.POST.get(f'question_{question.id}')
        
        if user_answer and int(user_answer) in correct_answers:
            score += 1
    
    # Calculate percentage score
    if total_questions > 0:
        percentage_score = int((score / total_questions) * 100)
    else:
        percentage_score = 0
    
    # Update user progress
    user_progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
    )
    
    user_progress.score = percentage_score
    user_progress.completed = True
    user_progress.save()
    
    messages.success(request, f'Test completed! Your score: {percentage_score}%')
    return redirect('lesson_detail', slug=slug)

@login_required
def save_lesson(request, slug):
    lesson = get_object_or_404(Lesson, slug=slug, is_published=True)
    user_progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
    )
    
    # Toggle the saved status
    is_saved = not user_progress.completed
    user_progress.completed = is_saved
    user_progress.save()
    
    if is_saved:
        messages.success(request, f'Lesson "{lesson.title_en}" saved to your profile.')
    else:
        messages.info(request, f'Lesson "{lesson.title_en}" removed from saved.')
    
    return redirect('lesson_detail', slug=slug) 