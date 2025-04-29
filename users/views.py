from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Prefetch
from .models import CustomUser, UserProgress, SavedWord
from .forms import UserProfileForm, CustomUserChangeForm
from lessons.models import Lesson
from django.urls import reverse_lazy, translate_url
from django.views.generic.edit import UpdateView
from allauth.account.views import SignupView
from allauth.account.utils import complete_signup
from allauth.account import app_settings
from dictionary.models import Word
from django.utils import translation
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from urllib.parse import urlparse
from django.utils.translation import activate, get_language

# Custom signup view to override email verification
class CustomSignupView(SignupView):
    def form_valid(self, form):
        user = form.save(self.request)
        # Use 'none' verification regardless of settings
        return complete_signup(
            self.request,
            user,
            app_settings.EmailVerificationMethod.NONE,
            self.get_success_url(),
        )

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'users/edit_profile.html', context)

@login_required
def saved_words(request):
    saved_words = SavedWord.objects.filter(user=request.user).select_related('word')
    return render(request, 'users/saved_words.html', {'saved_words': saved_words})

@login_required
def remove_saved_word(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    saved_word = SavedWord.objects.filter(user=request.user, word=word)
    
    if saved_word.exists():
        saved_word.delete()
        messages.success(request, f'Word "{word.word_kz}" removed from your saved words.')
    else:
        messages.error(request, f'Word not found in your saved words.')
    
    # Redirect to referer or saved words page
    return redirect(request.META.get('HTTP_REFERER', 'saved_words'))

@login_required
def user_progress(request):
    user_progress = UserProgress.objects.filter(user=request.user)
    
    completed_lessons = [progress.lesson for progress in user_progress if progress.completed]
    in_progress_lessons = [progress.lesson for progress in user_progress if not progress.completed]
    
    # Group progress by level
    progress_by_level = {}
    for progress in user_progress:
        level = progress.lesson.level
        if level not in progress_by_level:
            progress_by_level[level] = {
                'total': 0,
                'completed': 0,
                'percentage': 0,
            }
        progress_by_level[level]['total'] += 1
        if progress.completed:
            progress_by_level[level]['completed'] += 1
    
    # Calculate completion percentage for each level
    for level in progress_by_level:
        total = progress_by_level[level]['total']
        completed = progress_by_level[level]['completed']
        if total > 0:
            progress_by_level[level]['percentage'] = int((completed / total) * 100)
    
    context = {
        'completed_lessons': completed_lessons,
        'in_progress_lessons': in_progress_lessons,
        'progress_by_level': progress_by_level,
    }
    return render(request, 'users/user_progress.html', context)

@login_required
def change_theme(request, theme):
    if theme in ['light', 'dark']:
        request.user.theme = theme
        request.user.save()
        messages.success(request, f'Theme changed to {theme} mode.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def change_language(request, language):
    # Check if language is valid
    languages = [code for code, name in settings.LANGUAGES]
    if language not in languages:
        return JsonResponse({'success': False, 'message': 'Invalid language'}, status=400)
    
    # Update user preference if authenticated
    if request.user.is_authenticated:
        request.user.language = language
        request.user.save()
    
    # Set language in session
    request.session['_language'] = language
    translation.activate(language)
    
    # Get the next URL from the request, or default to home
    next_url = request.GET.get('next', '/')
    
    # Handle language prefix in the URL
    # First, check if the URL starts with a language prefix
    has_lang_prefix = False
    for lang_code, _ in settings.LANGUAGES:
        if next_url.startswith(f'/{lang_code}/'):
            has_lang_prefix = True
            # Replace the current language prefix with the new one
            next_url = f'/{language}/{next_url[len(lang_code)+2:]}'
            break
    
    # If no language prefix was found, add the new language prefix
    if not has_lang_prefix:
        if next_url.startswith('/'):
            next_url = f'/{language}{next_url}'
        else:
            next_url = f'/{language}/{next_url}'
    
    # Ensure we don't have double slashes
    next_url = next_url.replace('//', '/')
    if not next_url.startswith('/'):
        next_url = '/' + next_url
    
    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        response = JsonResponse({
            'success': True,
            'redirect_url': next_url,
            'message': 'Language changed successfully'
        })
        # Set language cookie for AJAX responses
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            language,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE
        )
        return response
    
    # For non-AJAX requests, redirect to the translated URL
    response = redirect(next_url)
    
    # Set language cookie for non-AJAX responses
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME,
        language,
        max_age=settings.LANGUAGE_COOKIE_AGE,
        path=settings.LANGUAGE_COOKIE_PATH,
        domain=settings.LANGUAGE_COOKIE_DOMAIN,
        secure=settings.LANGUAGE_COOKIE_SECURE,
        httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
        samesite=settings.LANGUAGE_COOKIE_SAMESITE
    )
    
    # Set success message
    if language == 'en':
        messages.success(request, 'Language changed to English.')
    elif language == 'ru':
        messages.success(request, 'Язык изменен на Русский.')
    
    return response

def debug_language(request):
    """Debug view to show language settings"""
    active_language = translation.get_language()
    language_from_request = getattr(request, 'LANGUAGE_CODE', None)
    cookie_language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
    session_language = request.session.get('_language')
    
    user_language = None
    if request.user.is_authenticated:
        user_language = request.user.language
    
    # Test translations
    from django.utils.translation import gettext as _
    translated = {
        'Home': _('Home'),
        'Lessons': _('Lessons'),
        'Dictionary': _('Dictionary'),
    }
    
    # Check if we're using a language URL prefix
    path = request.path_info
    url_has_prefix = False
    url_language = None
    
    # Check if URL starts with a language code
    for lang_code, _ in settings.LANGUAGES:
        if path.startswith(f'/{lang_code}/'):
            url_has_prefix = True
            url_language = lang_code
            break
    
    data = {
        'active_language': active_language,
        'language_from_request': language_from_request,
        'cookie_language': cookie_language,
        'session_language': session_language,
        'user_language': user_language,
        'available_languages': settings.LANGUAGES,
        'language_cookie_name': settings.LANGUAGE_COOKIE_NAME,
        'translations': translated,
        'url_has_language_prefix': url_has_prefix,
        'url_language': url_language,
        'note': 'When using i18n_patterns with language URL prefixes, the URL prefix takes precedence over cookies',
        'current_url': request.build_absolute_uri(),
    }
    
    return JsonResponse(data)

class ProfileUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form) 