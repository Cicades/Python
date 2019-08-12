# 归并排序
# 采用分治法：对待排序的序列进行拆分，直到每个最小的子序列只有一个元素
# 将拆分的子序列进行合并

def merge_sort(li):
	"""归并排序"""
	n = len(li)
	if n <= 1:
		return li
	mid = n // 2
	left_li = merge_sort(li[:mid])
	right_li = merge_sort(li[mid:])
	res = list()
	l = r = 0
	while l < len(left_li) and r < len(right_li):
		if left_li[l] <= right_li[r]:
			res.append(left_li[l])
			l += 1
		else:
			res.append(right_li[r])
			r += 1
	res += left_li[l:]
	res += right_li[r:]
	return res

if __name__ == '__main__':
	li = [54,26,93,17,77,31,44,55,20, 54]
	print(merge_sort(li))