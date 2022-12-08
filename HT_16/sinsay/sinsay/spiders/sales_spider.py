"""Sales sinsay"""

from scrapy import Spider

class SinSaySpider(Spider):
    name ='sales'
    start_urls = ["https://www.sinsay.com/ua/uk/spetsialna-propozytsiya/woman/sb/0/s/xxs-i-ua-40_xs"]

    def parse(self, response, **kwargs):
        for item in response.css("section#categoryProducts article.es-product figcaption.es-product-name"):
            yield {
                "title": item.css("h1::text").extract_first(),
                "url_product": item.css("a::attr(href)").extract_first(),
            }
