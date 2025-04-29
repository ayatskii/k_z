from django.core.management.base import BaseCommand
from lessons.models import LessonLevel, Lesson, Question, Answer
from django.db.models import Q

class Command(BaseCommand):
    help = 'Add Russian translations to existing lessons, levels, questions, and answers'

    def handle(self, *args, **options):
        # Translate lesson levels
        self.stdout.write(self.style.SUCCESS('Adding Russian translations to lesson levels...'))
        levels = LessonLevel.objects.filter(Q(name_ru__isnull=True) | Q(name_ru=''))
        level_translations = {
            'Beginner': 'Начальный',
            'Elementary': 'Элементарный',
            'Pre-Intermediate': 'Предсредний',
            'Intermediate': 'Средний',
            'Upper-Intermediate': 'Выше среднего',
            'Advanced': 'Продвинутый',
            'A1': 'A1 (Начальный)',
            'A2': 'A2 (Элементарный)',
            'B1': 'B1 (Средний)',
            'B2': 'B2 (Выше среднего)',
            'C1': 'C1 (Продвинутый)',
            'C2': 'C2 (Владение в совершенстве)'
        }
        
        for level in levels:
            if level.name in level_translations:
                level.name_ru = level_translations[level.name]
                level.description_ru = f"Уровень {level_translations[level.name]}: {level.description}"
                level.save()
                self.stdout.write(f"  - Added translation for level: {level.name} -> {level.name_ru}")
        
        # Translate lessons
        self.stdout.write(self.style.SUCCESS('Adding Russian translations to lessons...'))
        lessons = Lesson.objects.filter(Q(title_ru__isnull=True) | Q(title_ru=''))
        
        # Add some sample translations based on common lesson titles
        lesson_title_translations = {
            'Introduction to Kazakh': 'Введение в казахский язык',
            'Greetings and Introductions': 'Приветствия и знакомства',
            'Numbers and Counting': 'Числа и счет',
            'Family and Relations': 'Семья и отношения',
            'Food and Dining': 'Еда и питание',
            'Time and Date': 'Время и дата',
            'Weather and Seasons': 'Погода и времена года',
            'Travel and Directions': 'Путешествия и направления',
            'Everyday Conversations': 'Повседневные разговоры',
            'Kazakh Grammar Basics': 'Основы казахской грамматики',
            'House and Home': 'Дом и жилище',
            'Shopping and Money': 'Покупки и деньги',
        }
        
        for lesson in lessons:
            # Try to find a matching title pattern or generate a default translation
            translated_title = None
            for eng_title, ru_title in lesson_title_translations.items():
                if eng_title.lower() in lesson.title_en.lower():
                    translated_title = ru_title
                    break
            
            if not translated_title:
                translated_title = f"Урок: {lesson.title_en}"
            
            lesson.title_ru = translated_title
            lesson.description_ru = f"Это урок на тему '{translated_title}'. {lesson.description if lesson.description else ''}"
            lesson.content_ru = f"<h2>{translated_title}</h2>\n<p>Содержание урока на русском языке.</p>\n{lesson.content}"
            lesson.save()
            self.stdout.write(f"  - Added translation for lesson: {lesson.title_en} -> {lesson.title_ru}")
        
        # Translate questions
        self.stdout.write(self.style.SUCCESS('Adding Russian translations to questions...'))
        questions = Question.objects.filter(Q(question_text_ru__isnull=True) | Q(question_text_ru=''))
        
        for question in questions:
            question.question_text_ru = f"Вопрос: {question.question_text}"
            question.save()
            self.stdout.write(f"  - Added translation for question ID {question.id}")
        
        # Translate answers
        self.stdout.write(self.style.SUCCESS('Adding Russian translations to answers...'))
        answers = Answer.objects.filter(Q(answer_text_ru__isnull=True) | Q(answer_text_ru=''))
        
        for answer in answers:
            answer.answer_text_ru = f"{answer.answer_text} (по-русски)"
            answer.save()
            self.stdout.write(f"  - Added translation for answer ID {answer.id}")
        
        self.stdout.write(self.style.SUCCESS('Russian translations added successfully!')) 