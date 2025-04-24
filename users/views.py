from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Prefetch
from .models import CustomUser, UserProgress, SavedWord
from .forms import UserProfileForm, CustomUserChangeForm
from lessons.models import Lesson
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from allauth.account.views import SignupView
from allauth.account.utils import complete_signup
from allauth.account import app_settings
from dictionary.models import Word

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