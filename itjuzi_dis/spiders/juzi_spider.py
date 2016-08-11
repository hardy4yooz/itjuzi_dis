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

        cpy1 = soup.find('div', class_='infoheadrow-v2')
        if cpy1:
            company_name = cpy1.find(class_='title').b.contents[0].strip().replace('\t', '').replace('\n', '')
            slogan = cpy1.find(class_='info-line').p.get_text()
            scope_a = cpy1.find(class_='scope c-gray-aset').find_all('a')
            scope = scope_a[0].get_text().strip() if len(scope_a) > 0 else ''
            sub_scope = scope_a[1].get_text().strip() if len(scope_a) > 1 else ''
            city_a = cpy1.find(class_='loca c-gray-aset').find_all('a')
            city = city_a[0].get_text().strip() if len(city_a) > 0 else ''
            area = city_a[1].get_text().strip() if len(city_a) > 1 else ''

            home_page = cpy1.find(class_='weblink marl10')['href']
            tags = cpy1.find(class_='tagset dbi c-gray-aset').get_text().strip().strip().replace('\n', ',')

        cpy2 = soup.find('div', class_='block-inc-info on-edit-hide')
        if cpy2:
            company_intro = cpy2.find(class_='des').get_text().strip()
            cpy2_content = cpy2.find(class_='des-more').contents
            company_full_name = cpy2_content[1].get_text().strip()[len('公司全称：'):] if cpy2_content[1] else ''
            found_time = cpy2_content[3].contents[1].get_text().strip()[len('成立时间：'):] if cpy2_content[3] else ''
            company_size = cpy2_content[3].contents[3].get_text().strip()[len('公司规模：'):] if cpy2_content[3] else ''
            company_status = cpy2_content[5].get_text().strip() if cpy2_content[5] else ''

        main = soup.find('div', class_='main')

        # 投资
        tz = main.find('table', 'list-round-v2')
        tz_list = []
        if tz:
            all_tr = tz.find_all('tr')
            for tr in all_tr:
                tz_dict = {}
                all_td = tr.find_all('td')
                tz_dict['tz_time'] = all_td[0].span.get_text().strip()
                tz_dict['tz_round'] = all_td[1].get_text().strip()
                tz_dict['tz_finades'] = all_td[2].get_text().strip()
                tz_dict['tz_capital'] = all_td[3].get_text().strip().replace('\n', ',')
                tz_list.append(tz_dict)

        # 团队 team
        tm = main.find('ul', class_='list-prodcase limited-itemnum')
        tm_list = []
        if tm:
            for li in tm.find_all('li'):
                tm_dict = {}
                tm_dict['tm_m_name'] = li.find('span', class_='c').get_text().strip()
                tm_dict['tm_m_title'] = li.find('span', class_='c-gray').get_text().strip()
                tm_dict['tm_m_intro'] = li.find('p', class_='mart10 person-des').get_text().strip()
                tm_list.append(tm_dict)

        pdt = main.find('ul', class_='list-prod limited-itemnum')
        pdt_list = []
        if pdt:
            for li in pdt.find_all('li'):
                pdt_dict = {}
                pdt_dict['pdt_name'] = li.find('h4').b.get_text().strip()
                pdt_dict['pdt_type'] = li.find('span', class_='tag yellow').get_text().strip()
                pdt_dict['pdt_intro'] = li.find(class_='on-edit-hide').p.get_text().strip()
                pdt_list.append(pdt_dict)
        item = CompanyItem()
        item['info_id'] = response.url.split('/')[-1:][0]
        item['company_name'] = company_name
        item['slogan'] = slogan
        item['scope'] = scope
        item['sub_scope'] = sub_scope
        item['city'] = city
        item['area'] = area
        item['home_page'] = home_page
        item['tags'] = tags
        item['company_intro'] = company_intro
        item['company_full_name'] = company_full_name
        item['found_time'] = found_time
        item['company_size'] = company_size
        item['company_status'] = company_status
        item['tz_info'] = tz_list
        item['tm_info'] = tm_list
        item['pdt_info'] = pdt_list
        return item
