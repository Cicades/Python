import socket


def main():
	tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_server.bind(('', 8080))
	tcp_server.listen(128)
	tcp_client, client_addr = tcp_server.accept()
	filename = tcp_client.recv(1024).decode('utf-8')
	try:
		file = open(filename, 'rb')
		content = file.read()
		send_msg = content
	except Exception as res:
		print('文件读取失败:%s' % res)
		send_msg = ''
	finally:
		tcp_client.send(send_msg.encode('utf-8'))
	# 关闭客户端套接字
	tcp_client.close()
	# 关闭服务端套接字
	tcp_server.close()

if __name__ == '__main__':
	main()