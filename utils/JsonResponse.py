import datetime
import json

from django.http import JsonResponse

from .ResCode import Code


# json编码器
# 自定义序列化器，处理时间字段
class MyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            # 转换为本地时间
            return o.astimezone().strftime('%Y-%m-%d %H:%M:%S')


def json_response(errno=Code.OK, errmsg='OK', data=None, kwargs=None):
    """
    该方法实现的目的是为了使json数据在传输过程中,能够携带错误代码之类的信息
    :param errno: 错误代码
    :param errmsg: 错误信息
    :param data: 携带的用户信息数据,例如用户名,手机号等
    :return: 返回的相当于是我们处理好的json响应
    """
    json_dict = {
        'errno': errno,
        'errmsg': errmsg,
        'data': data,
    }
    if kwargs and isinstance(kwargs, dict):
        # 判断kwargs中是否有传输数据信息, 有则更新我们已有的信息
        json_dict.update(kwargs)
    return JsonResponse(json_dict, encoder=MyJSONEncoder)
