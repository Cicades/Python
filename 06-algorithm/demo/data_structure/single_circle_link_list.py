# 单向循环链表的实现

class Node(object):
	"""链表的节点"""
	def __init__(self, data):
		self.data = data
		self.next = None
		

class SingleCircleLinkList(object):
	"""单链表"""
	def __init__(self, head=None):
		if head is None:
			self.__head = None
		else:
			head.next = head
			self.__head = head

	def is_empty(self):
		"""判断链表是否为空"""
		return self.__head is None

	@property
	def length(self):
		"""获取单链表的长度"""
		cur = self.__head # 游标
		if cur is None:
			return -1
		count = 0 # 计数器
		while cur.next is not self.__head:
			cur = cur.next
			count += 1
		count += 1
		return count

	def travel(self):
		"""遍历单链表"""
		cur = self.__head # 游标
		if cur is None:
			print('列表为空！')
			return
		while cur.next is not self.__head:
			print(cur.data, end=' ')
			cur = cur.next
		print(cur.data)

	def unshift(self, data):
		"""头部添加元素"""
		node = Node(data) # 待插入节点
		if self.is_empty():
			# 链表为空
			node.next = node
		else:
			tail = self.__head
			while tail.next is not self.__head:
				tail = tail.next # 找到尾节点
			node.next = self.__head
			tail.next = node
		self.__head = node

	def append(self, data):
		"""尾部添加元素"""
		node = Node(data)
		if self.is_empty():
			node.next = node
			self.__head = node
		else:
			cur = self.__head
			while cur.next is not self.__head:
				cur = cur.next
			node.next = self.__head
			cur.next = node

	def insert(self, pos, data):
		"""在指定位置添加元素"""
		if pos <= 0:
			self.unshift(data)
		elif pos > self.length - 1:
			self.append(data)
		else:
			count = 0
			cur = self.__head
			while count < pos - 1:
				cur = cur.next
				count += 1
			node = Node(data)
			node.next = cur.next
			cur.next = node

	def remove(self, data):
		"""删除节点"""
		if self.is_empty():
			# 链表为空
			return -1
		pre = None # 目标元素的前驱
		cur = self.__head # 目标元素
		count = 0 # 删除元素的下标
		while cur.next is not self.__head:
			if cur.data == data:
				if pre is None:
					# 删除的目标是头节点
					# 寻找尾节点
					tail = cur # 从现在位置继续遍历
					while tail.next is not self.__head:
						tail = tail.next
					self.__head = cur.next
					tail.next = self.__head
				else:
					pre.next = cur.next
				return count
			else:
				pre, cur = cur, cur.next
				count += 1
		# 遍历结束,cur指向尾节点
		if cur.data == data:
			if cur == self.__head:
				# 尾节点又是头节点
				self.__head = None
			else:
				pre.next = self.__head
			return count
		return -1 # 不存在要删除的元素

	def search(self, data):
		"""查找结点"""
		cur = self.__head
		if cur is None:
			return -1
		count = 0
		while cur.next is not self.__head:
			if cur.data == data:
				return count
			else:
				cur = cur.next
				count += 1
		if cur.data == data:
			return count
		return -1 # 没有找到相关元素


if __name__ == '__main__':
	from test import test
	test(SingleCircleLinkList)
