import socket
import re
import select

def client_service(new_client):
    """处理客户端的请求"""
    request = new_client.recv(1024).decode('utf-8')
    request_lines = request.splitlines()
    request_target = re.match(r'[^/]+([^ ]+)', request_lines[0]).group(1)
    request_target = request_target if request_target != '/' else '/index.html'
    print(request_target)
    try:
        file = open('./html' + request_target, 'rb')
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
    finally:
        new_client.close()

def main():
    
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(('', 80))
    tcp_socket.listen(128)
    epl = select.epoll()
    epl.register(tcp_socket.fileno(), select.EPOLLIN)  # 将监听套接字的fd注册到epoll中并设置被触发的事件类型
    client_socket_dict = dict()
    while True:
        fd_event_list = epoll()  # 获取触发的套接字列表
        for fd, event in fd_event_list:
            if fd == tcp_socket.fileno():
                """监听套接字触发，意味着有新的客户端请求连接"""
                new_client, client_addr = tcp_socket.accept()
                epl.register(new_client, select.EPOLLIN)
                client_socket_dict[new_client.fileno()] = new_client
            elif event == select.EPOLLIN:
                """客户端套接字发送请求"""
                client_service(client_socket_dict[fd])
                epl.unregister(fd)  # 处理完请求从epoll中吊销对应的fd
                del fd_event_list[fd]

if __name__ == '__main__':
    main()
