from socket import *

def main():
		
	# 1.创建套接字
	udp_socket = socket(AF_INET, SOCK_DGRAM)
	while True:
	
		# 2.准备发送内容
		send_data = input('请输入要发送的内容(exit退出):')
		if send_data == 'exit':
			break
		# 3.准备接受方地址
		dest_addr = ('192.168.22.1', 8080)

		# 4.发送数据
		# b可以将字符转换为二进制数据
		# udp_socket.sendto(b'hello world', dest_addr)
		udp_socket.sendto(send_data.encode('utf-8'), dest_addr)
	# 5.关闭套接字
	udp_socket.close()

if __name__ == '__main__':
	main()


