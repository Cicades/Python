import pprint
guest = {'alice': {'apple': 2,'bananas': '4'},
		'bob': {'apple': 3,'shit': 3},
		'sam': {'pineapple': 2,'rice': 5}
		}
food = {}
for item in guest.values():
	for k,v in item.items():
		food.setdefault(k,0)
		food[k] += int(v)
pprint.pprint(food)