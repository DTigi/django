from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


# Create your tests here.


class GetPagesTestCase(TestCase):
    def setUp(self):
        "Инициализация перед выполнением каждого теста"

    def test_mainpage(self):
        '''Проверка получения главной страницы'''
        path = reverse('home') # вычисляем URL-адрес главной страницы
        response = self.client.get(path) # имитация get-запроса от браузера для получения главной страницы
        self.assertEqual(response.status_code, HTTPStatus.OK) # проверка на равенство. Убедимся, что страница успешно возвращается клиенту (код 200)
        # self.assertIn('women/index.html', response.template_name) # проверяет вхождение значения(шаблона) в коллекцию данных (template_name - список из набора наследуемых и расширяемых шаблонов )
        self.assertTemplateUsed(response, 'women/index.html') # для проверки использования того или иного шаблона есть свой отдельный метод assertTemplateUsed()
        self.assertEqual(response.context_data['title'], 'Главная страница') # проверка на равенство

    def test_redirect_addpage(self):
        '''тест, который будет проверять перенаправление со страницы: http://127.0.0.1:8000/addpage/
на страницу авторизации для неавторизованных пользователей'''
        path = reverse('add_page')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND) # проверка кода статуса 302 страницы addpage
        self.assertRedirects(response, redirect_uri) # проверка перенаправления на страницу с URL-адресом redirect_uri

    def tearDown(self):
        "Действия после выполнения каждого теста"
