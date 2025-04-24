from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProgress, SavedWord
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'dark_mode')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name', 'avatar', 'dark_mode')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    ordering = ('email',)

class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'score', 'date_completed')
    list_filter = ('completed', 'user', 'lesson')
    search_fields = ('user__email', 'lesson__title')

class SavedWordAdmin(admin.ModelAdmin):
    list_display = ('user', 'word', 'date_added')
    list_filter = ('user',)
    search_fields = ('user__email', 'word__word_kz', 'word__word_en')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProgress, UserProgressAdmin)
admin.site.register(SavedWord, SavedWordAdmin) 