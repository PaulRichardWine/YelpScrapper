from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from YelpScrapper.spiders.Yelp2 import YelpSpider2
from datetime import datetime


timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

#I've been thinking about putting the location and category name in the filename,
# but I've given up on that idea because it can cause unnecessary errors, so I'd have to add
# additional logic to validate input from the user to make sure it
# doesn't contain characters that might be invalid in the file names in the operating system.

process = CrawlerProcess(settings={
    **get_project_settings(),


    'FEEDS': {
        f'output_{timestamp}.json': {
            'format': 'json',
            'encoding': 'utf8',
            'indent': 4,
            'overwrite': True
        },
    },
})


category_name = input ("Enter category_name...")
location = input ("Enter location...")

process.crawl(YelpSpider2, category_name = category_name, location = location)

# or use te one below to not enter keyboard input everytime
# process.crawl(YelpSpider2, category_name = "contractors", location = "Los Angeles")

process.start()

