import requests
import re
import json

url = 'https://lol.qq.com/biz/hero/champion.js'
content = requests.get(url).content.decode()
data = re.search(r'LOLherojs.champion=(.*)', content).group(1)[:-1]
hero_list = json.loads(data, encoding='utf-8')
with open('lol.json', 'w', encoding='utf-8') as f:
	f.write(json.dumps(hero_list, ensure_ascii=False, indent=2))