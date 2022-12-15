"""
Використовуючи Scrapy,
заходите на "https://chrome.google.com/webstore/sitemap"
переходите на кожен лінк з тегів <loc>, з кожного лінка берете посилання на
сторінки екстеншинів, парсите їх і зберігаєте в CSV файл ID, назву та короткий
пис кожного екстеншена (пошукайте уважно де його можна взяти).
Наприклад:
“aapbdbdomjkkjkaonfhkkikfgjllcleb”,
“Google Translate”,
“View translations easily as you browse the web. By the Google Translate team.”
"""

from scrapy.crawler import CrawlerProcess

from chrome.chrome.spiders.chromegoogle import ChromegoogleSpider


def main():
    """Main function"""

    process = CrawlerProcess(settings={
        "FEEDS": {
            "out_file.csv": {  # CSV file
                "format": "csv",
                "header": True,
                "encoding": "utf-8",
                "indent": True,
                "overwrite": True},
        },
    })

    process.crawl(ChromegoogleSpider)
    process.start()


if __name__ == '__main__':
    main()
