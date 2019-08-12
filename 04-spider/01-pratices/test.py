# coding=utf-8
import requests
import json


class DoubanSpider:
    def __init__(self):
        self.url_temp_list = [
            {
                "url_temp": "https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_american_hot/items?start=0&count=18&loc_id=108288",
                "country": "US"
            },
            {
                "url_temp": "https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_english_hot/items?start={}&count=18&loc_id=108288",
                "country": "UK"
            },
            {
                "url_temp": "https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_domestic_hot/items?start={}&count=18&loc_id=108288",
                "country": "CN"
            }
        ]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36"}

    def parse_url(self, url):  # 发送请求，获取响应
        print(url)
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def get_content_list(self, json_str):  # 提取是数据
        dict_ret = json.loads(json_str)
        content_list = dict_ret["subject_collection_items"]
        total = dict_ret["total"]
        return content_list, total

    def save_content_list(self, content_list,country):  # 保存
        with open("douban.txt", "a", encoding="utf-8") as f:
            for content in content_list:
                content["country"] = country
                f.write(json.dumps(content, ensure_ascii=False))
                f.write("\n")  # 写入换行符，进行换行
        print("保存成功")

    def run(self):  # 实现主要逻辑
        print(self.parse_url(self.url_temp_list[0]['url_temp']))

if __name__ == '__main__':
    douban_spider = DoubanSpider()
    douban_spider.run()
