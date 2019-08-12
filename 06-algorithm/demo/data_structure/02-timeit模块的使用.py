# a+b+c=1000 and a^2+b^2=c^2
from timeit import Timer
def t1():
	for a in range(1001):
		for b in range(1001 - a):
			c = 1000 - (a + b)
			if a + b + c == 1000 and a ** 2 + b ** 2 == c ** 2:
				pass

def t2():
	for a in range(1001):
		for b in range(1001):
			for c in range(1001):
				if a + b + c == 1000 and a ** 2 + b ** 2 == c ** 2:
					pass

timer1 = Timer('t1()', 'from __main__ import t1')
timer2 = Timer('t2()', 'from __main__ import t2')
print(timer1.timeit(100))
print(timer2.timeit(100))