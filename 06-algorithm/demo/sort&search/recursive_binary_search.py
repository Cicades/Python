# 二分查找法的递归实现

def recursive_binary_search(li, num):
	"""二分查找"""
	if len(li) <= 1:
		if li[0] == num:
			return True
		else: 
			return False
	low = 0
	high = len(li) - 1
	mid = (low + high) // 2
	if li[mid] == num:
		return True
	elif num < li[mid]:
		return recursive_binary_search(li[:mid], num)
	else:
		return recursive_binary_search(li[mid + 1:], num)
if __name__ == '__main__':
	li = [17, 20, 26, 31, 44, 45, 53, 56, 77, 93]
	res = recursive_binary_search(li, 54)
	print(res)
