# 单链表的实现

class Node(object):
	"""链表的节点"""
	def __init__(self, data):
		self.data = data
		self.next = None
		

class LinkList(object):
	"""单链表"""
	def __init__(self, head=None):
		self.__head = head

	def is_empty(self):
		"""判断链表是否为空"""
		return self.__head is None

	@property
	def length(self):
		"""获取单链表的长度"""
		count = 0 # 计数器
		cur = self.__head # 游标
		while cur:
			count += 1
			cur = cur.next
		return count

	def travel(self):
		"""遍历单链表"""
		cur = self.__head # 游标
		while cur:
			print(cur.data)
			cur = cur.next

	def unshift(self, data):
		"""头部添加元素"""
		node = Node(data) # 待插入节点
		head = self.__head # 头节点
		node.next = head
		self.__head = node
		

	def append(self, data):
		"""尾部添加元素"""
		node = Node(data)
		if self.is_empty():
			self.__head = node
		else:
			cur = self.__head
			while cur.next is not None:
				cur = cur.next
			cur.next = node

	def insert(self, pos, data):
		"""在指定位置添加元素"""
		if pos < 0:
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
		pre = None # 目标元素的前驱
		cur = self.__head # 目标元素
		count = 0 # 删除元素的下标
		while cur is not None:
			if cur.data == data:
				if pre is None:
					# 删除的目标是头节点
					self.__head = cur.next
				else:
					pre.next = cur.next
				return count
			else:
				pre, cur = cur, cur.next
		return -1 # 不存在要删除的元素

	def search(self, data):
		"""查找结点"""
		cur = self.__head
		count = 0
		while cur is not None:
			if cur.data == data:
				return count
			else:
				cur = cur.next
				count += 1
		return -1 # 没有找到相关元素


	