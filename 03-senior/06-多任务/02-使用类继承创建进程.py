import threading
import time


class MyThread(threading.Thread):
	"""使用类继承来创建线程"""
	def run(self):
		time.sleep(1)
		print('子线程执行完毕！')
		

if __name__ == '__main__':
	thread = MyThread()
	thread.start()  # 会默认调用MyThread实例对象中的run方法
	time.sleep(1)
	print('主线程执行完毕！')