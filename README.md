# Qazaq Learn
A Django-based site for learning the Kazakh language with interactive lessons and a dictionary.

## Internationalization (i18n)

The site supports multiple languages using Django's built-in internationalization framework. Currently, the site is available in English and Russian.

### URL Structure

The site uses language-prefixed URLs. For example:
- English: `http://example.com/en/lessons/`
- Russian: `http://example.com/ru/lessons/`

The language prefix takes precedence over other language selection methods.

### Language Selection

The language can be selected in several ways (in order of precedence):

1. URL prefix (e.g., `/en/`, `/ru/`) - always takes precedence when using i18n_patterns
2. User preference (for authenticated users)
3. Session/Cookie (django_language)
4. Browser preference (Accept-Language header)
5. Default language (LANGUAGE_CODE setting, currently 'en')

### How to Compile Translation Files

If you make changes to the translation strings, you need to compile the translation files:

```bash
python update_translations.py
```

### Adding New Translations

To add a new translation:

1. Add the language to the LANGUAGES setting in settings.py
2. Run `django-admin makemessages -l <language_code>`
3. Edit the generated .po file in locale/<language_code>/LC_MESSAGES/django.po
4. Compile using `python update_translations.py`

### Translation Files

- Translation strings are defined in Python code with `gettext` or `_()` functions
- Templates use `{% trans %}` or `{% blocktrans %}` tags
- .po files contain the translatable strings and their translations
- .mo files are compiled versions used by Django at runtime 