# This handles parsing of sale data
import json
import requests
from typing import Dict, Any, List, Literal, Union, Set, Tuple
from bs4 import BeautifulSoup
from .. import defaults


class Sale:
    # TODO

    def __init__(self, url: str) -> None:

        self.url = url

        # get root props
        self.soup, self.preload = self.get_root_props_from_page(
            self.get_page(self.url)
        )

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
    def get_root_props_from_page(page: requests.Response) -> Tuple[BeautifulSoup, Dict[Any, Any]]:
        """This gets the root/top most props of the page, that being the html parsed to a BeautifulSoup object and a dictionary with the preloaded data.

        Args:
            page (requests.Response): The GET response from a valid GET requests on the detail URL page

        Returns:
            Tuple[BeautifulSoup, Dict[Any, Any]]: Page HTML parsed as a BeautifulSoup Object, Preloaded data parsed to a dictionary
        """

        soup = BeautifulSoup(page.content, "html.parser")
        preload = soup.find("script", id="hdpApolloPreloadedData").text
        preload = json.loads(preload)
        preload['apiCache'] = json.loads(preload['apiCache'])

        return soup, preload
