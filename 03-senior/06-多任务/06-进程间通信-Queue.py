import multiprocessing


def get_msg(queue):
	"""往队列中取数据"""
	try:
		while True:
			print('取出数据：%d' % queue.get(True, 1))  # 超过一秒还没取到数据就抛出异常
	except:
		print('数据读取完毕！')


def send_msg(queue):
	"""往队列中存数据"""
	for i in range(9):
		queue.put(i)
		print('放入数字%d' % i)
	else:
		return


def main():

	queue = multiprocessing.Queue(3)  # 队列的长度为3，可以不规定队列的长度
	pr_get_msg = multiprocessing.Process(target=get_msg, args=(queue,))
	pr_send_msg = multiprocessing.Process(target=send_msg, args=(queue,))
	pr_get_msg.start()
	pr_send_msg.start()
	# 等待两个子进程执行完毕
	# pr_get_msg.join()
	# pr_send_msg.join()


if __name__ == '__main__':
	main()