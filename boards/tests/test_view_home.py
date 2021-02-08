from django.test.testcases import TestCase
from django.urls import reverse, resolve
from ..views import home
from ..models import Board


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
