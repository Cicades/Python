import socket
import threading


def send_msg(udp_socket):
	while True:
		ip = input('请输入目标主机ip：')
		port = input('请输入目标主机端口：')
		msg = input('请输入要发送的内容：')
		udp_socket.sendto(msg.encode('gbk'), (ip, int(port)))


def recv_msg(udp_socket):
	while True:
		recv_content = udp_socket.recvfrom(1024)
		sender_addr = recv_content[1]
		recv_message = recv_content[0].decode('gbk')
		print('收到来自%s:%d的消息：\n%s' % (sender_addr[0], sender_addr[1], recv_message))


def main():
	udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udp_socket.bind(('', 3000))
	# 发送消息
	send_thread = threading.Thread(target=send_msg, args=(udp_socket, ))
	send_thread.start()
	# 接受消息
	# recv_thread = threading.Thread(target=recv_msg, args=(udp_socket,))
	# recv_thread.start()
	udp_socket.close()

if __name__ == '__main__':
	main()