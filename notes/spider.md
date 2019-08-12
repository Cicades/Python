# spider

***

### url请求去重

- 可使用加密算法生成`url`的指纹

  ~~~python
  import hashlib # hashlib封装了常用的摘要算法，如hash，md5等
  sh = hashlib.sha1()
  sh.update('how to use sha1 in')
  sh.update('python hashlib')
  print(sh.hexdigest())  # 打印生成的16进制字符串
  ~~~

***

## scrapy

- 爬虫流程

  ![](./images/spider/scrapy-process.png)

  + `scrapy engine`——总指挥，负责数据和信号在不同的模块间传递（框架已实现）
  + `scheduler`——队列，存放引擎发送过来的request请求（框架已实现），可重写，并配合`redis`实现分布式爬虫，如`scrapy-redis`
  + `Downloader`——根据引擎指派过来的request，发送web请求，并将响应返回给引擎（框架已实现）
  + `spider`——处理response，构造新的request交付给引擎，同时提取item（需要自己实现）
  + `Item Pipline`——处理引擎传递过来的item，如实现存储（需要自己实现）
  + `Downloader Middlewares`——可对item，request进行拦截，改变其默认行为，一般是重写`process_item`和`process_request`两个方法，可以设置代理ip，随机使用不同的cookies，user-agent发送请求
  + `SpiderMiddlewareSpider`——可自定义requests请求和对response进行过滤

- `Selector`

  - 常用api
    + `get`或者`extract_first`
    + `getall`或者`extract`
    + `re`、`re_first`——使用正则对selector或者selectorlist对象进行内容提取

- `post`请求

  + `scrapy.FormRequest`
  + `scrapy.FormRequest.from_response`——从响应中找到表单并发送请求
