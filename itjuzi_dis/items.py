# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    info_id = scrapy.Field()
    company_name = scrapy.Field()
    slogan = scrapy.Field()
    scope = scrapy.Field()
    sub_scope = scrapy.Field()
    city = scrapy.Field()
    area = scrapy.Field()
    home_page = scrapy.Field()
    tags = scrapy.Field()
    company_intro = scrapy.Field()
    company_full_name = scrapy.Field()
    found_time = scrapy.Field()
    company_size = scrapy.Field()
    company_status = scrapy.Field()
    tz_info = scrapy.Field()
    tm_info = scrapy.Field()
    pdt_info = scrapy.Field()