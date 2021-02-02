from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Topic, Post
from django.http import HttpResponse

# Create your views here.


def home(request):
    boards = Board.objects.all()  # new一个对象，包括board类下所有对象
    return render(request, 'home.html', {'boards': boards})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)

    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']

        user = User.objects.first()  # TODO: 临时使用一个账号作为登录用户

        topic = Topic.objects.create(
            subject=subject,
            board=board,
            starter=user
        )

        post = Post.objects.create(
            message=message,
            topic=topic,
            created_by=user
        )
        return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    return render(request, 'new_topic.html', {'board': board})

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
