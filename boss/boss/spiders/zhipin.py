# -*- coding: utf-8 -*-
import scrapy


class ZhipinSpider(scrapy.Spider):
    name = 'zhipin'

    def start_requests(self):
        urls = ['https://www.zhipin.com/job_detail/?query=%E6%95%B0%E6%8D%AE&city=101020100&industry=&position=']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print(response.xpath("//div"))
        jobs = response.xpath('//div[@class = "job-primary"]')
        for job in jobs:
            post = job.xpath('./div/h3/a/div/text()').get()
            address = job.xpath('./div[@class="info-primary"]/p/text()').getall()[0]
            experience = job.xpath('./div[@class="info-primary"]/p/text()').getall()[1]
            education = job.xpath('./div[@class="info-primary"]/p/text()').getall()[2]
            company = job.xpath('./div[@class="info-company"]/div/h3/a/text()').get()
            companyinfo = job.xpath('./div[@class="info-company"]/div/p/text()').getall()
            # financing = job.xpath('./div[@class="info-company"]/div/p/text()').getall()[1]
            # print(post, address)
            # number = job.xpath('./div[@class="info-company"]/div/p/text()').getall()[2]
            yield {"post": post,
                   "address": address,
                   "experince": experience,
                   "education": education,
                   "company": company,
                   "companyinfo": companyinfo,
                   # "financing": financing,
                   # "number": number
                   }

        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)








