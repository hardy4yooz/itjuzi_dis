# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

from itjuzi_dis.db_util import JuziCompany,DB_Util,JuziTeam,JuziTz,JuziProduct


# 去重复的 company
class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['info_id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['info_id'])
            return item


class ItjuziSpiderPipeline(object):
    def open_spider(self, spider):
        DB_Util.init_db()  # 表不存在时候,初始化表结构

    def process_item(self, item, spider):
        if not item['info_id']:
            raise DropItem('item info_id is null.{0}'.format(item))
        else:
            session = DB_Util.get_session()
            company = JuziCompany()
            company.company_name = item['company_name']
            company.slogan = item['slogan']
            company.scope=item['scope']
            company.sub_scope=item['sub_scope']
            company.city = item['city']
            company.area = item['area']
            company.home_page=item['home_page']
            company.tags=item['tags']
            company.company_intro=item['company_intro']
            company.company_full_name=item['company_full_name']
            company.found_time=item['found_time']
            company.company_size=item['company_size']
            company.company_status=item['company_status']
            company.info_id = item['info_id']
            session.add(company)
            if item['tz_info']:
                for touzi in item['tz_info']:
                    tz = JuziTz()
                    tz.company_id = company.info_id
                    tz.tz_time = touzi['tz_time']
                    tz.tz_finades = touzi['tz_finades']
                    tz.tz_capital = touzi['tz_capital']
                    tz.tz_round = touzi['tz_round']
                    session.add(tz)
            if item['tm_info']:
                for team in item['tm_info']:
                    tm = JuziTeam()
                    tm.company_id = company.info_id
                    tm.tm_m_name = team['tm_m_name']
                    tm.tm_m_title = team['tm_m_title']
                    tm.tm_m_intro = team['tm_m_intro']
                    session.add(tm)
            if item['pdt_info']:
                for product in item['pdt_info']:
                    pdt = JuziProduct()
                    pdt.company_id = company.info_id
                    pdt.pdt_name = product['pdt_name']
                    pdt.pdt_type = product['pdt_type']
                    pdt.pdt_intro = product['pdt_intro']
                    session.add(pdt)
            session.commit()
        return item
