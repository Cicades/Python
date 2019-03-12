import gevent
import time
from gevent import monkey

monkey.patch_all()

def task1():
	for i in range(5):
		print('task1执行...')
		time.sleep(1)


def task2():
	for i in range(9):
		print('task2执行...')
		time.sleep(1)


def task3():
	for i in range(10):
		print('task3执行...')
		time.sleep(1)


def main():
	ge1 = gevent.spawn(task1)
	ge2 = gevent.spawn(task2)
	ge3 = gevent.spawn(task3)
	# ge1.join()
	# ge2.join()
	# ge3.join()
	gevent.joinall([ge1, ge2, ge3])

if __name__ == '__main__':
	main()