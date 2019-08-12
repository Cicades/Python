# 希尔排序：插入排序的增量方式
# 根据gap产生若干个子序列，对子序列执行插入排序，完成后，不断缩小gap，重复上述过程，直到gap=1（等价于插入排序）
def shell_sort(li):
	"""希尔排序"""
	n = len(li)
	gap = n // 2
	while gap > 0: 
		for j in range(gap, n):
			i = j
			while i > 0:
				if li[i] < li[i - gap]:
					li[i], li[i - gap] = li[i - gap], li[i]
					i -= gap
				else:
					break
		gap //= 2

if __name__ == '__main__':
	li = [ 54,226,93,17,
		   77,31,44,55,
		   20 ]
	shell_sort(li)
	print(li)