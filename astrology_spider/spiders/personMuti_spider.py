# coding:utf-8
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from astrology_spider.items import PersonItem
class PersonMutiSpider(CrawlSpider):
    name = "personMuti"
    allowed_domain = "baike.baidu.com"
    #李幼斌,毛泽东,爱因斯坦
    start_urls = [
        'http://baike.baidu.com/subview/5972/10680834.htm'
        #"http://baike.baidu.com/view/2526.htm",
        #"http://baike.baidu.com/subview/15435/6046883.htm",
        #"http://baike.baidu.com/subview/1689/11849262.htm"

    ]
    #通过相关人物/其他人正在看,进行层进
    rules = (
        Rule(LinkExtractor(allow_domains=('baike.baidu.com'),restrict_xpaths=('//div[@class="lemmaWgt-sideRecommend"]')),
             callback='parse_item', follow=True),
    )

    #pra = '//div[@class="lemmaWgt-sideRecommend"]/a[re:test(@href, "http://baike.baidu.com/[view|subview]/*htm")]'
    def parse_item(self, response):
        fields = {
            "中文名": 'name',
            "出生地": 'region',
            "出生日期": 'birthday',
            "职    业": 'occupation'
        }
        items = []
        base_info = response.selector.xpath('//div[@class="basic-info"]')
        key_dom = base_info.xpath('.//dt')
        item = PersonItem()
        for dt in key_dom:
            k = dt.xpath('.//text()').extract()
            if len(k) > 0:
                key = k[0].encode('utf-8')
            else:
                continue
            v = dt.xpath('.//following-sibling::dd[1]/descendant::text()').extract()
            value = ''.join(v).encode('utf-8').replace('\n', '')

            item['url'] = response.url
            if key in fields:
                item[fields[key]] = value
        return item
