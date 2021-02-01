from django.urls import reverse, resolve
from django.test import TestCase
from .views import home, board_topics
from .models import Board

# Create your tests here.


class HomeTests(TestCase):
    # 设置测试用数据库
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        url = reverse('home')
        self.response = self.client.get(url)

    # 请求该URL后返回的响应状态码。状态码200（成功）
    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        # url = reverse('home')
        # response = self.client.get(url)
        # self.assertEquals(response.status_code, 200)

    # 将浏览器发起请求的URL与urls.py模块中列出的URL进⾏匹配
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    # 使⽤ assertContains ⽅法来测试 response 主体部分是否包含href
    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))


class BoardTopicsTests(TestCase):
    # 设置测试用数据库
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')

    # 测试 Django 是否对于现有的 Board 返回 status code(状态码) 200(成功)
    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    # 测试 Django 是否对于不存在于数据库的 Board 返回 status code 404(⻚⾯未找到)
    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    # 测试 Django 是否使⽤了正确的视图函数去渲染 topics
    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)

    # 使⽤ assertContains ⽅法来测试 response 主体部分是否包含href
    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))