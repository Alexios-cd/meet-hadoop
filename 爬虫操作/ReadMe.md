# 综述
在使用爬虫时遇见的问题
## 项目相关操作
### 新建项目

```shell
# 新建项目
scrapy startproject sogou_dict_scrapy
# 生成样例项目
cd sogou_dict_scrapy
scrapy genspider example example.com
```

修改项目的setting.py文件中的ROBOTSTXT_OBEY,如果不遵守请设置为 False

```
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
```



修改项目的setting.py文件的的USER_AGENT，USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36' 

```
# 修改 USER_AGENT 模拟浏览器
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
# 修改延迟下载
DOWNLOAD_DELAY = 1
# 修改随机下载间隔
RANDOMIZE_DOWNLOAD_DELAY = True 
# 打开Cookies
COOKIES_ENABLED = True
```

**注意**

1. 如果使用文件下载功能需要在 setting.py 中配置 FILES_STORE字段，否则不生效。
2. 在 pipelines.py 继承 SogouDictScrapyPipeline(FilesPipeline)
3. 在 setting文件中配置 ITEM_PIPELINES 

```
ITEM_PIPELINES = {
    "sogou_dict_scrapy.pipelines.SogouDictScrapyPipeline": 300,
}
```

否则不生效

4. 在解析 node_list 子元素使用 xpath时需要在前面添加 ./ ,不添加默认解析父元素

   ```
   item_name = node.xpath('.//div[@class="detail_title"]//a/text()').extract_first()
   ```
