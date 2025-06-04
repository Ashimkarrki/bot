import logging
import os
import sys
import scrapy
import redis
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
load_dotenv()
logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger('scrapy').propagate = False
# host=os.getenv("DEV_HOST")
host=os.getenv("PROD_HOST")

r = redis.Redis(host=host, port=6379, db=0)
outputResponse = []
class NewsListSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
    "https://www.onlinekhabar.com/latest"]

    def parse(self, response):
        linkList=response.xpath('//div[@class="ok-news-post"]')
        for link in  linkList:
            outputResponse.append(link.css('a::attr("href")').get())
        next_page = response.css('div.ok-pagination-wrap a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })
    process.crawl(NewsListSpider)
    process.start()
    links=list(set(outputResponse))
    print("Total links found ", len(links))
    if len(sys.argv)==2 and  sys.argv[1]=="initial":
        r.delete("newlinks")
        r.delete("oldlinks")
        for l in links:
            r.lpush("newlinks",str(l))
            r.lpush("oldlinks",str(l))
        print("The links are initialized. Now schedule the script to get new links from now on.")

    else:
        r.delete("newlinks")
        for l in links:
            r.lpush("newlinks",str(l))
