# -*- coding: utf-8 -*-
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

    def start_requests(self):
        """自定义起始request"""
        for url in self.start_urls:

            yield SplashRequest(url, self.parse, args={'wait': 1})

    def parse(self, response):
        """解析列表页"""
        #print response.body
        soup = BeautifulSoup(response.body,'html.parser')
        td_list = soup.find_all('td',class_='name')
        result = [{'pt_url':td.get('href'),
                   'pt_name':td.get_text(),} for td in td_list]

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