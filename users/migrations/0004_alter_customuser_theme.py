# Generated by Django 4.2.10 on 2025-04-24 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_update_black_theme_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='theme',
            field=models.CharField(choices=[('light', 'Light Theme'), ('dark', 'Dark Theme')], default='light', max_length=10),
        ),
    ]
