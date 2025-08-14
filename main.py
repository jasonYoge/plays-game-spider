from scrapy.crawler import CrawlerProcess
from spiders.image_spider import ImageSpider  

def main():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    process.crawl(ImageSpider)
    process.start()

if __name__ == "__main__":
    main() 