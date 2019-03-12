import os
import multiprocessing

def copy_file(old_folder_name, new_folder_name, filename, queue):
	"""复制文件"""
	with open(os.path.join(old_folder_name, filename), 'rb') as old_file:
		new_file = open(os.path.join(new_folder_name, filename), 'wb')
		new_file.write(old_file.read())
		new_file.close()
		queue.put(filename)


def main():
	"""程序主函数"""
	# 获取需拷贝的文件夹
	old_folder_name = input('请输入需要拷贝的文件夹名：')
	if not os.path.exists(old_folder_name):
		print('不存在指定的文件夹！')
		return
	# 新建文件夹
	new_folder_name = input('请输入新建的文件夹名：')
	if os.path.exists(new_folder_name):
		print('文件已存在！')
		return
	os.mkdir(new_folder_name)
	# 创建进程池
	po = multiprocessing.Pool(5)
	# 创建队列用来进程之间的通信,注意和一般队列创建的区别
	queue = multiprocessing.Manager().Queue()
	files = os.listdir(old_folder_name)
	for file in files:
		# 将每个文件的复制视为一个任务，并交付进程池
		po.apply_async(copy_file, args=(old_folder_name, new_folder_name, file, queue))
	po.close()  # 关闭进程池即不再允许往进程池中添加任务
	finished_num = 0
	while True:
		queue.get()
		finished_num += 1
		progress = finished_num / len(files) * 100
		print('\r已完成：【%s】%.2f%%' % ('*' * round(progress), progress), end='')
		if finished_num >= len(files):
			break

if __name__ == '__main__':
	main()