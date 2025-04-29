from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from allauth.account.views import SignupView
from users.views import change_language, debug_language
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import translation

# Redirect root to default language based on settings
def redirect_to_default(request):
    default_lang = settings.LANGUAGE_CODE
    return HttpResponseRedirect(f'/{default_lang}/')

# Non-translatable URLs
urlpatterns = [
    path('', redirect_to_default, name='root'),  # Redirect root to default language
    path('i18n/', include('django.conf.urls.i18n')),
    path('users/language/<str:language>/', change_language, name='change_language'),
    path('debug-language/', debug_language, name='debug_language'),
]

# Translatable URLs with language prefix
translatable_urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/signup/', SignupView.as_view(), name='account_signup'),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls')),
    path('lessons/', include('lessons.urls')),
    path('dictionary/', include('dictionary.urls')),
    path('', include('core.urls')),
    prefix_default_language=True,  # Show language prefix for all languages
)

# Make sure to properly add the i18n patterns to main urlpatterns
urlpatterns += translatable_urlpatterns

# Static/media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 