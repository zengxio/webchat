from 阶段2.s4 import Future
from 阶段2.s4 import HttpResponse
from 阶段2.s4 import Snow

request_list = []
#异步非阻塞 手动关闭sock

def callback(request, future):
    return HttpResponse(future.value)


def req(request):
    print('请求到来')
    obj = Future(callback=callback)
    request_list.append(obj)
    yield obj


def stop(request):
    obj = request_list[0]
    del request_list[0]
    obj.set_result('done')
    return HttpResponse('stop')


routes = [
    (r'/req/', req),
    (r'/stop/', stop),
]

app = Snow(routes)
app.run(port=8012)