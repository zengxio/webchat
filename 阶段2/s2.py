#!/usr/bin/env python
#encoding:utf-8

import socket
import select

def f1(request):
    return '内容1'

def f2(request):
    return '内容2'

urls=[
    ('/index.html',f1),
    ('/home.html',f2)
]

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.setblocking(False)
sock.bind(('127.0.0.1',9999,))
sock.listen(55)

input_list=[sock,]

while True:
    rlist,wlist,elist=select.select(input_list,[],[],0.005)
    for sk in rlist:
        #新连接 sock
        #发来数据 client
        if sk == sock:
            client,address=sock.accept()
            client.setblocking(False)
            input_list.append(client)
        else:
            data=sk.recv(8096)
            response=f1(data)

            sk.sendall(response.encode('utf-8'))
            sk.close()


