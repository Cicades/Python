# 冒泡排序
# 通过对相邻元素的两两比较，使较大或较小的元素不断向两端移动

def bubble_sort(li):
	# 冒泡排序
	n = len(li)
	for j in range(0, n-1):
		is_sort = True
		for i in range(0, n-1-j):
			# 对算法优化，若果列表已经有序，则一趟遍历即可
			if li[i] > li[i+1]:
				li[i], li[i+1] = li[i+1], li[i]
				is_sort = False
		if is_sort:
			return 


if __name__ == '__main__':
	li = [54,26,93,17,77,31,44,55,20]
	bubble_sort(li)
	print(li)
