from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, QuerySet
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView, ListView
from taggit.models import Tag as Taggit

from utils.JsonResponse import json_response
from .forms import NewTopicForm, PostForm, BannerForm
from .models import Board, Post, Topic, DocFile, Banner, HotTopics, SHOW_BANNER_COUNT, SHOW_HOTTOPIC_COUNT


# Create your views here.

# 基于 GCBV 创建
class BoardListView(ListView):
    """
    版块列表-视图
    """
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        kwargs['home'] = True
        return super().get_context_data(**kwargs)


# 基于 GCBV 创建
class TopicListView(ListView):
    """
    话题列表-视图
    """
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('post') - 1)
        return queryset


@login_required
def new_topic(request, pk):
    """
    新建话题-视图
    """
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        banner = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            form.save_m2m()
            if banner.is_valid():
                image = banner.cleaned_data['image_url']
                banner = Banner.objects.create(topic_id=topic.id, image_url=image)
                banner.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        banner = BannerForm()
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form, 'banner': banner})


@login_required
def reply_topic(request, pk, topic_pk):
    """
    回复话题-视图
    """
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


# 基于 GCBV 创建
class PostListView(ListView):
    """
    回复列表-视图
    """
    topic: Topic
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.post.order_by('created_at')
        return queryset


# 基于 GCBV 创建
@method_decorator(login_required, name='dispatch')  # 使用 method 传递装饰器
class PostUpdateView(UpdateView):
    """
    修改回复-视图
    """
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        # 重用父类
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


# 基于 GCBV 创建
class DownloadDocListView(ListView):
    """
    下载文档列表-视图
    """
    model = DocFile
    template_name = 'download.html'
    context_object_name = 'docs'

    def get_context_data(self, **kwargs):
        kwargs['search'] = True
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        queryset = DocFile.objects.order_by('-created_at')
        return queryset


# 基于 GCBV 创建
class SearchListView(ListView):
    """
    搜索列表-视图
    （搜索话题、按标签查询）
    """
    model = Topic
    context_object_name = 'results'
    template_name = 'topic_list.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        ctx = {}
        if self.sec:
            ctx['goal'] = self.sec
            ctx['count'] = self.count
        if self.tag:
            ctx['goal'] = self.tag
            ctx['count'] = self.count

        kwargs['page'] = ctx
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.sec = self.request.GET.get('sec')
        self.tag = self.request.GET.get('tag')

        topic_list = Topic.objects.all()

        if self.sec:
            queryset = topic_list.filter(subject__icontains=self.sec)
            self.count = len(queryset)
        elif self.tag:
            queryset = topic_list.filter(tag__name__in=[self.tag])
            self.count = len(queryset)
        else:
            queryset = QuerySet()
        return queryset


class TopicBannerView(View):
    """
    轮播图-接口
    GET /boards/banners/
    """

    def get(self, request):
        banner = Banner.objects.values('image_url', 'topic_id').annotate(
            topic_title=F('topic__subject'), board_id=F('topic__board__id'))[:SHOW_BANNER_COUNT]
        count = len(banner)
        return json_response(data={"count": count, 'banners': list(banner)})


class HomeTagsView(View):
    """
    主页最新话题标签-接口
    GET /boards/tags/
    """

    def get(self, request):
        tags = Taggit.objects.values('id', 'name')
        count = len(tags)
        return json_response(data={"count": count, "tags": list(tags)})


class HotTopicView(View):
    """
    最热话题-接口
    GET /boards/hotopics/
    """

    def get(self, request):
        data = []
        hot_topics = HotTopics.objects.all().order_by('-topic__views')[:SHOW_HOTTOPIC_COUNT]
        count = len(hot_topics)
        for tp in hot_topics:
            tp_item = model_to_dict(tp.topic, fields=['id', 'subject', 'board'])
            tp_item['image_url'] = Banner.objects.get(topic_id=tp.topic.id).image_url.url
            data.append(tp_item)
        return json_response(data={'count': count, 'topics': data})
