import time
import threading

def add_item1(times, mutex):

	global g_num
	for i in range(times):
		mutex.acquire()
		g_num += 1
		mutex.release()
	print('add_item1中的g_num:%d' % g_num)


def add_item2(times, mutex):

	global g_num
	for i in range(times):
		mutex.acquire()
		g_num += 1
		mutex.release()
	print('add_item2中的g_num:%d' % g_num)


def main():
	t1 = threading.Thread(target=add_item1, args=(1000000, mutex))
	t2 = threading.Thread(target=add_item2, args=(1000000, mutex))
	t1.start()
	t2.start()
	time.sleep(3)
	print('main中的g_num:%d' % g_num)


if __name__ == '__main__':
	g_num = 0
	# 定义一个互斥锁
	mutex = threading.Lock()
	main()