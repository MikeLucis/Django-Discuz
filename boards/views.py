from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Post
from .froms import NewTopicForm


# Create your views here.


def home(request):
    boards = Board.objects.all()  # new一个对象-board类下所有对象
    return render(request, 'home.html', {'boards': boards})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # TODO: 获取当前登录的用户
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', pk=board.pk)  # TODO: 重定向到创建的主题页
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})

    # 老版
    # board = Board.objects.get(pk=pk)
    # board = Board.objects.get(pk=pk)
    # return render(request, 'topics.html', {'board': board})

    # 老版
    # boards_name = list()  # 创建列表
    # for board in boards:  # 遍历类并添加到列表
    #     boards_name.append(boards_name)
    # response_html = '<br>'.join(boards_name)
    # return HttpResponse(response_html)
