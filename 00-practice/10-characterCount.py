import pprint #pretty print 
message ='It was a bright cold day in April, and the clocks were striking thirteen.'
charCount = {}
for char in message:
	charCount.setdefault(char,0)
	charCount[char] += 1
pprint.pprint(charCount)#等价于print(pprint.pformat(charCount))
	