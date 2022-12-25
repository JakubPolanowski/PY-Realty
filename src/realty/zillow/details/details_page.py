import json
import requests
from bs4 import BeautifulSoup
from numbers import Number
from typing import Dict, Any, Tuple
from .. import defaults


class Details_Page:
    """Static class which contains methods that are more or less generalizable to detail page parsing of Sales, Rental Homes, and Rental Apartments
    """

    @staticmethod
    def get_page(url: str, headers: Dict = defaults.HEADER) -> requests.Response:
        """Submits a GET request to the detail URL to get the page.

        Args:
            url (str): The detail URL. Note that invalid URL will lead to unexpected results and errors
            headers (Dict, optional): The request headers. Incorrect headers may lead to invalid results. It is recommended to leave as default. Defaults to defaults.HEADER.

        Returns:
            requests.Response: The page GET response
        """
        return requests.get(url, headers)

    @staticmethod
    def make_soup(page: requests.Response) -> BeautifulSoup:
        """This is a very simple function that has barely a reason to exist. Just takes the response content and has it parsed by Beautiful Soup via its html parser.

        Args:
            page (requests.Response): The GET response from a valid GET requests on the detail URL page

        Returns:
            BeautifulSoup: Page HTML parsed as a BeautifulSoup Object
        """

        soup = BeautifulSoup(page.content, "html.parser")

        return soup

    @staticmethod
    def get_api_preload(soup: BeautifulSoup) -> Dict[Any, Any]:
        """Extracts and parses the API preload cache from the page soup.

        Args:
            soup (BeautifulSoup): The html page soup object

        Returns:
            Dict[Any, Any]: The api preload cache dictionary
        """

        preload = soup.find("script", id="hdpApolloPreloadedData").text
        preload = json.loads(preload)
        preload['apiCache'] = json.loads(preload['apiCache'])
        return preload

    @staticmethod
    def get_variant_and_full_from_preload(preload: Dict[Any, Any]) -> Tuple[Dict[Any, Any], Dict[Any, Any]]:
        """Gets the variant and full API caches from the preload dictionary.

        Args:
            preload (Dict[Any, Any]): The preload dictionary obtained via get_api_preload

        Raises:
            KeyError: Unexpected key within apiCache

        Returns:
            Tuple[Dict[Any, Any], Dict[Any, Any]]: variant api cache dictionary, full api cache dictionary
        """

        for k in preload['apiCache'].keys():
            if 'Variant' in k:
                var_key = k
            elif 'Full' in k:
                full_key = k
            else:
                raise KeyError(
                    "Unexpected key in apiCache dictionary of preload dictionary")

        return preload['apiCache'][var_key], preload['apiCache'][full_key]

    @staticmethod
    def get_next_data(soup: BeautifulSoup) -> Dict[Any, Any]:
        """Extracts and parses the NEXT_DATA cache from the page soup.

        Args:
            soup (BeautifulSoup): The html page soup object

        Returns:
            Dict[Any, Any]: The api preload cache dictionary
        """

        ndata = soup.find("script", id="__NEXT_DATA__").text
        ndata = json.loads(ndata)

        return ndata

    @staticmethod
    def get_initial_data_and_redux_state(ndata: Dict[Any, Any]) -> Tuple[Dict[Any, Any], Dict[Any, Any]]:
        """Gets the initial Data and Redux State from the ndata (next data) dictionary.

        Args:
            ndata (Dict[Any, Any]): The ndata dictionary obtained via get_next_data

        Returns:
            Tuple[Dict[Any, Any], Dict[Any, Any]]: initialData dictionary, initialReduxState dictionary
        """

        props = ndata['props']
        return props['initialData'], props['initialReduxState']

    @staticmethod
    def get_walk_and_bike_score(zpid) -> Dict[str, Any]:
        """Gets the walk and bike details that appears on the Zillow details page

        Args:
            zpid (str): The Zillow property ID.

        Returns:
            Dict[str, Any]: Walk and bike score response dictionary
        """

        url = "https://www.zillow.com/graphql"
        querystring = {"zpid": zpid,
                       "operationName": "WalkTransitAndBikeScoreQuery"}

        payload = {
            "clientVersion": "home-details/6.1.1569.master.099cd8a",
            "operationName": "WalkTransitAndBikeScoreQuery",
            "query": "query WalkTransitAndBikeScoreQuery($zpid: ID!) {\n  property(zpid: $zpid) {\n    id\n    walkScore {\n      walkscore\n      description\n      ws_link\n    }\n    transitScore {\n      transit_score\n      description\n      ws_link\n    }\n    bikeScore {\n      bikescore\n      description\n    }\n  }\n}\n",
            "variables": {"zpid": zpid}
        }

        return requests.request(
            "POST", url, json=payload, headers=defaults.HEADER, params=querystring
        ).json()['data']

    @classmethod
    def parse_lot_size(cls, lot_size: str) -> Number:
        """Parses lot size string to sqft. Assumes that lot size will follow format of 'x Acres' or 'x.x Acres'.

        Args:
            lot_size (str): Zillow lot size string.

        Returns:
            Number: Lot size in sqft
        """
        if not 'Acres' in lot_size:
            ValueError("Expected to find 'Acres' in lot_size string, did not")

        acres = int(lot_size.replace("Acres", "").strip())
        return cls.calculate_acres_to_sqft(acres)

    @staticmethod
    def calculate_acres_to_sqft(acres: Number) -> Number:
        """Converts acres to sqft. 

        Conversion factor from https://www.metric-conversions.org/area/acres-to-square-feet.htm

        Args:
            acres (Number): Acres

        Returns:
            Number: sqft
        """
        return acres * 43560
