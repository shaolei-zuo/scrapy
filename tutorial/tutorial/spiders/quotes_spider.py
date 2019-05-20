import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.xpath('//div[@class = "quote"]'):
            text = quote.xpath('./span[@class = "text"]/text()').get()
            author = quote.xpath('.//small[@class = "author"]/text()').get()
            tags = quote.xpath('./div[@class = "tags"]/a[@class="tag"]/text()').getall()
            yield {"text": text, "author": author, "tags": tags}

        next_page = response.xpath('//li[@class = "next"]/a/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse())

