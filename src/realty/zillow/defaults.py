URL = "https://www.zillow.com/search/GetSearchPageState.htm"
# The URL for the API request

HEADER = {  # Headers to be passed in the request (required to get results)
    "authority": "www.zillow.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

GRAPHQL_HEADER = {
    "authority": "www.zillow.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.7",
    "client-id": "vertical-living",
    "content-type": "application/json",
    "origin": "https://www.zillow.com",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}
