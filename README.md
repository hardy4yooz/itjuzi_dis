## 简介
在使用 scrapy 爬取 [IT桔子公司][1]信息，用来进行分析，了解 IT 创业公司的一切情况，之前使用 scrapy 写了一个默认线程是10的单个实例，为了防止被 ban IP 设置了下载的速度，3万多个公司信息爬了1天多才完成，现在想到使用分布式爬虫来提高效率。

***[源码githup][2]***

####技术工具：`Python3.5` `scrapy` `scrapy_redis` `redis` `docker1.12` `docker-compose` `Kitematic` `mysql` `SQLAlchemy`

## 准备工作

 1. 安装 `Docker` [点这里][3]去了解、安装;
 2. `pip install scrapy scrapy_redis`;
 
## 代码编写

1. 分析页面信息：
我需要获取的是每一个「公司」的详情页面链接 和 分页按钮链接；
2. 统一存储获取到的链接，提供给多个 `spider` 爬取；
3. 多个 `spider` 共享一个 `redis` `list` 中的链接；

###目录结构图
![图片描述][5]
###juzi_spider.py
```
# coding:utf-8

from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy_redis.spiders import RedisCrawlSpider
from itjuzi_dis.items import CompanyItem


class ITjuziSpider(RedisCrawlSpider):
    name = 'itjuzi_dis'
    allowed_domains = ['itjuzi.com']
    # start_urls = ['http://www.itjuzi.com/company/157']
    redis_key = 'itjuziCrawler:start_urls'
    rules = [
        # 获取每一页的链接
        Rule(link_extractor=LinkExtractor(allow=('/company\?page=\d+'))),
        # 获取每一个公司的详情
        Rule(link_extractor=LinkExtractor(allow=('/company/\d+')), callback='parse_item')
    ]

    def parse_item(self, response):
        soup = BeautifulSoup(response.body, 'lxml')

         .
         .省略一些处理代码
         .
        return item
```
**说明：** 
1. `class` 继承了`RedisCrawlSpider` 而不是`CrawlSpider`
2. `start_urls` 改为一个自定义的 `itjuziCrawler:start_urls`,这里的`itjuziCrawler:start_urls` 就是作为所有链接存储到 `redis` 中的 `key`,`scrapy_redis` 里也是通过`redis`的 `lpop`方法弹出并删除链接的；

###db_util.py
使用 `SQLAlchemy` 作为 `ORM` 工具，当表结构不存在时，自动创建表结构

###middlewares.py
增加了很多 `User-Agent`，每一个请求随机使用一个，防止防止网站通过 `User-Agent` 屏蔽爬虫

###settings.py
配置`middlewares.py` `scrapy_redis` `redis` 链接相关信息

##部署
在上面的「目录结构图」中有，`Dockerfile`和`docker-compose.yml`
### Dockerfile

```
FROM python:3.5
ENV PATH /usr/local/bin:$PATH
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
COPY spiders.py /usr/local/lib/python3.5/site-packages/scrapy_redis
CMD /usr/local/bin/scrapy crawl itjuzi_dis

```
**说明：** 

 - 使用 `python3.5`作为基础镜像
 - 将`/usr/local/bin`设置环境变量
 - 映射 `host` 和 `container` 的目录
 - 安装 `requirements.txt`
 - 特别要说明的是`COPY spiders.py /usr/local/lib/python3.5/site-packages/scrapy_redis`，将 `host` 中的 `spiders.py` 拷贝到`container` 中的 `scrapy_redis` 安装目录中，因为 `lpop` 获取`redis` 的值在 `python2`中是 `str` 类型，而在 `python3`中是 `bytes` 类型，这个问题在 `scrapy_reids` 中需要修复，`spiders.py` 第84行需要修改；
 - 启动后立即执行爬行命令 `scrapy crawl itjuzi_dis`

### docker-compose.yml
```
version: '2'
services:
  spider:
    build: .
    volumes:
     - .:/code
    links:
     - redis
    depends_on:
     - redis
  redis:
    image: redis
    ports:
    - "6379:6379"

```
**说明:**

 - 使用第2版本的 `compose` 描述语言
 - 定义了 `spider` 和 `redis` 两个 `service`
 - `spider`默认使用当前目录的 `Dockerfile` 来创建，`redis`使用 `redis:latest` 镜像创建，并都映射6379端口

###开始部署

**启动 container**
    docker-compose up #从 docker-compose.yml 中创建 `container` 们
    docker-compose scale spider=4 #将 spider 这一个服务扩展到4个，还是同一个 redis

 可以在 `Kitematic` GUI 工具中观察创建和运行情况；

![图片描述][6]

 在没有设置 `start_urls` 时，4个 `container` 中的爬虫都处于饥渴的等待状态

![图片描述][7]

现在给 `redis` 中放入 `start_urls`:
    lpush itjuziCrawler:start_urls http://www.itjuzi.com/company
   
4个爬虫都动起来了，一直爬到`start_urls`为空
![图片描述][8]

以上！


  [1]: http://www.itjuzi.com/company
  [2]: https://github.com/caoxiaozh/itjuzi_dis
  [3]: https://www.docker.com/products/overview
  [4]: https://github.com/caoxiaozh/itjuzi_dis
  [5]: https://segmentfault.com/img/bVAlLY
  [6]: https://segmentfault.com/img/bVAlSh
  [7]: https://segmentfault.com/img/bVAlS7
  [8]: https://segmentfault.com/img/bVAlUh
