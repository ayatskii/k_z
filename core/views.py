from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson

def home(request):
    # Get featured lessons for the homepage
    featured_lessons = Lesson.objects.filter(is_published=True).order_by('level__order', 'order')[:6]
    
    context = {
        'featured_lessons': featured_lessons,
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

@login_required
def toggle_theme(request):
    # Toggle dark mode setting for the user (legacy support)
    user = request.user
    user.dark_mode = not user.dark_mode
    
    # Also update the theme field for consistency
    if user.dark_mode:
        user.theme = 'dark'
    else:
        user.theme = 'light'
        
    user.save()
    
    # Redirect back to the referring page or home
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)

@login_required
def change_theme(request, theme_name):
    # Change to the specified theme
    user = request.user
    
    # Handle case where black theme was requested but is no longer available
    if theme_name == 'black':
        theme_name = 'dark'
    
    if theme_name in [choice[0] for choice in user._meta.get_field('theme').choices]:
        user.theme = theme_name
        
        # Update dark_mode for backward compatibility
        user.dark_mode = (theme_name != 'light')
        
        user.save()
    
    # Redirect back to the referring page or home
    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url) 