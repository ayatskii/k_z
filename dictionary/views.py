from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Word, Category
from users.models import SavedWord
from django.utils.translation import get_language

def dictionary_home(request):
    random_words = Word.objects.order_by('?')[:10]
    categories = Category.objects.all()
    
    context = {
        'random_words': random_words,
        'categories': categories,
    }
    return render(request, 'dictionary/dictionary_home.html', context)

def search_word(request):
    query = request.GET.get('q', '')
    words = []
    
    if query:
        words = Word.objects.filter(
            Q(word_kz__icontains=query) | 
            Q(word_en__icontains=query) |
            Q(word_ru__icontains=query)
        ).order_by('word_kz')
    
    context = {
        'query': query,
        'words': words,
    }
    return render(request, 'dictionary/search_results.html', context)

def word_detail(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    is_saved = False
    
    if request.user.is_authenticated:
        is_saved = SavedWord.objects.filter(user=request.user, word=word).exists()
    
    context = {
        'word': word,
        'is_saved': is_saved,
    }
    return render(request, 'dictionary/word_detail.html', context)

@login_required
def save_word(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    
    saved_word, created = SavedWord.objects.get_or_create(
        user=request.user,
        word=word,
    )
    
    if created:
        messages.success(request, f'Word "{word.word_kz}" added to your saved words.')
    else:
        messages.info(request, f'Word "{word.word_kz}" is already in your saved words.')
    
    return redirect('word_detail', word_id=word_id)

@login_required
def remove_saved_word(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    
    saved_word = SavedWord.objects.filter(user=request.user, word=word)
    if saved_word.exists():
        saved_word.delete()
        messages.success(request, f'Word "{word.word_kz}" removed from your saved words.')
    
    return redirect('word_detail', word_id=word_id)

def category_list(request):
    categories = Category.objects.all()
    
    context = {
        'categories': categories,
    }
    return render(request, 'dictionary/category_list.html', context)

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    words = category.words.all().order_by('word_kz')
    
    context = {
        'category': category,
        'words': words,
    }
    return render(request, 'dictionary/category_detail.html', context) 