from django.test import TestCase, Client

from authuser.models import User
from .models import Categories, Note
from .views import check_status_category_name as cat_name
from django.utils import timezone
from datetime import timedelta

# run - python manage.py test todo_list

class CheckStatusCategoryNameTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser', password='password')
        self.client = Client()
        self.client.force_login(self.user)

    def test_category_exists(self):
        category_name = 'Работа'
        Categories.objects.create(user=self.user, name=category_name)
        function_input = 'работа'
        mock_self = type('MockSelf', (object,), {'request': type('MockRequest', (object,), {'user': self.user})()})
        result = cat_name(mock_self, function_input)
        print(f"\n-----Тест на проверку по регистру-----")
        print(f"DB: {category_name}, Search: {function_input}, result function: {result}")
        self.assertFalse(result)

    def test_category_not_exists(self):
        function_input = 'Отпуск'
        mock_self = type('MockSelf', (object,), {'request': type('MockRequest', (object,), {'user': self.user})()})
        result = cat_name(mock_self, function_input)
        print(f"\n-----Тест на проверку по возможности добавления-----")
        print(f"DB: None, Search: {function_input}, result function: {result}")
        self.assertTrue(result)


    def test_case_insensitive(self):
        category_name = 'Проекты'
        Categories.objects.create(user=self.user, name=category_name)
        function_input = 'пРоЕкТы'
        mock_self = type('MockSelf', (object,), {'request': type('MockRequest', (object,), {'user': self.user})()})
        result = cat_name(mock_self, function_input)
        print(f"\n-----Тест на проверку по регистру-----")
        print(f"DB: {category_name}, Search: {function_input}, result function: {result}")
        self.assertFalse(result)

    def test_case_insensitive1(self):
        category_name = 'Проекты1'
        Categories.objects.create(user=self.user, name=category_name)
        function_input = 'пРоЕкТы'
        mock_self = type('MockSelf', (object,), {'request': type('MockRequest', (object,), {'user': self.user})()})
        result = cat_name(mock_self, function_input)
        print(f"\n-----Тест на проверку по регистру-----")
        print(f"DB: {category_name}, Search: {function_input}, result function: {result}")
        self.assertTrue(result)





class NoteModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser', password='password')
        self.client = Client()
        self.client.force_login(self.user)

        self.category = Categories.objects.create(user=self.user, name='Тесты')

    def test_time_left_no_deadline(self):
        note = Note.objects.create(category=self.category, title='Note1', description='desc', color='green')
        result = note.time_left
        print(f"Тест: test_time_left_no_deadline, Ожидаемый результат: Нет дедлайна, Результат: {result}")
        self.assertEqual(result, "Нет дедлайна")

    def test_time_left_past_deadline(self):
        deadline = timezone.now() - timedelta(days=2)
        note = Note.objects.create(category=self.category, title='Note2', description='desc', color='green', deadline=deadline)
        result = note.time_left
        print(f"Тест: test_time_left_past_deadline, Ожидаемый результат: Просрочено, Результат: {result}")
        self.assertEqual(result, "Просрочено")

    def test_time_left_future_deadline(self):
        deadline = timezone.now() + timedelta(days=5, hours=3, minutes=30)
        note = Note.objects.create(category=self.category, title='Note3', description='desc', color='red', deadline=deadline)
        result = note.time_left
        print(f"Тест: test_time_left_future_deadline, Ожидаемый результат: 5 дней 3 часов 30 минут, Результат: {result}")
        self.assertEqual(result, "5 дней 3 часов 29 минут")

    def test_time_left_today(self):
        deadline = timezone.now() + timedelta(hours=2)
        note = Note.objects.create(category=self.category, title='Note4', description='desc', color='orange', deadline=deadline)
        result = note.time_left
        print(f"Тест: test_time_left_today, Ожидаемый результат: 1 часов 59 минут, Результат: {result}")
        self.assertTrue("1 часов 59 минут" in result)
