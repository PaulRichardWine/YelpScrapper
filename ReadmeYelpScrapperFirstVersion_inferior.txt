Yelp.py
It is first version of spider for fetching Yelp.com.
This version is inferior and mainly takes data from HTML code.
The code works, but it's not exactly polished. It does not get all the start pages, and also it does not take location
and category name as inputs. It would be easy to fix but I've already stopped working on this version.
I did this code at the beginning, getting acquainted with how Scrapy works.
But when I finished making it, it was clear to me that a decent Yelp scrapper should rather be based on JSON API queries.
And that's what Yelp2 spider is.
But I also left the code of that first spider as a curiosity.


First site:

For pagination I use CrawlSpider class with rule (LinkExtractor(allow=("start=",))),, it finds all the links containing
"start=" string. Duplicates are skipped by default. This is a ready-made solution provided by Scrapy, not very elegant but
seams to works well in this case. If it was not the case, I would try to use next button for pagination, like:
def parse(self, response):
        next_page_url = response.css('a.pagination-button__09f24__kbFYf::attr(href)').get()
        if next_page_url:
            yield response.follow(next_page_url, self.parse)

Later comment: I think this method only finds urls of start pages that are visible from the first pages, so just first 9 pages.
It would be easy to fix but I noticed it when I have already abandoned this version of spider,
because I focused on the spider that fetches the JSON API.

For finding single business pages, I take all the urls witch /biz/ in it from the main search pages.
Because all the single business pages urls was given in two url verions, I remove duplicates that contains additional
"\?hrid=..." line.

If you prefer, you can parse /biz/ urls from api:
https://www.yelp.pl/search/snippet?find_desc=restauracje&find_loc=Warszawa"
but it only shows first site anyway, so you would have to apply pagination
so I don't really see benefits.
The advantage is that the business ID variable is available in this json,
but we can still get it from the html of a single business page, so we would have to apply pagination anyways.

Single business site:
I used css selectors because they are precise and efficient and seam to work fine.
The downside of this solution is that CSS selectors on Yelp website look auto-generated.
So you may be worried that class names can change unpredictably.
If it is the case, you can use xpath selectors, like:
business_name_from_xpath = response.xpath('//h1/text()').get() or "".strip()
etc
You can also use json API on address url single_business_url/props?
to get single business page api json but it does not contain website address, and is generally not helpful.

For reviews I used API like in Yelp2 spider.


