# 快速排序
# 通过循环比较直接确定一个元素在理想序列中的正确位置
# 设置头，尾两个游标，从两端开始遍历，保证目标元素的左边都小于它，右边都大于它

def quick_sort(li, start, end):
	"""快速排序"""
	low = start
	high = end
	if low >= high:
		return
	mid_value = li[low]
	while low < high:
		while low < high:
			if mid_value >= li[high]:
				li[low] = li[high]
				break
			else:
				high -= 1

		while low < high:
			if mid_value < li[low]:
				li[high] = li[low]
				break
			else:
				low += 1
	li[low] = mid_value
	quick_sort(li, start, low-1) # 左子序列
	quick_sort(li, high+1, end) # 右子序列


if __name__ == '__main__':
	li = [ 54,226,93,17,
		   77,31,44,55,
		   20, 17 ]
	quick_sort(li, 0, len(li)-1)
	print(li)

