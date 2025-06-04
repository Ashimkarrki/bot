import json
import logging
import os
import scrapy
import redis
from scrapy.crawler import CrawlerProcess
from dotenv import load_dotenv
load_dotenv();
logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger('scrapy').propagate = False

# host=os.getenv("DEV_HOST")
host=os.getenv("PROD_HOST")


r = redis.Redis(host=host, port=6379, db=0)
# r = redis.Redis(host='localhost', port=6379, db=0)
links=[]
data=[]

class NewsSpider(scrapy.Spider):
    name = "title"
    start_urls = links
    def parse(self, response):
        title = response.css('h1.entry-title::text').get()
        date=response.css('div.ok-news-post-hour span::text').get()
        if title==None:
            title = response.css('div.single-post-heading h1::text').get().strip()
        if date==None:
            date=response.xpath('//div[@class="article-posted-date"]//text()').getall()[-1].strip()
        content=""
        for p in response.css("div.ok18-single-post-content-wrap p::text"):
            if content=="":
                content=str(p)
            else:
                content=content+"\n"+str(p)
        data.append({
                "title": title,
                "date":date,
                "content":content
        })

if __name__ == "__main__":

    
    redisList=r.lrange("newlinks",0,-1)
    newLinks=[x.decode() for x in redisList]
    redisList=r.lrange("oldlinks",0,-1)
    oldLinks=[x.decode() for x in redisList]


    for link in newLinks:
        if link not in oldLinks:
            links.append(link)

    print(f'Found {len(links)} new news')
    if len(links) !=0:
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        })
        process.crawl(NewsSpider)
        process.start()
    
    r.delete("news")
    for n in data:
        r.rpush('news', json.dumps(n))

    r.delete("newlinks")
    r.delete("oldlinks")

    for l in newLinks:
        r.lpush("oldlinks",str(l))
    print("Content extracted")
