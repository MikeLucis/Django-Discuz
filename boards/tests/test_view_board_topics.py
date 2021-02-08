from django.test.testcases import TestCase
from django.urls import resolve, reverse
from ..views import board_topics
from ..models import Board


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
