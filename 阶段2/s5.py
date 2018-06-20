from 阶段2.s4 import HttpResponse
from 阶段2.s4 import Snow


def index(request):
    return HttpResponse('OK')


routes = [
    (r'/index/', index),
]

app = Snow(routes)
app.run(port=8012)