from urllib.parse import urlparse, parse_qs, unquote
import json


def extract_yelp_path(long_url):
    """
    Takes a long URL as input and returns the shortened Yelp path.

    :param long_url: The long URL as a string
    :return: Shortened Yelp path or None if not found
    """
    # Parsing the URL query string to get parameters
    query_string = urlparse(long_url).query
    params = parse_qs(query_string)

    # Extracting and decoding the Yelp redirect URL from parameters
    redirect_url = params.get('redirect_url', [None])[0]

    # If there's a redirect URL, extract its path
    if redirect_url:
        yelp_path = urlparse(redirect_url).path
        return yelp_path
    else:
        return long_url

def extract_website_address(long_url):
    """
    Extracts the final website address from a Yelp ad redirect URL.

    :param long_url: The long Yelp ad redirect URL as a string
    :return: The final website address or None if not found
    """
    # Parsing the query string to get the 'redirect_url' parameter
    query_string = urlparse(long_url).query
    params = parse_qs(query_string)

    # Extracting the first level 'redirect_url' parameter
    first_redirect_url = params.get('redirect_url', [None])[0]

    # If there's a first level redirect URL, parse it for further processing
    if first_redirect_url:
        # Decoding the first redirect URL
        decoded_url = unquote(first_redirect_url)

        # Parsing the decoded URL to extract the 'url' parameter
        second_params = parse_qs(urlparse(decoded_url).query)
        final_website_url = second_params.get('url', [None])[0]

        return final_website_url
    else:
        return long_url


def clean_item(item):
    """
    Cleans the URLs in a single item.
    """
    # Clean "Business yelp url" if it starts with ad redirect
    if item["Business yelp url"].startswith("/adredir?"):
        item["Business yelp url"] = extract_yelp_path(item["Business yelp url"])

    # Clean "Business website" if it starts with ad redirect
    if item["Business website"] and item["Business website"].startswith("/adredir?"):
        item["Business website"] = extract_website_address(item["Business website"])

    return item


def process_json_file(input_filename, output_filename):
    """
    Processes a JSON file to clean up the URLs in each item.
    """
    with open(input_filename, 'r', encoding='utf-8') as file:
        data = json.load(file)

    cleaned_data = [clean_item(item) for item in data]

    with open(output_filename, 'w', encoding='utf-8') as file:
        json.dump(cleaned_data, file, indent=4, ensure_ascii=False)


# Example usage
input_filename = 'output_2024-04-09_14-59-51.json'
output_filename = input_filename + '___cleaned.json'
process_json_file(input_filename, output_filename)