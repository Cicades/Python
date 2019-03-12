import socket


def main():
	# 创建套接字
	tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ip = input('请输入服务器地址:')
	port = input('请输入服务器端口:')
	tcp_socket.bind(('', 8080))
	try:
		# 与服务器建立连接
		tcp_socket.connect((ip, int(port)))
		rev_msg = tcp_socket.recv(1024)
		print('收到数据为:%s' % rev_msg.decode('gbk'))

	except Exception as res:
		print('连接失败:输入的信息不正确!')

	tcp_socket.close()

if __name__ == '__main__':
	main()