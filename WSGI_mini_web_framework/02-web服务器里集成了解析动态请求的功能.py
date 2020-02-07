import socket
import re
import multiprocessing
import time

###############################################################
###################修改代码为面向对象的web_server###############
###############################################################

class WSGIServer(object):
    def __init__(self):
        """完成整体控制"""
        # 创建套接字
        self.tcp_server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        # 绑定
        self.tcp_server_socket.bind(("169.254.112.42",6688))
        # 变成监听套接字
        self.tcp_server_socket.listen(128)

    # 成为一个实例方法
    def server_client(self,new_socket):
        """为这个客户端返回数据"""
        # 1.接收浏览器发过来的数据 HTTP请求
        # GET HTTP/1.1
        # .......
        request=new_socket.recv(1024).decode("utf-8")
        request_lines=request.splitlines()
        #print("")
        #print(">"*200)
        #print(response_lines)

        # GET /index.html HTTP/1.1
        # get put post del
        file_name=""
        #  正则表达匹配网站名
        ret=re.match(r"[^/]+(/[^ ]*)",request_lines[0])   # 正则表达式要写正确
        if ret:
            file_name=ret.group(1)
            print(file_name)
            if file_name=="/":
                file_name="/Home _ Qt Forum..html"

        # 2.返回给浏览器http格式的数据  response
        # 2.1 如果请求的资源不是以.py结尾的，那么就认为是静态资源(html/css/js/png/jpg)
        if not file_name.endswith(".py"):
            try:
                f=open("./html"+file_name,"rb")
            except:
                response="HTTP/1.1 404 NOT FOUND\r\n"
                response+="\r\n"
                response+="=====file not found====="
                new_socket.send(response.encode("utf-8"))
            else:
                html_content=f.read()
                f.close()
                # 2.1发送header给浏览器
                response="HTTP/1.1 200 OK\r\n"  # 对于windows系统 换行空行是 ：\r\n
                response+="\r\n"     #表示换行空行（\r\n）

                # 2.2发送body给浏览器
                # 将response header发送给浏览器
                new_socket.send(response.encode("utf-8"))
                # 将response body发送给浏览器
                new_socket.send(html_content)
        else:
            #2.2如果1请求的资源是.py，那么就是动态资源
            header="HTTP/1.1 200 OK \r\n"
            header+="\r\n"

            body="hahahahaa %s" % time.ctime()
            response=header+body
            # 将response header发送给浏览器
            new_socket.send(response.encode("utf-8"))

            # 关闭套接字
        new_socket.close()


    def run_forever(self):

        while True:
            # 等待新客户的链接
            new_socket,client_addr=self.tcp_server_socket.accept()
            # 为这个客户服务
            p=multiprocessing.Process(target=self.server_client,args=(new_socket,))
            p.start()
            new_socket.close()
        # 关闭监听套接字
        self.tcp_server_socket.close()
def main():
    #控制整体，创建一个Web服务对象，然后调用这个对象的run_forever方法运行
    wsgi_server=WSGIServer()
    wsgi_server.run_forever()

if __name__=="__main__":
    main()
