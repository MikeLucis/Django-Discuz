from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase
from .views import home, board_topics, new_topic
from .models import Board, Topic, Post

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

    # 使⽤ assertContains ⽅法来测试 response 主体部分是否包含href, 确保 view 包含所需的导航链接
    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))


class NewTopicTests(TestCase):
    # 创建⼀个测试中使⽤的 Board 实例
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        User.objects.create_user(username='mike', email='mike@lucis.site', password='123')

    # 检查发给 view 的请求是否成功
    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    # 检查当 Board 不存在时 view 是否会抛出⼀个 404 的错误
    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    # 检查是否正在使⽤正确的 view
    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    # 确保导航能回到 topics 的列表
    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    # CSRF Token 预留
    def test_csrf(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    # 发送有效的数据并检查视图函数是否创建了 Topic 和 Post 实例
    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    # 发送⼀个空字典来检查应⽤的⾏为
    def test_new_topic_invalid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    # 类似于上⼀个测试，但是这次我们发送⼀些数据。预期应⽤程序会验证并且拒绝空的 subject 和 message
    def test_new_topic_invalid_post_data_empty_fields(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())
