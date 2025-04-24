import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from dictionary.models import Category, Word
from lessons.models import LessonLevel, Lesson, Question, Answer

class Command(BaseCommand):
    help = 'Populates the database with sample Kazakh words and lessons'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting database population...')
        
        # Create categories
        self.create_categories()
        
        # Create words
        self.create_words()
        
        # Create lesson levels
        self.create_lesson_levels()
        
        # Create lessons
        self.create_lessons()
        
        self.stdout.write(self.style.SUCCESS('Database successfully populated!'))
    
    def create_categories(self):
        categories = [
            {'name': 'Everyday', 'description': 'Common everyday words'},
            {'name': 'Numbers', 'description': 'Numerical words and counting'},
            {'name': 'Food', 'description': 'Words related to food and dining'},
            {'name': 'Family', 'description': 'Family-related terminology'},
            {'name': 'Travel', 'description': 'Words useful for traveling'},
            {'name': 'Colors', 'description': 'Color-related vocabulary'},
            {'name': 'Time', 'description': 'Time-related words and phrases'},
            {'name': 'Greetings', 'description': 'Greeting words and phrases'},
        ]
        
        for category_data in categories:
            Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
        
        self.stdout.write(f'Created {len(categories)} categories')
    
    def create_words(self):
        words_data = [
            # Greetings
            {'word_kz': 'Сәлем', 'word_en': 'Hello', 'pronunciation': 'Sälem', 
             'definition': 'A common greeting used to say hello', 
             'example_kz': 'Сәлем, қалың қалай?', 'example_en': 'Hello, how are you?',
             'categories': ['Greetings', 'Everyday']},
            
            {'word_kz': 'Қайырлы таң', 'word_en': 'Good morning', 'pronunciation': 'Qaiyrly tang', 
             'definition': 'Morning greeting', 
             'example_kz': 'Қайырлы таң, бүгін ауа-райы жақсы.', 'example_en': 'Good morning, the weather is good today.',
             'categories': ['Greetings', 'Time']},
            
            {'word_kz': 'Қайырлы кеш', 'word_en': 'Good evening', 'pronunciation': 'Qaiyrly kesh', 
             'definition': 'Evening greeting', 
             'example_kz': 'Қайырлы кеш, кешкі ас ішесіз бе?', 'example_en': 'Good evening, would you like dinner?',
             'categories': ['Greetings', 'Time']},
            
            {'word_kz': 'Рахмет', 'word_en': 'Thank you', 'pronunciation': 'Rakhmet', 
             'definition': 'Expression of gratitude', 
             'example_kz': 'Көмегіңіз үшін рахмет.', 'example_en': 'Thank you for your help.',
             'categories': ['Greetings', 'Everyday']},
            
            # Numbers
            {'word_kz': 'Бір', 'word_en': 'One', 'pronunciation': 'Bir', 
             'definition': 'The number 1', 
             'example_kz': 'Маған бір алма берші.', 'example_en': 'Please give me one apple.',
             'categories': ['Numbers']},
            
            {'word_kz': 'Екі', 'word_en': 'Two', 'pronunciation': 'Yeki', 
             'definition': 'The number 2', 
             'example_kz': 'Менің екі бауырым бар.', 'example_en': 'I have two brothers.',
             'categories': ['Numbers']},
            
            {'word_kz': 'Үш', 'word_en': 'Three', 'pronunciation': 'Üsh', 
             'definition': 'The number 3', 
             'example_kz': 'Үстелде үш кітап жатыр.', 'example_en': 'There are three books on the table.',
             'categories': ['Numbers']},
            
            # Food
            {'word_kz': 'Нан', 'word_en': 'Bread', 'pronunciation': 'Nan', 
             'definition': 'Baked food made of flour', 
             'example_kz': 'Дүкеннен нан сатып алдым.', 'example_en': 'I bought bread from the store.',
             'categories': ['Food']},
            
            {'word_kz': 'Ет', 'word_en': 'Meat', 'pronunciation': 'Yet', 
             'definition': 'Flesh of an animal used as food', 
             'example_kz': 'Бұл ет өте дәмді.', 'example_en': 'This meat is very tasty.',
             'categories': ['Food']},
            
            {'word_kz': 'Су', 'word_en': 'Water', 'pronunciation': 'Su', 
             'definition': 'Clear liquid essential for life', 
             'example_kz': 'Маған бір стакан су беріңізші.', 'example_en': 'Please give me a glass of water.',
             'categories': ['Food', 'Everyday']},
            
            # Family
            {'word_kz': 'Ата', 'word_en': 'Grandfather', 'pronunciation': 'Ata', 
             'definition': 'Father of one\'s father or mother', 
             'example_kz': 'Менің атам 80 жаста.', 'example_en': 'My grandfather is 80 years old.',
             'categories': ['Family']},
            
            {'word_kz': 'Әже', 'word_en': 'Grandmother', 'pronunciation': 'Äje', 
             'definition': 'Mother of one\'s father or mother', 
             'example_kz': 'Әжем маған ертегі айтып береді.', 'example_en': 'My grandmother tells me stories.',
             'categories': ['Family']},
            
            {'word_kz': 'Әке', 'word_en': 'Father', 'pronunciation': 'Äke', 
             'definition': 'Male parent', 
             'example_kz': 'Менің әкем мұғалім.', 'example_en': 'My father is a teacher.',
             'categories': ['Family']},
            
            {'word_kz': 'Ана', 'word_en': 'Mother', 'pronunciation': 'Ana', 
             'definition': 'Female parent', 
             'example_kz': 'Менің анам дәрігер.', 'example_en': 'My mother is a doctor.',
             'categories': ['Family']},
            
            # Colors
            {'word_kz': 'Қызыл', 'word_en': 'Red', 'pronunciation': 'Qyzyl', 
             'definition': 'Color of blood or a ripe tomato', 
             'example_kz': 'Мен қызыл көйлек сатып алдым.', 'example_en': 'I bought a red dress.',
             'categories': ['Colors']},
            
            {'word_kz': 'Көк', 'word_en': 'Blue', 'pronunciation': 'Kök', 
             'definition': 'Color of the sky or sea', 
             'example_kz': 'Аспан көк.', 'example_en': 'The sky is blue.',
             'categories': ['Colors']},
            
            {'word_kz': 'Жасыл', 'word_en': 'Green', 'pronunciation': 'Jasyl', 
             'definition': 'Color of grass or leaves', 
             'example_kz': 'Жапырақтар жасыл.', 'example_en': 'The leaves are green.',
             'categories': ['Colors']},
        ]
        
        # Add words to database
        categories = {category.name: category for category in Category.objects.all()}
        
        for word_data in words_data:
            word, created = Word.objects.get_or_create(
                word_kz=word_data['word_kz'],
                word_en=word_data['word_en'],
                defaults={
                    'pronunciation': word_data['pronunciation'],
                    'definition': word_data['definition'],
                    'example_kz': word_data['example_kz'],
                    'example_en': word_data['example_en'],
                }
            )
            
            # Add categories to word
            for category_name in word_data['categories']:
                if category_name in categories:
                    word.categories.add(categories[category_name])
        
        self.stdout.write(f'Created {len(words_data)} words')
    
    def create_lesson_levels(self):
        levels = [
            {'name': 'A1 - Beginner', 'description': 'Basic phrases and expressions', 'order': 1},
            {'name': 'A2 - Elementary', 'description': 'Simple conversations on familiar topics', 'order': 2},
            {'name': 'B1 - Intermediate', 'description': 'Clear standard speech on familiar matters', 'order': 3},
            {'name': 'B2 - Upper Intermediate', 'description': 'Complex speech and advanced topics', 'order': 4},
        ]
        
        for level_data in levels:
            LessonLevel.objects.get_or_create(
                name=level_data['name'],
                defaults={
                    'description': level_data['description'],
                    'order': level_data['order']
                }
            )
        
        self.stdout.write(f'Created {len(levels)} lesson levels')
    
    def create_lessons(self):
        lessons_data = [
            # A1 Beginner Lessons
            {
                'level': 'A1 - Beginner',
                'title_kz': 'Амандасу',
                'title_en': 'Greetings',
                'description': 'Learn basic Kazakh greetings and introductions',
                'content': """
# Greetings in Kazakh

In this lesson, you will learn basic greetings in Kazakh language.

## Basic Greetings

- **Сәлем** (Sälem) - Hello
- **Қайырлы таң** (Qaiyrly tang) - Good morning
- **Қайырлы күн** (Qaiyrly kün) - Good day
- **Қайырлы кеш** (Qaiyrly kesh) - Good evening
- **Сау болыңыз** (Sau bolyñyz) - Goodbye (formal)
- **Сау бол** (Sau bol) - Goodbye (informal)

## Introductions

- **Менің атым...** (Meniñ atym...) - My name is...
- **Сіздің атыңыз кім?** (Sizdiñ atyñyz kim?) - What is your name? (formal)
- **Сенің атың кім?** (Seniñ atyñ kim?) - What is your name? (informal)
- **Танысқаныма қуаныштымын** (Tanysqanyma quanyshtymyn) - Nice to meet you

## Common Phrases

- **Рахмет** (Rakhmet) - Thank you
- **Өтінемін** (Ötinemin) - Please / You're welcome
- **Кешіріңіз** (Keshiriñiz) - Excuse me / Sorry
- **Иә** (Iä) - Yes
- **Жоқ** (Joq) - No
                """,
                'order': 1,
                'questions': [
                    {
                        'question_text': 'How do you say "Hello" in Kazakh?',
                        'order': 1,
                        'answers': [
                            {'answer_text': 'Сәлем', 'is_correct': True},
                            {'answer_text': 'Рахмет', 'is_correct': False},
                            {'answer_text': 'Сау бол', 'is_correct': False},
                            {'answer_text': 'Иә', 'is_correct': False},
                        ]
                    },
                    {
                        'question_text': 'Which phrase means "Thank you" in Kazakh?',
                        'order': 2,
                        'answers': [
                            {'answer_text': 'Сәлем', 'is_correct': False},
                            {'answer_text': 'Рахмет', 'is_correct': True},
                            {'answer_text': 'Жоқ', 'is_correct': False},
                            {'answer_text': 'Өтінемін', 'is_correct': False},
                        ]
                    },
                    {
                        'question_text': 'How do you ask "What is your name?" in formal Kazakh?',
                        'order': 3,
                        'answers': [
                            {'answer_text': 'Сенің атың кім?', 'is_correct': False},
                            {'answer_text': 'Менің атым...', 'is_correct': False},
                            {'answer_text': 'Сіздің атыңыз кім?', 'is_correct': True},
                            {'answer_text': 'Танысқаныма қуаныштымын', 'is_correct': False},
                        ]
                    },
                ]
            },
            {
                'level': 'A1 - Beginner',
                'title_kz': 'Сандар',
                'title_en': 'Numbers',
                'description': 'Learn numbers in Kazakh language from 1 to 20',
                'content': """
# Numbers in Kazakh

In this lesson, you will learn how to count in Kazakh from 1 to 20.

## Numbers 1-10

- **1 - Бір** (Bir)
- **2 - Екі** (Yeki)
- **3 - Үш** (Üsh)
- **4 - Төрт** (Tört)
- **5 - Бес** (Bes)
- **6 - Алты** (Alty)
- **7 - Жеті** (Jeti)
- **8 - Сегіз** (Segiz)
- **9 - Тоғыз** (Toğyz)
- **10 - Он** (On)

## Numbers 11-20

- **11 - Он бір** (On bir)
- **12 - Он екі** (On yeki)
- **13 - Он үш** (On üsh)
- **14 - Он төрт** (On tört)
- **15 - Он бес** (On bes)
- **16 - Он алты** (On alty)
- **17 - Он жеті** (On jeti)
- **18 - Он сегіз** (On segiz)
- **19 - Он тоғыз** (On toğyz)
- **20 - Жиырма** (Jiyrma)

## Using Numbers in Sentences

- **Маған бес алма керек.** (Mağan bes alma kerek.) - I need five apples.
- **Сіз неше жастасыз?** (Siz neshe jastasyz?) - How old are you?
- **Мен жиырма жастамын.** (Men jiyrma jastamyn.) - I am twenty years old.
                """,
                'order': 2,
                'questions': [
                    {
                        'question_text': 'What is the Kazakh word for the number 5?',
                        'order': 1,
                        'answers': [
                            {'answer_text': 'Үш', 'is_correct': False},
                            {'answer_text': 'Бес', 'is_correct': True},
                            {'answer_text': 'Жеті', 'is_correct': False},
                            {'answer_text': 'Тоғыз', 'is_correct': False},
                        ]
                    },
                    {
                        'question_text': 'How do you say 18 in Kazakh?',
                        'order': 2,
                        'answers': [
                            {'answer_text': 'Он алты', 'is_correct': False},
                            {'answer_text': 'Жиырма', 'is_correct': False},
                            {'answer_text': 'Он сегіз', 'is_correct': True},
                            {'answer_text': 'Сегіз', 'is_correct': False},
                        ]
                    },
                    {
                        'question_text': 'Which of these numbers is "Töрт" in Kazakh?',
                        'order': 3,
                        'answers': [
                            {'answer_text': '2', 'is_correct': False},
                            {'answer_text': '4', 'is_correct': True},
                            {'answer_text': '6', 'is_correct': False},
                            {'answer_text': '8', 'is_correct': False},
                        ]
                    },
                ]
            },
            # A2 Elementary Lessons
            {
                'level': 'A2 - Elementary',
                'title_kz': 'Отбасы',
                'title_en': 'Family',
                'description': 'Learn family-related vocabulary in Kazakh',
                'content': """
# Family Vocabulary in Kazakh

In this lesson, you will learn vocabulary related to family members in Kazakh.

## Immediate Family

- **Әке** (Äke) - Father
- **Ана** (Ana) - Mother
- **Ұл** (Ul) - Son
- **Қыз** (Qyz) - Daughter
- **Аға** (Ağa) - Elder brother
- **Іні** (Ini) - Younger brother
- **Әпке** (Äpke) - Elder sister
- **Сіңлі/Қарындас** (Siñli/Qaryndas) - Younger sister
- **Ата** (Ata) - Grandfather
- **Әже** (Äje) - Grandmother

## Extended Family

- **Немере** (Nemere) - Grandchild
- **Нағашы** (Nağashy) - Maternal relatives
- **Жиен** (Jien) - Nephew/niece (sister's children)
- **Келін** (Kelin) - Daughter-in-law
- **Күйеу бала** (Küyeu bala) - Son-in-law
- **Құда** (Quda) - Co-in-laws

## Useful Phrases

- **Менің отбасым үлкен.** (Meniñ otbasym ülken.) - My family is big.
- **Сіздің отбасыңызда кім бар?** (Sizdiñ otbasyñyzda kim bar?) - Who is in your family?
- **Менің екі ағам және бір әпкем бар.** (Meniñ yeki ağam jäne bir äpkem bar.) - I have two elder brothers and one elder sister.
                """,
                'order': 1,
                'questions': [
                    {
                        'question_text': 'What is the Kazakh word for "Father"?',
                        'order': 1,
                        'answers': [
                            {'answer_text': 'Ана', 'is_correct': False},
                            {'answer_text': 'Әке', 'is_correct': True},
                            {'answer_text': 'Ата', 'is_correct': False},
                            {'answer_text': 'Ұл', 'is_correct': False},
                        ]
                    },
                    {
                        'question_text': 'Which word means "Grandmother" in Kazakh?',
                        'order': 2,
                        'answers': [
                            {'answer_text': 'Әже', 'is_correct': True},
                            {'answer_text': 'Ана', 'is_correct': False},
                            {'answer_text': 'Әпке', 'is_correct': False},
                            {'answer_text': 'Келін', 'is_correct': False},
                        ]
                    },
                    {
                        'question_text': 'What does "Мениң отбасым үлкен" mean?',
                        'order': 3,
                        'answers': [
                            {'answer_text': 'My father is old', 'is_correct': False},
                            {'answer_text': 'I have many brothers', 'is_correct': False},
                            {'answer_text': 'My family is big', 'is_correct': True},
                            {'answer_text': 'My grandfather is tall', 'is_correct': False},
                        ]
                    },
                ]
            },
        ]
        
        # Get levels
        levels = {level.name: level for level in LessonLevel.objects.all()}
        
        for lesson_data in lessons_data:
            # Create or get the lesson
            slug = slugify(lesson_data['title_en'])
            level = levels[lesson_data['level']]
            
            lesson, created = Lesson.objects.get_or_create(
                title_en=lesson_data['title_en'],
                level=level,
                defaults={
                    'title_kz': lesson_data['title_kz'],
                    'description': lesson_data['description'],
                    'content': lesson_data['content'],
                    'order': lesson_data['order'],
                    'slug': slug,
                }
            )
            
            # Add questions and answers
            for q_data in lesson_data['questions']:
                question, q_created = Question.objects.get_or_create(
                    lesson=lesson,
                    order=q_data['order'],
                    defaults={'question_text': q_data['question_text']}
                )
                
                if q_created:
                    # Only add answers if the question was created
                    for a_data in q_data['answers']:
                        Answer.objects.create(
                            question=question,
                            answer_text=a_data['answer_text'],
                            is_correct=a_data['is_correct']
                        )
        
        self.stdout.write(f'Created {len(lessons_data)} lessons with questions and answers') 