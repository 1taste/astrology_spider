# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from scrapy.exceptions import DropItem
from DBUtils.PooledDB import PooledDB
class DataBasePipeline(object):

    __pool = None

    def __get_conn(self):
        if self.__pool is None:
            __pool = PooledDB(creator=MySQLdb, mincached=1, maxcached=20,
                              host='localhost', port=3306, user='root', passwd='',
                              db='astrology', charset='utf8')
        return __pool.connection()

    def process_item(self, item, spider):
        try:
            #conn = MySQLdb.connect(host='localhost', port=3306, db='astrology', user='root', passwd='', charset='utf8')
            conn = self.__get_conn()
            cur = conn.cursor()
            cur.execute('select * from PERSON where URL=%s', [item['url']])
            for row in cur.fetchall():
                raise DropItem("Duplicate item found: %s" % item)

            insert_sql = 'insert into PERSON(`NAME`,`OCCUPATION`,`BIRTHDAY`,`URL`,`REGION`) VALUES(%s,%s,%s,%s,%s)'
            #print item
            params = [item['name'], item['occupation'], item['birthday'], item['url'], item['region']]
            cur.execute(insert_sql, params)
            conn.commit()

            cur.close()
            conn.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return item


class ValidatePipeline(object):
    keys = ['name', 'birthday', 'occupation', 'region']
    def process_item(self, item, spider):
        for k in self.keys:
            if k not in item:
                raise DropItem("Duplicate item found: %s" % item)
        return item