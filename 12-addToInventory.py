def addToInventory(inventory, addedItems):
	for item in addedItems:
		inv.setdefault(item,0)
		inventory[item] +=1
	return inventory
def printInv(inv):
	print('Inventory:')
	for k,v in inv.items():
		print(v,k,sep='\t')
inv = {'gold coin': 42, 'rope': 1}
dragonLoot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']
inv = addToInventory(inv, dragonLoot)
printInv(inv)