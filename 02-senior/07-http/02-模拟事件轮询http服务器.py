import socket
import re

def client_service(new_client):
    try:
        request = new_client.recv(1024).decode('utf-8')
    except:
        print('no request!')
        return
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
    tcp_socket.setblocking(False)  # ½«Ì×½Ó×ÖÉèÖÃÎª·Ç¶ÂÈûµÄ
    clients = list()
    while True:
        try:
            new_client, client_addr = tcp_socket.accept()
            new_client.setblocking(False)
        except:
            # print('no new client!')
            pass
        else:
            clients.append(new_client)
            print(client_addr)
        for client in clients:
            client_service(client)        
            clients.remove(client)
                

if __name__ == '__main__':
    main()
