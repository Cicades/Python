# 每趟遍历的元素的下标和是一定，且和的大小不断递增
# 找到规律后，剩下的就是利用枚举法求解方程：row_index + col_index = sum_index

def findDiagonalOrder(matrix):
        """
        :type matrix: List[List[int]]
        :rtype: List[int]
        """
        if not matrix:
            # 数组为空
            return []
        col_len = len(matrix[0])
        row_len = len(matrix)
        res = list()
        if row_len == 1:
            return matrix[0]
        if col_len == 1:
            for i in range(row_len):
                res.append(matrix[i][0])
            return res
        direction = True # 向上
        index_sum = col_len + row_len - 2
        for s in range(index_sum + 1):
            travle_range = range(s + 1) if direction else range(s, -1, -1)
            for col_index in travle_range:
                row_index = s - col_index
                if(col_index < col_len and row_index < row_len):
                    res.append(matrix[row_index][col_index])
            direction = not direction
        return res

if __name__ == '__main__':
    matrix = [
     [ 1, 2, 3 ],
     [ 4, 5, 6 ],
     [ 7, 8, 9 ]
    ]
    res = findDiagonalOrder(matrix)
    print(res)