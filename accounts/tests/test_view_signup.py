from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from ..forms import SignUpForm
from ..views import signup


# Create your tests here.


# 常规类测试
class SignUpTests(TestCase):
    # 创建⼀个测试中使⽤的 SignUp 实例
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    # 测试状态码 （200=success
    def test_signup_status_code(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    # URL /signup/ 是否传回正确视图函数
    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

    # CSRF Token 预留
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    # 抓取上下文表单实例，检查它是否为 UserCreationForm
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    # 验证模板 HTML字段输入
    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


# 账户注册成功性检测
class SuccessfulSignUpTests(TestCase):
    # 创建⼀个测试中使⽤的 SignUp 账户
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'Jack',
            'email': 'mike@lucis.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    #
    def test_redirection(self):
        self.assertRedirects(self.response, self.home_url)

    #
    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    #
    def test_user_authentication(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


# 数据无效性检测
class InvalidSignUpTest(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})

    #
    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    #
    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    #
    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
