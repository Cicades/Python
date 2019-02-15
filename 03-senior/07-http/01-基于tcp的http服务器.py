import socket
import re

def client_service(new_client):
	"""处理客户端发过来的请求"""
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
	while True:
		new_client, client_addr = tcp_socket.accept()
		client_service(new_client)
		new_client.close()
	tcp_socket.close()

if __name__ == '__main__':
	main()