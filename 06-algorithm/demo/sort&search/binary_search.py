# 二分查找法

def binary_search(li, num):
	"""二分查找"""
	low  = 0
	high = len(li) - 1
	while low <= high:
		mid = (low + high) // 2
		if li[mid] == num:
			return mid
		elif num < li[mid]:
			high = mid - 1
		else:
			low = mid + 1
	return -1

if __name__ == '__main__':
	li = [17, 20, 26, 31, 44, 45, 53, 56, 77, 93]
	res = binary_search(li, 53)
	print(res)