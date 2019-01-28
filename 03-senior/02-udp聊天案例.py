import socket


def send_msg(udp_socket):
	"""发送消息"""
	ip = input('请输入目标ip:')
	port = input('请输入目标端口:')
	msg = input('请输入要发送的内容:')
	try:
		udp_socket.sendto(msg.encode('utf-8'), (ip, int(port)))
	except Exception as e:
		print('发送失败:%s!' % e)


def recv_msg(udp_socket):
	"""接受消息"""
	msg = udp_socket.recvfrom(1024)  # 接受数据并指定接受的数据量
	content = msg[0]
	addr = msg[1]
	try:
		print('接收到来自%s的信息:\n%s' % (str(addr), content.decode('gbk')))
	except Exception as res:
		print('数据接受失败:%s' % res)



def main():
	udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# 绑定端口(要接受数据端口应该是固定的)
	udp_socket.bind(('', 8080))
	while True:
		print('*' * 50)
		print('1: 发送信息')
		print('2: 接受消息')
		print('0: 退出程序')
		print('*' * 50)
		operation = input('请输入您要进行的操作:')
		if operation == '1':
			# 发送消息
			send_msg(udp_socket)
		elif operation == '2':
			# 接受消息
			recv_msg(udp_socket)
		elif operation == '0':
			break
		else:
			print('您输入的指令不正确!')
	udp_socket.close()


if __name__ == '__main__':
	main()