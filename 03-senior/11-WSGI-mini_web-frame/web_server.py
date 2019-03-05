import socket
import re
import multiprocessing
import dynamic.mini_frame
import sys

class WSGIServer(object):
    """WSGI服务器封装"""
    def __init__(self, port, app, static_path):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.bind(('', port))
        self.tcp_socket.listen(128)
        self.app = app
        self.static_path = static_path
        print('server is running at localhost:%d...' % port)

    def client_service(self, new_client):
        """处理客户端发过来的请求"""
        request = new_client.recv(1024).decode('utf-8')
        request_lines = request.splitlines()
        request_target = re.match(r'[^/]+([^ ]+)', request_lines[0]).group(1)
        request_target = request_target if request_target != '/' else '/index.py'
        print('the request url is %s' % request_target)
        if not request_target.endswith('.py'):
            """响应静态资源"""
            try:
                file = open(self.static_path + request_target, 'rb')
            except:
                response_header = 'HTTP/1.1 404 NOT FOUND\r\n\r\n'
                response_body = '<h1>file not exists</h1>'
                response = response_header + response_body
                new_client.send(response.encode('utf-8'))
            else:
                response_header = 'HTTP/1.1 200 OK\r\n\r\n'
                new_client.send(response_header.encode('utf-8'))
                response_body = file.read()
                new_client.send(response_body)
                file.close()
        else:
            """响应动态资源，为实现更好的解耦需要调用web frame来做，但web frame要实现WSGI协议"""
            env = dict()  # 存储服务器传给frame的数据
            env['url'] = request_target
            # body = dynamic.mini_frame.application(env, self.set_response_header)
            body = self.app(env, self.set_response_header)
            header = 'HTTP/1.1 %s\r\n' % self.status
            for item in self.headers:
                header +='%s:%s\r\n' % (item[0], item[1])
            header += '\r\n'
            # print(header, body)
            response_content = (header + body).encode('utf-8')
            new_client.send(response_content)
        new_client.close()


    def set_response_header(self, status, headers):
        """接受frame传递过来的headers信息"""
        self.status = status
        self.headers = headers


    def run(self):
        while True:
            new_client, client_addr = self.tcp_socket.accept()
            p = multiprocessing.Process(target=self.client_service, args=(new_client,))
            p.start()
            new_client.close()
        self.tcp_socket.close()


def main():
    if len(sys.argv) == 3:
        port = int(sys.argv[1])
        ret = re.match(r'([^:]+):(.*)', sys.argv[2])
        frame_path = ret.group(1)  # 框架的名字
        app_path = ret.group(2)  # 框架application入口
        print(port, frame_path, app_path)
        with open('./web_server.config', encoding='utf8') as f:
            """解析配置文件"""
            server_config = eval(f.read())
        dynamic_path = server_config['dynamic_path']  # 服务器框架路径
        static_path = server_config['static_path']  # 静态资源路径
        print(dynamic_path, static_path)
        sys.path.append(dynamic_path)  # 将框架路径添加到包查询路径
        frame = __import__(frame_path)  # 导入框架文件
        app = getattr(frame, app_path)  # 获取框架中的application入口
        web_server = WSGIServer(port, app, static_path)
        web_server.run()
    else:
        print('please run the server with true format:python web_server.py <port> <frame:application>!')

if __name__ == '__main__':
    main()