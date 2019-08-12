# 双向链表的实现

class Node(object):
	"""链表的节点"""
	def __init__(self, data):
		self.data = data
		self.next = None
		self.prior = None
		

class DoubleLinkList(object):
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
			print(cur.data, end=' ')
			cur = cur.next

	def unshift(self, data):
		"""头部添加元素"""
		node = Node(data) # 待插入节点
		if self.is_empty():
			self.__head = node
		else:
			node.next = self.__head
			self.__head.prior = node
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
			node.prior = cur
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
			while count < pos:
				cur = cur.next
				count += 1
			node = Node(data)
			node.next = cur
			node.prior = cur.prior
			cur.prior.next = node
			cur.prior = node

	def remove(self, data):
		"""删除节点"""
		cur = self.__head # 目标元素
		count = 0 # 删除元素的下标
		while cur is not None:
			if cur.data == data:
				# 匹配删除对象
				if cur.prior is None:
					# 删除的节点为头节点
					self.__head = cur.next
					cur.next.prior = None
				elif cur.next is None:
					# 如果删除的节点为尾节点
					cur.prior.next = None
				else:
					cur.prior.next = cur.next
					cur.next.prior = cur.prior
				return count
			else:
				# 不匹配
				cur = cur.next
				count += 1
		# 循环自然结束， 不存在匹配对象
		return -1


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

if __name__ == '__main__':
	from test import test
	test(DoubleLinkList)