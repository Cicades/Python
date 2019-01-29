import threading
import time


def print_msg():
	print('hello world')
	time.sleep(1) # 将程序挂起一秒

def main():
	for i in range(5):
		thread = threading.Thread(target=print_msg)
		thread.start()

if __name__ == '__main__':
	main() # 同时打印五次'hello world'