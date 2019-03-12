

def fibonacci(times):
	"""使用生成器实现Fibonacci数列"""
	current_time = 0
	a = 0
	b = 1
	while True:
		if current_time <= times:
			a, b = b, a + b
			current_time += 1
			ret = yield b  # ret可接收生成器send方法传入的参数
			print(ret)
		else:
			break


def main():
	generator = fibonacci(4)
	res = next(generator)
	print(res)
	while True:
		print(generator.send('ret'), end='\t')

if __name__ == '__main__':
	try:
		main()
	except StopIteration:
		print('\n遍历结束！')

