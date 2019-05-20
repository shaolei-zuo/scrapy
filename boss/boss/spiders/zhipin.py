# -*- coding: utf-8 -*-
import scrapy
from boss.items import BossItem


class ZhipinSpider(scrapy.Spider):
    name = 'zhipin'

    def start_requests(self):
        urls = ['https://www.zhipin.com/job_detail/?query=%E6%95%B0%E6%8D%AE&city=101020100&industry=&position=']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        jobs = response.xpath('//div[@class = "job-primary"]')
        for job in jobs:
            item = BossItem()
            item['post'] = job.xpath('./div/h3/a/div/text()').get()
            item['address'] = job.xpath('./div[@class="info-primary"]/p/text()').getall()[0]
            item['experience'] = job.xpath('./div[@class="info-primary"]/p/text()').getall()[1]
            item['education'] = job.xpath('./div[@class="info-primary"]/p/text()').getall()[2]
            item['company'] = job.xpath('./div[@class="info-company"]/div/h3/a/text()').get()
            item['companyinfo'] = job.xpath('./div[@class="info-company"]/div/p/text()').getall()

            detail_page = job.xpath('./div/h3/a/@href').get()
            detail_page = response.urljoin(detail_page)
            if detail_page is not None:
                detail_page = response.urljoin(detail_page)
                yield scrapy.Request(url=detail_page,  meta={'item': item}, callback=self.parse_detail)

        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_detail(self, response):
        detail = response.xpath(
            '//div[@class="job-sec"]/h3[contains(text(), "职位描述")]' +
            '/following-sibling::div[@class="text"]//text()').getall()
        item = response.meta['item']
        item['detail'] = detail
        yield response.meta






