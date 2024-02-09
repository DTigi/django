from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from women.models import Women


# Create your tests here.


class GetPagesTestCase(TestCase):
    fixtures = ['women_women.json', 'women_category.json', 'women_husband.json', 'women_tagpost.json']

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

    def test_data_mainpage(self):
        '''Тест содержимого главной страницы (на соответствие с данными из БД)'''
        w = Women.published.all().select_related('cat')
        path = reverse('home')
        response = self.client.get(path)
        #Метод assertQuerysetEqual() позволяет сравнивать два разных QuerySet. Первый мы берем из ответа клиенту из коллекции context_data (ключ ‘posts’ мы определяем в классе WomenHome), а второй – напрямую из тестовой БД. Срез до пяти берется из-за наличия пагинации при отображении списка по пять постов. Поэтому мы должны видеть первые пять записей.
        self.assertQuerysetEqual(response.context_data['posts'], w[:5])

    def test_paginate_mainpage(self):
        '''тест, который будет проверять работу пагинации главной страницы'''
        path = reverse('home')
        page = 2
        paginate_by = 5
        response = self.client.get(path + f'?page={page}')
        w = Women.published.all().select_related('cat')
        self.assertQuerysetEqual(response.context_data['posts'], w[(page - 1) * paginate_by:page * paginate_by])

    def test_content_post(self):
        '''проверка содержимого страницы отображения поста'''
        w = Women.published.get(pk=1)
        path = reverse('post', args=[w.slug])
        response = self.client.get(path)
        self.assertEqual(w.content, response.context_data['post'].content)

    def tearDown(self):
        "Действия после выполнения каждого теста"
