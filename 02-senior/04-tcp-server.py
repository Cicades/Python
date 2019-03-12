import socket

def main():
	tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('', 8080)
	tcp_socket.bind(server_address)
	# 监听客户端的请求 128表示并发数,但实际意义并不大,操作系统会影响这个参数
	tcp_socket.listen(128)
	# 接受客户端的请求,其返回值是个元组,可利用拆包来接受
	client_socket, client_addr = tcp_socket.accept() # client_socket用来处理对应客户端的请求
	print('%s已连接!' % (str(client_addr)))
	# 接受客户端的消息
	recv_msg = client_socket.recv(1024)  # 注意与udp的区别
	print('已收到来自%s的请求:\n%s' % (str(client_addr), recv_msg.decode('gbk')))
	# 发送反馈
	client_socket.send('您的信息已送达!'.encode('utf-8'))
	client_socket.close()
	tcp_socket.close()

if __name__ == '__main__':
	main()