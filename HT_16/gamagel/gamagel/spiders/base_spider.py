"""Self-study"""
from scrapy import Spider


class BasesGelSpider(Spider):
    """Base gel parser"""
    name = "bases"
    allowed_domains = ["gamagel.com.ua"]
    start_urls = ["https://gamagel.com.ua/bazi/"]

    def parse(self, response, **kwargs):
        """
        parse page
        """
        # Products on the current page
        for item in response.css("div.catalogCard-title"):
            item_url = item.css("a::attr(href)").extract_first()
            if item_url:
                yield response.follow(
                    item_url, callback=self.parse_product, dont_filter=True
                )
        # Pagination
        last_page = response.css(
            "div.pager__container"
            "span.pager__item-text::text").getall()[-3].strip("\n ")

        for i in range(1, int(last_page) + 1):
            yield response.follow(
                f"{self.start_urls[0]}filter/page={i}/",
                callback=self.parse_product,
                dont_filter=True,
            )

    def parse_product(self, response):
        """
        parse product
        """
        # Information about an individual product
        yield {
            "name": response.css("h1.product-title::text").get().strip(),
            "url": response.url,
            "description": response.css("div.text p::text").get().strip(),
            "img_url": self.allowed_domains[0] +
                       response.css(
                           "img.gallery__photo-img::attr(src)").get().strip(),
            "volume": ", ".join([i.strip("\n ") for i in response.css(
                "div.modification__list a::text").getall()]),
            "category": response.css(
                "nav.breadcrumbs span::text").getall()[-2].strip()
        }
