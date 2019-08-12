# 将每趟遍历得到的最小或最大元素放至列表的两端

def select_sort(li):
	"""选择排序"""
	n = len(li)
	for j in range(n-1):
		min_index = j
		for i in range(1+j, n):
			if li[min_index] > li[i]:
				min_index = i
		li[j], li[min_index] = li[min_index], li[j]

if __name__ == '__main__':
	li = [54,226,93,17,77,31,44,55,20]
	select_sort(li)
	print(li)