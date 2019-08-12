# 解题关键：发现遍历的周期性规律

def travel(matrix):
	"""螺旋矩阵遍历"""
	if not matrix:
		return []
	res = []
	row, col = len(matrix), len(matrix[0])
	if row <= 1:
		return matrix[0]
	if col <= 1:
		for i in range(row):
			res.append(matrix[i][0])
		return res
	row_max = row - 1
	col_max = col - 1
	start_index = 0
	while start_index <= row_max and start_index <= col_max:
		i = j = start_index
		while j < col_max:
				res.append(matrix[i][j])
				j += 1
		res.append(matrix[i][j])
		i += 1
		if i > row_max:
			return res
		while i < row_max:
			res.append(matrix[i][j])
			i += 1
		res.append(matrix[i][j])
		j -= 1
		if j < start_index :
			return res
		while j > start_index:
			res.append(matrix[i][j])
			j -= 1
		res.append(matrix[i][j])
		i -= 1
		while i > start_index:
			res.append(matrix[i][j])
			i -= 1
		start_index += 1
		row_max -= 1
		col_max -= 1
	return res

if __name__ == '__main__':
	# matrix = [[2,3,4],[5,6,7],[8,9,10],[11,12,13]]
	matrix = [[1,2],[3,4]]
	print(travel(matrix))