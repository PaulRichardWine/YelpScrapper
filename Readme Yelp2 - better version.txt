Python - version 3.10


Second version of Yelp spider bases on direct API Json requests. It is more elegant and gives expected output.
You can run a spider from main2.py or from terminal.

The code connects to two API endpoints. First 'https://www.yelp.pl/search/snippet', that contains most of the
needed information, and second API endpoint for reviews.

Horizontal transition to other snippet api sites is based on calculation based information about
total number of results, number of results per page and currents start number, that is fetched from search page snippet.

In some areas, like Los Angeles, there can be some sponsored ads amongs results. They have longer form of url with redirect.
I decided not to clean it during fetching data to not increase risk of errors. I've made separate  module
clean_ad_ulrs.py, that can be run on json file to clean the data after scrapping is finished.



What is missing:

Error handling for entire code.

All free code that parses responses from json could be dressed up in functions with a decorator with a try/except block,
where in the case of an error, it does not interrupt the operation of the program,
but saves information about the error in a file, for example errors.txt.
Functions that retrieve data from json responses can also check if the values meet certain conditions,
e.g. type, but also value content. In case of an unexpected value, the function can raise error so that the
try/except decorator saves the case in the errors.txt file to analise it later.

For example, a function that checks whether the retrieved values business_yelp_url and business_website
would allow you to see that some of the results you download are not generic Yelp results, but sponsored ads.
In this case, a decision must be made whether to save or filter such results.

Also it could be useful to add code in case there is no output - checking what is the cause,
for example if there is a connection to the network,
or ir there are no Yelp results in a particular category/location, or if the input is in the wrong format, etc.
For example, selecting Tbilisi as a location doesn't give results because Yelp doesn't seem to work in Georgia.