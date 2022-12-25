# This handles parsing of rental homes data
from typing import Dict, Any, List
from numbers import Number
from details_page import Preload_Detail_Page


class Rental_Home(Preload_Detail_Page):
    # TODO

    def __init__(self, url: str) -> None:
        """This initializes the Rental_Home object, which call a GET request on the Zillow detail URL. 

        Args:
            url (str): The Zillow Rental Property details URL.
        """

        super().__init__(url)
