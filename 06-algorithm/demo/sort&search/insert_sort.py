# 插入排序
# 将未排序的列表分为无序和有序两部分，从无序的部分不断选择元素插入到有序部分的合适位置
def insert_sort(li):
	n = len(li)
	for i in range(1, n):
		while i > 0:
			if li[i] < li[i-1]:
				li[i], li[i-1] = li[i-1], li[i]
				i -= 1
			else:
				break

if __name__ == '__main__':
	li = [77,226,93,17,77,31,44,55,20]
	insert_sort(li)
	print(li)