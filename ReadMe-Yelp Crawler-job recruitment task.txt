Yelp Crawler
Description:
The purpose is to develop a yelp crawler that scraps all the businesses from Yelp website.

Requirements:
The crawler should be given as an input:
1. Category name, ie - contractors
2. Location, ie - San Francisco, CA
The crawler should return a file with json objects, each json representing a business from the
given search results. Each business should have the following data:
● Business name
● Business rating
● Number of reviews
● Business yelp url
● Business website
● List of first 5 reviews, for each review:
○ Reviewer name
○ Reviewer location
○ Review date
Some notes:
● Using scrapy - an advantage but not a MUST
● Pay attention to which data you can get via XHR request (direct json api) and which data
you need to parse html
● You should build a solution that CAN get ALL the businesses, not some, even though
you don't need to actually run on all, just a sample to demonstrate that it works.