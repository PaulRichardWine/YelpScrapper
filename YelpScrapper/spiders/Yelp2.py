from jsonpath_ng import parse
import scrapy
import json
from urllib.parse import urlencode


class YelpSpider2(scrapy.Spider):
    name = "Yelp2"

    def start_requests(self):
        # API endpoint for Yelp search
        api_url = 'https://www.yelp.pl/search/snippet'

        category_name = self.category_name if hasattr(self, 'category_name') else input("Enter category name...")
        location = self.location if hasattr(self, 'location') else input("Enter location...")

        # Query parameters for the API request
        params = {
            'find_desc': category_name,
            'find_loc': location,
        }

        # Full URL with query parameters
        self.full_url = f"{api_url}?{urlencode(params)}"


        # Making the request to the API
        yield scrapy.Request(url=self.full_url, callback=self.parse_snippet_api_response)

    def parse_snippet_api_response(self, response):
        # Converting the response body from bytes to a dictionary
        snippet_data = json.loads(response.text)


        # Horizontal transition to other snippet api requests

        # I chose not to use the entire path because along the way I would have to apply a selector "[12]"
        # based only on the order of the items in the list, which could change in the future
        totalResults = [match.value for match in parse('$..totalResults').find(snippet_data)][0]
        print("totalResults:", totalResults)
        resultsPerPage = [match.value for match in parse('$..resultsPerPage').find(snippet_data)][0]
        print("resultsPerPage:", resultsPerPage)
        startResult = [match.value for match in parse('$..startResult').find(snippet_data)][0]
        print("startResult:", startResult)

        if resultsPerPage + startResult < totalResults:
            next_startResult = startResult + resultsPerPage
            print ("next_startResult:", next_startResult)
            next_page_url = self.full_url + "&start=" + str(next_startResult)
            print ("next_page_url:", next_page_url)

            yield scrapy.Request(next_page_url, callback=self.parse_snippet_api_response)


        # dehash return statement below to see how horizontal transition works without vertical actions
        # return


        # Vertical actions:
        # Extracting values from snippet api json

        mainContent_list = snippet_data["searchPageProps"]["mainContentComponentsListProps"]
        for element in mainContent_list:
            bizId = element.get("bizId")
            if bizId:
                print ("bizId:", bizId)
                business_name = element["searchResultBusiness"].get("name")
                print ("business_name:", business_name)
                business_yelp_url = element["searchResultBusiness"].get("businessUrl")
                print ("business_yelp_url:", business_yelp_url)
                business_rating = element["searchResultBusiness"].get("rating")
                print("business_rating:", business_rating)
                number_of_reviews = element["searchResultBusiness"].get("reviewCount")
                print ("number_of_reviews:", number_of_reviews)

                if "website" in element["searchResultBusiness"] and element["searchResultBusiness"][
                    "website"] is not None:
                    business_website = element["searchResultBusiness"]["website"].get("href")
                else:
                    business_website = None

                print("business_website:", business_website)
                print("\n")


                pre_collected_data = {
                    "Business name": business_name,
                    "Business rating": business_rating,
                    "Number of reviews": number_of_reviews,
                    "Business yelp url": business_yelp_url,
                    "Business website": business_website
                }

                print ("bizId:", bizId)

                payload = json.dumps([
                    {
                        "operationName": "GetBusinessReviewFeed",
                        "variables": {
                            "encBizId": bizId,
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
                    callback=self.parse_review_api_response,
                    meta={'pre_collected_data': pre_collected_data}
                )

    def parse_review_api_response(self, response):
        pre_collected_data = response.meta['pre_collected_data']
        # print (pre_collected_data)
        api_data = json.loads(response.text)

        reviews_edges = api_data[0]["data"]["business"]["reviews"]["edges"]

        reviews_final_list = []
        # Loop through the first 5 reviews in 'reviews_edges'
        for review in reviews_edges[:5]:
            review_data = {
                #"Review text": review["node"]["text"]["full"], #dehash to include review text
                "Reviewer name": review["node"]["author"]["displayName"],
                "Reviewer location": review["node"]["author"]["displayLocation"],
                "Review date": review["node"]["createdAt"]["utcDateTime"]
            }
            reviews_final_list.append(review_data)

        pre_collected_data['List of first 5 reviews'] = reviews_final_list

        # Print the prettified string
        pretty_pre_collected_data = json.dumps(pre_collected_data, indent=4)
        print(pretty_pre_collected_data)

        yield pre_collected_data


