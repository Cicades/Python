

class FibnacciIterator(object):
	"""使用迭代器实现Fibonacci数列"""
	def __init__(self, times):
		self.times = times  # 迭代的次数
		self.current_times = 0
		self.a = 0  
		self.b = 1
	
	def __iter__(self):
		"""判断一个对象是不是可遍历的，最直观的是看他有没有__iter__方法"""
		return self  # 发挥的对象就是遍历器，其一定要包含__next__方法

	def __next__(self):
		"""迭代器的核心方法，用来存储值生成的方式"""
		if self.current_times <= self.times:
			self.a, self.b = self.b, self.a + self.b
			self.current_times += 1
			return self.b
		else:
			raise StopIteration  # 遍历次数超出范围就会抛出异常，而使用for in 循环会自动处理此异常


def main():
	fibonacci_iterator = iter(FibnacciIterator(3))  #  iter 内置函数可以返回一个可遍历对象的遍历器
	print('*****使用next*****：')
	try:
		while True:
			res = next(fibonacci_iterator)  # next 函数可以调用遍历器的__next__ 方法，并获得其返回值
			print(res, end='\t')
	except:
		print('遍历完成！')

	# 使用for循环直接对可变了对象进行遍历
	print('*****for*****:')
	for item in FibnacciIterator(4):
		print(item, end='\t')
	else:
		print('遍历完成！')

if __name__ == '__main__':
	main()
