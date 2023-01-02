import json
import requests
from bs4 import BeautifulSoup
from numbers import Number
from typing import Dict, Any, Tuple, List
from .. import defaults


class Sale:

    def __init__(self, url: str) -> None:
        """This initializes the Preload_Detail_Page object, which call a GET request on the Zillow detail URL. 

        Args:
            url (str): The Zillow Property Sale details URL.
        """

        self.url = url

        # get soup
        self.soup = self.make_soup(self.get_page(self.url))

        # get ndata
        self.ndata = self.get_next_data(self.soup)

        # get initialState and propertyDetails
        self.initial_state = self.ndata['props']['pageProps']['initialState']
        self.property_details = self.initial_state['propertyDetails']

    @staticmethod
    def get_page(url: str, headers: Dict = defaults.HEADER) -> requests.Response:
        """Submits a GET request to the detail URL to get the page.

        Args:
            url (str): The detail URL. Note that invalid URL will lead to unexpected results and errors
            headers (Dict, optional): The request headers. Incorrect headers may lead to invalid results. It is recommended to leave as default. Defaults to defaults.HEADER.

        Returns:
            requests.Response: The page GET response
        """
        return requests.get(url, headers=headers)

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
