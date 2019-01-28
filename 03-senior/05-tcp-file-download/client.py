import socket

def main():

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		ip = input('请输入目标ip:')
		port = input('请输入目标端口:')
		client_socket.connect((ip, int(port)))
	except Exception as res:
		print('连接失败!')
	filename = input('请输入需要下载的文件名:')
	client_socket.send(filename.encode('utf-8'))
	recv_data = client_socket.recv(1024**2)
	if not recv_data:
		print('下载失败!')
	else:
		with open('new_' + filename, 'wb') as file:
			file.write(recv_data)

	client_socket.close()

if __name__ == '__main__':
	main()