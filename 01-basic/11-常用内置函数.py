def test_enumerate(iteration):
	"""enumerate()函数会将一个遍历对象转换为包含索引值和数据的enumerate对象"""
	for index, value in enumerate(iteration):
		print(index, value, sep='-----')


def main():
	# 1.enumerate()
	test_enumerate('cicades')

if __name__ == '__main__':
	main()