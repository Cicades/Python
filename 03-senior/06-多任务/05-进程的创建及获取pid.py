import time
import multiprocessing
import os

def test():
	"""子线程"""
	# os.getpid => 当前线程pid，os.getppid =>父线程pid
	time.sleep(1)
	print('test线程的pid为:%d,父线程的pid为：%d' % (os.getpid(), os.getppid()))


def main():

	po = multiprocessing.Process(target=test)
	po.start()
	time.sleep(1)
	print('main线程的pid为:%d,父线程的pid为：%d' % (os.getpid(), os.getppid()))


if __name__ == '__main__':
	main()