def listToStr(item):
	str = ''
	for i in range(len(item)):
		if i == (len(item)-1):
			str += 'and cat'
			return str
		str +=item[i] + ', '
spam = ['apples', 'bananas', 'tofu', 'cats']
print(listToStr(spam))


