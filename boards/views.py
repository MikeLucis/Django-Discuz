from django.shortcuts import render
from .models import Board
from django.http import HttpResponse

# Create your views here.


def home(request):
    boards = Board.objects.all()  # new一个对象，包括board类下所有对象
    return render(request, 'home.html', {'boards': boards})

    # 老版
    # boards_name = list()  # 创建列表
    # for board in boards:  # 遍历类下所有对象并添加到列表中
    #     boards_name.append(boards_name)
    # response_html = '<br>'.join(boards_name)
    # return HttpResponse(response_html)

