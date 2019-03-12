def main():
	li = [ x * 2 for x in range(20) if x < 10 ]  # 列表表达式
	print(*li)
	print('使用列表表达式构建的生成器:')
	generator = ( x * 2 for x in range(20) if x < 10 )
	try:
		while True:
			res = next(generator)
			print(res, end='\t')
	except StopIteration:
		print('遍历完成！')

if __name__ == '__main__':
	main()