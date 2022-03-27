from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, QuerySet
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView, ListView
from taggit.models import Tag as Taggit

from .forms import NewTopicForm, PostForm, BannerForm
from .models import Board, Post, Topic, DocFile, Banner, HotTopics, SHOW_BANNER_COUNT, SHOW_HOTTOPIC_COUNT


# Create your views here.

# 基于 GCBV 创建
class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'


class HomeTagsView(View):
    def get(self, request):
        tags = Taggit.objects.values('id', 'name')
        count = len(tags)

        ctx = {
            "count": count,
            "data": {"tags": list(tags)}
        }
        return JsonResponse(data=ctx)


# def home(request):
#     boards = Board.objects.all()  # new一个对象-board类下所有对象
#     return render(request, 'home.html', {'boards': boards})


class SearchListView(ListView):
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


class DownloadDocListView(ListView):
    """
    文档列表视图
    """
    model = DocFile
    template_name = 'download.html'
    context_object_name = 'docs'

    def get_queryset(self):
        queryset = DocFile.objects.order_by('-created_at')
        return queryset


# 基于 GCBV 创建
class TopicListView(ListView):
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


# def board_topics(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     queryset = board.topics.order_by('-last_updated').annotate(replies=Count('post') - 1)
#     page = request.GET.get('page', 1)
#
#     paginator = Paginator(queryset, 20)
#
#     try:
#         topics = paginator.page(page)
#     except PageNotAnInteger:
#         # 返回第一页
#         topics = paginator.page(1)
#     except EmptyPage:
#         # 当用户是否尝试添加页码
#         # 若在url中，则回退到最后一页
#         topics = paginator.page(paginator.num_pages)
#
#     return render(request, 'topics.html', {'board': board, 'topics': topics})


@login_required
def new_topic(request, pk):
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


# 显示回复条数
class PostListView(ListView):
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


# def topic_posts(request, pk, topic_pk):
#     topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
#     topic.views += 1
#     topic.save()
#     return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def reply_topic(request, pk, topic_pk):
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
# 使用 method 传递装饰器
@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
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


class TopicBannerView(View):
    """
    轮播图
    GET /news/banners/
    """

    def get(self, request):
        # 读取到图片,文章id和标题, 由于标题是外键, 发送json的话就需要重命名
        banner = Banner.objects.values('image_url', 'topic_id').annotate(
            topic_title=F('topic__subject'), board_id=F('topic__board__id'))[:SHOW_BANNER_COUNT]
        count = len(banner)
        ctx = {
            "count": count,
            "errmsg": "OK",
            "data": {'banners': list(banner)}
        }
        return JsonResponse(data=ctx)


class HotTopicView(View):
    def get(self, request):
        data = []
        hot_topics = HotTopics.objects.all().order_by('-topic__views')[:SHOW_HOTTOPIC_COUNT]
        count = len(hot_topics)
        for tp in hot_topics:
            tp_item = model_to_dict(tp.topic, fields=['id', 'subject', 'board'])
            tp_item['image_url'] = Banner.objects.get(topic_id=tp.topic.id).image_url.url
            data.append(tp_item)

        ctx = {
            'count': count,
            'data': {'topics': data}
        }

        return JsonResponse(data=ctx)
