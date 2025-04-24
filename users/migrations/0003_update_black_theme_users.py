from django.db import migrations

def update_black_theme_users(apps, schema_editor):
    CustomUser = apps.get_model('users', 'CustomUser')
    # Find all users with black theme and update them to dark theme
    CustomUser.objects.filter(theme='black').update(theme='dark')

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_theme'),
    ]

    operations = [
        migrations.RunPython(update_black_theme_users),
    ] 