# a+b+c=1000 and a^2+b^2=c^2
# for a in range(1001):
# 	for b in range(1001):
# 		for c in range(1001):
# 			if a + b + c == 1000 and a ** 2 + b ** 2 == c ** 2:
# 				print('({0},{1},{2})'.format(a, b, c))
import time
start = time.time()
count = 0
for a in range(1001):
	for b in range(1001 - a):
		count += 1
		c = 1000 - (a + b)
		if a + b + c == 1000 and a ** 2 + b ** 2 == c ** 2:
			print('({0},{1},{2})'.format(a, b, c))
end = time.time()
print(end - start)
print('时间复杂度为：%d' % count)
				