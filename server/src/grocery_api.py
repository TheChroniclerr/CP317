import requests
import json
import pandas as pd
from serpapi import GoogleSearch

#takes item to search for in api calls 
def make_api_call(item):
    #url to amazon api
    url_amazon = "https://api-to-find-grocery-prices.p.rapidapi.com/amazon"
    #query of what to find in api call
    querystring_amazon = {"query":item,"country":"us","page":"1"}
    #api key for amazon
    headers_amazon = {
	"x-rapidapi-key": "8c1e48015cmsh7969212773f17a8p1edcaejsnd39e13360f91",
	"x-rapidapi-host": "api-to-find-grocery-prices.p.rapidapi.com"
}

    #walmart api key
    params = {
    "engine": "walmart",
    "query": item,
    "sort": "price_low",
    "page": 1,
    "api_key": "7d6b417cf7002e5ba57d4a7179f5e0c046b9c1614f39ec930a12e091378c61a1"
}
    #gets data from walmart and amazon
    response_amazon = requests.get(url_amazon, headers=headers_amazon, params=querystring_amazon)
    search = GoogleSearch(params)
    response_walmart = search.get_dict() 

    #check to make sure api call was successful
    if "organic_results" not in response_walmart:
        print("API call failed")
        exit()
   
    #checks make sure api call was successful
    if response_amazon.status_code != 200:
        print("API call failed:")
        exit()

    #get prices from walmart responses to be able to use in data frame 
    results_walmart = response_walmart["organic_results"]
    for item in results_walmart:
        primary = item.get("primary_offer", {})
        price_value = None
        if isinstance(primary, dict):
            price_value = primary.get("offer_price")
            item["price_value"] = price_value

    #get product data form amazon search results
    data_amazon = response_amazon.json()
    results_amazon = data_amazon.get("products", [])

    #create a data frame to store resuls
    df = pd.DataFrame(results_amazon)
    df2 = pd.DataFrame(results_walmart)
    min_price_amazon = None
    min_price_walmart = None
    link_amazon = None
    link_walmart = None

    #try to exract prices from amazon dataframe
    if "price" in df.columns:
        try:
            #convert prices to floats 
            df["price_value"] = df["rawPrice"].astype(float)
            min_index_amazon = df["price_value"].idxmin()
            min_row_amazon = df.loc[min_index_amazon]
            min_price_amazon = min_row_amazon["price_value"]
            # Get the link to the item if it exists
            link_amazon = min_row_amazon.get("amazonLink", "No link available")
        except Exception as e:
            print("Couldn't get price:", e)

    #try to extract prices from walmart data frame
    if "price_value" in df2.columns:
        try:
            # Convert prices to floats 
            df2["price_value"] = df2["price_value"].astype(float)
            min_index_walmart = df2["price_value"].idxmin()
            min_row_walmart = df2.loc[min_index_walmart]
            min_price_walmart = min_row_walmart["price_value"]
            #Get link to the item it if exists
            link_walmart = min_row_walmart.get("product_page_url", "No link available")
        except Exception as e:
            print("Couldn't get price:", e)
    return min_price_walmart, min_price_amazon, link_walmart, link_amazon
