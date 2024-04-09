import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import unquote, urlparse, parse_qs
import re
import json



class YelpSpider(CrawlSpider):
    name = "Yelp"
    start_urls = ["https://www.yelp.pl/search?find_desc=restauracje&find_loc=Warszawa&request_origin=user"]



    rules = (
        Rule(LinkExtractor(allow=("start=",))),
        Rule(LinkExtractor(allow=("/biz/",), deny=("\?hrid=",)), callback = "parse_biz")
    )


    def parse_biz(self, response):
        '''
        This function is used to parse single business pages.
        '''

        print ("\nPARSE_BIZ")
        print(f"Processing: {response.url}")

        business_name = response.css('h1.css-hnttcw::text').get()
        business_rating = response.css('span.css-1fdy0l5::text').get()
        business_yelp_url = response.url

        try:
            encoded_url = response.css('div.css-1c9o6ng a.css-1idmmu3::attr(href)').get()
            if encoded_url:
                query_str = urlparse(encoded_url).query
                actual_url = parse_qs(query_str).get('url', [])[0]
                if actual_url:
                    business_website = unquote(actual_url)
                    print("business_website", business_website)
        except:
            ()

        try:
            reviews_text = response.css('a.css-19v1rkv::text').get()
            # regular expression for getting reviews number
            match = re.search(r'\((\d+)\s+reviews\)', reviews_text)
            if match:
                number_of_reviews = match.group(1)
                print ("number of reviews:", number_of_reviews)
        except:
            ()

        print("business_name:", business_name)
        print("business_yelp_url", business_yelp_url)
        print ("business_rating", business_rating)

        # Preparing data for callback API
        pre_collected_data = {
            "Business name": business_name,
            "Business rating": business_rating,
            "Number of reviews": number_of_reviews,
            "Business yelp url": business_yelp_url,
            "Business website": business_website
        }


        businessId = response.css('meta[name="yelp-biz-id"]::attr(content)').get()
        print ("businessId:", businessId)

        payload = json.dumps([
            {
                "operationName": "GetBusinessReviewFeed",
                "variables": {
                    "encBizId": businessId,
                    "reviewsPerPage": 5,
                    "selectedReviewEncId": "",
                    "hasSelectedReview": False,
                    "sortBy": "DATE_DESC",
                    "languageCode": "en",
                    "ratings": [5, 4, 3, 2, 1],
                    "isSearching": False,
                    "after": "",
                    "isTranslating": False,
                    "translateLanguageCode": "en",
                    "reactionsSourceFlow": "businessPageReviewSection",
                    "minConfidenceLevel": "HIGH_CONFIDENCE",
                    "highlightType": "",
                    "highlightIdentifier": "",
                    "isHighlighting": False
                },
                "extensions": {
                    "operationType": "query",
                    "documentId": "ef51f33d1b0eccc958dddbf6cde15739c48b34637a00ebe316441031d4bf7681"
                }
            }
        ])


        headers = {
            'Content-Type': 'application/json',
            'authority': 'www.yelp.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'x-apollo-operation-name': 'GetBusinessReviewFeed',
            'origin': 'https://www.yelp.com',
            'referer': response.url,
        }

        yield scrapy.Request(
            url="https://www.yelp.com/gql/batch",
            method='POST',
            headers=headers,
            body=payload,
            callback=self.parse_api_response,
            meta={'pre_collected_data': pre_collected_data}
        )

    def parse_api_response(self, response):
        pre_collected_data = response.meta['pre_collected_data']
        print (pre_collected_data)
        api_data = json.loads(response.text)


        reviews_edges = api_data[0]["data"]["business"]["reviews"]["edges"]

        reviews_final_list = []
        # Loop through the first 5 reviews in 'reviews_edges'
        for review in reviews_edges[:5]:
            review_data = {
                #"Review text": review["node"]["text"]["full"],
                "Reviewer name": review["node"]["author"]["displayName"],
                "Reviewer location": review["node"]["author"]["displayLocation"],
                "Review date": review["node"]["createdAt"]["utcDateTime"]
            }
            reviews_final_list.append(review_data)

        pre_collected_data['List of first 5 reviews'] = reviews_final_list

        pretty_pre_collected_data = json.dumps(pre_collected_data, indent=4)
        print (pretty_pre_collected_data)


        yield pre_collected_data

