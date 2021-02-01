from django.shortcuts import render, get_object_or_404
from .models import Board
from django.http import HttpResponse

# Create your views here.


def home(request):
    boards = Board.objects.all()  # new一个对象，包括board类下所有对象
    return render(request, 'home.html', {'boards': boards})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})

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
