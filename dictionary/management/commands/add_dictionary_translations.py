from django.core.management.base import BaseCommand
from dictionary.models import Category, Word
from django.db.models import Q

class Command(BaseCommand):
    help = 'Add Russian translations to dictionary categories and words'

    def handle(self, *args, **options):
        # Translate categories
        self.stdout.write(self.style.SUCCESS('Adding Russian translations to dictionary categories...'))
        categories = Category.objects.filter(Q(name_ru__isnull=True) | Q(name_ru=''))
        
        category_translations = {
            'Animals': 'Животные',
            'Food': 'Еда',
            'Family': 'Семья',
            'Numbers': 'Числа',
            'Colors': 'Цвета',
            'Clothing': 'Одежда',
            'Transportation': 'Транспорт',
            'Time': 'Время',
            'Weather': 'Погода',
            'Places': 'Места',
            'Professions': 'Профессии',
            'Body Parts': 'Части тела',
            'House': 'Дом',
            'Nature': 'Природа',
            'Verbs': 'Глаголы',
            'Adjectives': 'Прилагательные',
            'Common Phrases': 'Общие фразы',
            'Greetings': 'Приветствия'
        }
        
        for category in categories:
            if category.name in category_translations:
                category.name_ru = category_translations[category.name]
                category.description_ru = f"Словарь казахских слов в категории '{category_translations[category.name]}'"
                category.save()
                self.stdout.write(f"  - Added translation for category: {category.name} -> {category.name_ru}")
            else:
                category.name_ru = f"{category.name} (рус)"
                category.description_ru = f"Словарь казахских слов в этой категории"
                category.save()
                self.stdout.write(f"  - Added generic translation for category: {category.name}")
        
        # Translate words
        self.stdout.write(self.style.SUCCESS('Adding Russian translations to dictionary words...'))
        words = Word.objects.filter(Q(word_ru__isnull=True) | Q(word_ru='') | Q(definition_ru__isnull=True) | Q(definition_ru=''))
        
        # Sample common words translations
        word_translations = {
            'hello': 'привет',
            'goodbye': 'до свидания',
            'thank you': 'спасибо',
            'yes': 'да',
            'no': 'нет',
            'please': 'пожалуйста',
            'water': 'вода',
            'bread': 'хлеб',
            'good': 'хороший',
            'bad': 'плохой',
            'family': 'семья',
            'mother': 'мать',
            'father': 'отец',
            'brother': 'брат',
            'sister': 'сестра',
            'house': 'дом',
            'car': 'машина',
            'time': 'время',
            'day': 'день',
            'night': 'ночь'
        }
        
        for word in words:
            # Try to find a matching word or generate a default translation
            for eng_word, ru_word in word_translations.items():
                if eng_word.lower() in word.word_en.lower():
                    word.word_ru = ru_word
                    break
            
            if not word.word_ru:
                word.word_ru = f"{word.word_en} (рус)"
            
            word.definition_ru = f"Определение: {word.definition}"
            
            if word.example_en and not word.example_ru:
                word.example_ru = f"Пример: {word.example_en}"
            
            word.save()
            self.stdout.write(f"  - Added translation for word: {word.word_en} -> {word.word_ru}")
        
        self.stdout.write(self.style.SUCCESS('Russian translations added successfully to dictionary!')) 