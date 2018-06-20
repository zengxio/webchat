#!/usr/bin/env python
#encoding:utf-8
#异步非阻塞:
  #阻塞式：（django，flask，tornado，bottle）
  #一个请求到来未处理完成，后续一直等待
  #解决方案:多线程或多进程
    # from tornado.httpserver import HTTPServer
    # import tornado.ioloop
    # server = HTTPServer(application)
    # server.bind(9999)
    # server.start(4)  # 开的进程数
    # tornado.ioloop.IOLoop.current().start()

#异步分阻塞（存在io请求）:tornado
#模拟1
# import tornado.ioloop
# import tornado.web #tornado.web.RequestHandler引用
# from tornado.web import RequestHandler
# from tornado import gen
# from tornado.concurrent import Future
# import time
#
# class IndexHandler(RequestHandler):
#     @gen.coroutine
#     def get(self):
#         print('开始')
#         future=Future()
#         tornado.ioloop.IOLoop.current().add_timeout(time.time() + 5,self.doing)
#         yield future
#     def doing(self,*args,**kwargs):
#         self.write('hello world')
#         self.finish()
#
#
#
# application = tornado.web.Application([
#     (r"/index", IndexHandler),
# ])
#
#
# if __name__ == "__main__":
#     application.listen(8888) #监听8888端口
#     tornado.ioloop.IOLoop.instance().start() #启动程序
#     # server = HTTPServer(application)
#     # server.bind(9999)
#     # server.start(4)  #开的进程数
    # tornado.ioloop.IOLoop.current().start()

#模拟2
# import tornado.ioloop
# import tornado.web #tornado.web.RequestHandler引用
# from tornado.web import RequestHandler
# from tornado import gen
# from tornado.concurrent import Future
# import time
# from tornado import httpclient
#
# class IndexHandler(RequestHandler):
#     @gen.coroutine
#     def get(self):
#         print('开始')
#         http=httpclient.AsyncHTTPClient()
#         #模拟发送http请求
#         yield http.fetch("http://www.github.com",self.doing)
#
#     def doing(self,response):
#         self.write('hello world')
#         self.finish()
#
#
#
# application = tornado.web.Application([
#     (r"/index", IndexHandler),
# ])
#
#
# if __name__ == "__main__":
#     application.listen(8888) #监听8888端口
#     tornado.ioloop.IOLoop.instance().start() #启动程序

#模拟3
import tornado.ioloop
import tornado.web #tornado.web.RequestHandler引用
from tornado.web import RequestHandler
from tornado.concurrent import Future
from tornado import gen
import time
from tornado import httpclient
from threading import Thread
def waiting(futher):
    time.sleep(10)
    futher.set_result(1000)  #执行完成设置为True。执行doing函数。如果不设置，这个请求不会挂断

class IndexHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        print('开始')
        fu=Future()
        fu.add_done_callback(self.doing)
        thread=Thread(target=waiting,args=(fu,))
        thread.start()
        yield fu


    def doing(self,response):
        self.write('hello world')
        self.finish()



application = tornado.web.Application([
    (r"/index", IndexHandler),
])


if __name__ == "__main__":
    application.listen(8888) #监听8888端口
    tornado.ioloop.IOLoop.instance().start() #启动程序


#pip install Tornado-MysQL