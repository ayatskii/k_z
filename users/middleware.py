from django.utils import translation
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class ForceLanguageMiddleware:
    """
    Middleware to handle language selection from URL prefixes, cookies, and defaults
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        try:
            # Check for language prefix in URL first
            language_from_url = None
            path = request.path_info.lstrip('/')
            
            # Look for language code at the start of the URL
            for lang_code, _ in settings.LANGUAGES:
                if path.startswith(f'{lang_code}/') or path == lang_code:
                    language_from_url = lang_code
                    logger.debug(f"Found language in URL: {language_from_url}")
                    break
            
            # Determine which language to use
            if language_from_url:
                # URL language prefix takes precedence
                language = language_from_url
            elif getattr(settings, 'FORCE_DEFAULT_LANGUAGE', False):
                # Use default language if forced
                language = settings.LANGUAGE_CODE
            else:
                # Get language from cookie
                language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
                
                # If not in cookie, try session
                if not language and hasattr(request, 'session'):
                    language = request.session.get('_language')
                
                # If still no language and user is authenticated, use their preference
                if not language and hasattr(request, 'user') and request.user.is_authenticated:
                    language = getattr(request.user, 'language', None)
                
                # If still no language, use default language
                if not language:
                    language = settings.LANGUAGE_CODE
                
                # Validate the language
                valid_languages = [code for code, name in settings.LANGUAGES]
                if language not in valid_languages:
                    language = settings.LANGUAGE_CODE
            
            # Activate the language
            logger.debug(f"Setting language to {language}")
            translation.activate(language)
            request.LANGUAGE_CODE = language
            
            # Get response
            response = self.get_response(request)
            
            # Ensure the language cookie is set (if not coming from URL)
            # This way cookie will match the current URL language
            if language_from_url or not request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME):
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language,
                                  max_age=settings.LANGUAGE_COOKIE_AGE,
                                  path=settings.LANGUAGE_COOKIE_PATH,
                                  domain=settings.LANGUAGE_COOKIE_DOMAIN,
                                  secure=settings.LANGUAGE_COOKIE_SECURE,
                                  httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
                                  samesite=settings.LANGUAGE_COOKIE_SAMESITE)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in ForceLanguageMiddleware: {str(e)}")
            return self.get_response(request) 