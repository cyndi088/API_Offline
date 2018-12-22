# -*- coding: utf-8 -*-
import pymysql
from pymongo import MongoClient


class MiddleTable(object):

    def __init__(self):
        self.mysql_host = "192.168.10.121"
        self.mysql_user = 'hzyg'
        self.mysql_password = '@hzyq20180426..'
        self.MONGO_HOST = '106.14.176.62'
        self.MONGO_PORT = 27017
        # self.MONGO_USER = ''
        # self.PSW = ''

    def open_sql(self, ms_db, mo_db, mo_coll):
        self.link = pymysql.connect(self.mysql_host, self.mysql_user, self.mysql_password, ms_db)
        self.link.set_charset('utf8')
        self.cursor = self.link.cursor()
        self.client = MongoClient(host=self.MONGO_HOST, port=self.MONGO_PORT)
        self.mo_db = self.client[mo_db]
        self.coll = self.mo_db[mo_coll]

    def input_sql(self):
        producer_list = self.coll.distinct('corpName', {})
        seller_list = self.coll.distinct('corpNameBy', {})
        company_list = list(set(producer_list + seller_list))
        for name in company_list or seller_list:
            if name != '/':
                detail_list = self.coll.find({'$or': [{'corpName': name, 'corpNameBy': name}]})
                for detail in detail_list:
                    inspection_id = detail['_id']
                    product_name = detail['commodityName']
                    produce_name = detail['corpName']
                    seller_name = detail['corpNameBy']
                    security_results = detail['newsDetailTypeId']
                    source = detail['rwly_id']
                    data_type = detail['flId']
                    status = detail['status']
                    notice_date = detail['ggrq']
                    if produce_name != '/':
                        sql = "select id from sys_organization where name='%s'" % produce_name
                        self.cursor.execute(sql)
                        produce_id = self.cursor.fetchone()
                        if produce_id == None:
                            produce_id = None
                        else:
                            produce_id = produce_id[0]
                    else:
                        produce_id = None
                    if seller_name != '/':
                        sql = "select id from sys_organization where name='%s'" % seller_name
                        self.cursor.execute(sql)
                        seller_id = self.cursor.fetchone()
                        if seller_id == None:
                            seller_id = None
                        else:
                            seller_id = seller_id[0]
                    else:
                        seller_id = None
                    if detail['addressByRegionId'] == detail['addressRegionId']:
                        supervise_id = detail['addressByRegionId']
                        sql = """INSERT INTO organization_inspection_relation(inspection_id, producer_id, seller_id, supervise_id, security_results, source, data_type, status, notice_date, product_name, organization_name, casual_organization_name) VALUES("%s","%d", "%d", "%d","%d", "%d", "%d", "%d", "%s", "%s", "%s", "%s")"""  % (inspection_id, produce_id, seller_id, supervise_id, security_results, source, data_type, status, notice_date, product_name, produce_name, seller_name)
                        self.cursor.execute(sql)
                        self.link.commit()
                    else:
                        supervise_id1 = detail['addressByRegionId']
                        supervise_id2 = detail['addressRegionId']
                        sql1 = """INSERT INTO organization_inspection_relation(inspection_id, producer_id, seller_id, supervise_id, security_results, source, data_type, status, notice_date, product_name, organization_name, casual_organization_name) VALUES("%s","%d", "%d", "%d","%d", "%d", "%d", "%d", "%s", "%s", "%s", "%s")"""  % (inspection_id, produce_id, seller_id, supervise_id1, security_results, source, data_type, status, notice_date, product_name, produce_name, seller_name)
                        self.cursor.execute(sql1)
                        self.link.commit()
                        sql2 = """INSERT INTO organization_inspection_relation(inspection_id, producer_id, seller_id, supervise_id, security_results, source, data_type, status, notice_date, product_name, organization_name, casual_organization_name) VALUES("%s","%d", "%d", "%d","%d", "%d", "%d", "%d", "%s", "%s", "%s", "%s")""" % (inspection_id, produce_id, seller_id, supervise_id2, security_results, source, data_type,
                        status, notice_date, product_name, produce_name, seller_name)
                        self.cursor.execute(sql2)
                        self.link.commit()

    def close_sql(self):
        self.link.close()


mt = MiddleTable()
mt.open_sql('yfhunt', 'zhejiang', 'sheng')
mt.input_sql()
mt.close_sql()



