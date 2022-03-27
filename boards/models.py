import math

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe
from django.utils.text import Truncator
from markdown import markdown
from taggit.managers import TaggableManager

SHOW_BANNER_COUNT = 5
SHOW_HOTTOPIC_COUNT = 4


# Create your models here.


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.SET_NULL, null=True)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.SET_NULL, null=True)
    tag = TaggableManager()
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

    def get_page_count(self):
        count = self.post.count()
        pages = count / 20
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_last_ten_posts(self):
        return self.post.order_by('-created_at')[:10]


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='post', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='post', on_delete=models.SET_NULL, null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL)

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))


class DocFile(models.Model):
    """
    文件模型
    """
    file_url = models.CharField('文件url', max_length=250, help_text='文件url')
    file_name = models.CharField('文件名', max_length=48, help_text='文件名')
    title = models.CharField('文件标题', max_length=150, help_text='文件标题')
    desc = models.TextField('文件描述', help_text='文件描述')
    image_url = models.CharField('封面图片url', max_length=250, help_text='封面图片url')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        verbose_name = '文件表'  # admin 站点中显示的名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


# def custom_path(instance, filename):
#     ext = filename.split('.')[-1]
#     filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
#     return filename


class Banner(models.Model):
    topic = models.ForeignKey(Topic, null=False, on_delete=models.CASCADE, related_name="banner")
    image_url = models.ImageField(null=True, blank=True, upload_to="img")

    def __str__(self):
        return self.topic


class HotTopics(models.Model):
    topic = models.OneToOneField('Topic', on_delete=models.CASCADE)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        ordering = ['-update_time', '-id']  # 排序
        verbose_name = "热门话题"  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        return '<热门话题{}>'.format(self.id)
