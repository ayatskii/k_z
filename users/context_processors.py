from django.utils import translation
from django.conf import settings
from django.middleware.csrf import get_token

def user_preferences(request):
    """
    Add user preferences to the context for all templates.
    Also adds language information.
    """
    # Get CSRF token for JavaScript
    csrf_token = get_token(request)
    
    # Get current language from request
    current_language = translation.get_language() or 'en'
    
    context = {
        'current_language': current_language,
        'available_languages': [lang_code for lang_code, lang_name in settings.LANGUAGES],
        'csrf_token': csrf_token,
    }
    
    # User theme preference
    if request.user.is_authenticated:
        context['user_theme'] = request.user.theme
        context['user_language'] = request.user.language
    else:
        # Default values for non-authenticated users
        context['user_theme'] = 'light'
        context['user_language'] = current_language
    
    # Ensure LANGUAGE_CODE is always available
    context['LANGUAGE_CODE'] = context['current_language']
    
    return context 