# -*- coding: utf-8 -*-
from copy import deepcopy

from scrapy import Spider
from scrapy import Request
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup

class P2peyeSpider(Spider):
    name = "p2peye"
    #allowed_domains = ["p2peye.com"]
    start_urls = (
        'http://www.p2peye.com/rating',
    )
    headers = {
        'Host':'www.p2peye.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer':'http://www.p2peye.com/',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
    }
    def start_requests(self):
        """自定义起始request"""
        for url in self.start_urls:

            yield SplashRequest(url, self.parse,
                                args={'wait': 10},
                                splash_headers=self.headers)

    def parse(self, response):
        """解析列表页"""
        #print response.body
        soup = BeautifulSoup(response.body,'html.parser')
        headers = deepcopy(self.headers)
        headers['Referer']='http://www.p2peye.com/rating'
        td_list = soup.find_all('td',class_='name')
        result = [{'pt_url':td.a.get('href'),
                   'pt_name':td.a.get_text(),} for td in td_list]
        for item in result:
            print item['pt_name'],item['pt_url']

            yield SplashRequest(url=item['pt_url'],
                                callback=self.parseDetail,
                                args={'wait':10},
                                splash_headers=headers,
                                )


    def parseDetail(self,response):
        """解析详细页面"""
        print response.body
        soup = BeautifulSoup(response.body,'html.parser')
        td_list = soup.find_all('td',class_='list')
        result = {'companyName':td_list[0].span.get_text(),
                  'legalRepresentative':td_list[1].span.get_text(),
                  'employeeAmount':td_list[2].span.get_text(),
                  'registeredCapitital':td_list[3].span.get_text(),
                  'QQ':td_list[4].span.get_text(),
                  'phoneCustomer':td_list[5].span.get_text(),
                  'autoBidding':td_list[6].span.get_text(),
                  'assignmentOfDebt':td_list[7].span.get_text(),
                  'foundCustodian':td_list[8].span.get_text(),
                  'safeguardWay':td_list[9].span.get_text()
                  }
        yield result