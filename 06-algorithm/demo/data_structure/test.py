def test(T):
	t = T()
	t.unshift(1) # 1
	t.unshift(2) # 2 1
	t.append(3) # 2 1 3
	t.insert(2, 4) # 2 1 4 3
	t.insert(4, 5) # 2 1 4 3 5
	t.insert(0, 6) # 6 2 1 4 3 5
	print("预计长度为6，实际长度为：%d" % t.length)
	print("预计遍历结果为： 6 2 1 4 3 5")
	print("实际遍历结果为：", end='')
	t.travel()
	print('\n')
	print('预计返回的下表为:4，实际为：%d' % t.search(3)) # 4
	print('预计返回的下表为:3，实际为：%d' % t.search(4)) # 3
	t.remove(1) # 返回2 6 2 4 3 5
	t.remove(9) # 返回-1 6  2 4 3 5
	t.remove(6) # 返回0  2 4 3 5
	print('预计删除元素的下表为3，实际为：%d' % t.remove(5)) # 返回3  2 4 3
	print("预计长度为3，实际长度为：%d" % t.length)
	print("预计遍历结果为： 2 4 3")
	print("实际遍历结果为：", end='')
	t.travel()