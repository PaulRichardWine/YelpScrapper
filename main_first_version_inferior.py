from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from YelpScrapper.spiders.Yelp_first_version_inferior import YelpSpider


process = CrawlerProcess(get_project_settings())

# dehash only one of the options below at the time.

# dehash to run first spider.
process.crawl(YelpSpider)

process.start()


