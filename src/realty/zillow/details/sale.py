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

        # get soup
        self.soup = self.make_soup(self.get_page(self.url))

        # get api preload
        self.preload = self.get_api_preload(self.soup)
        self.zpid = self.preload['zpid']

        # get caches
        self.varient_cache, self.full_cache = self.get_variant_and_full_from_preload(
            self.preload)

        # quick access values
        self.property = self.full_cache['property']

        self.home_type = self.property['homeType']
        self.year_built = self.property['yearBuilt']
        self.parcel_number = self.property['parcelNumber']

        self.price = self.property['price']
        self.zestimate = self.property['zestimate']
        self.currency = self.property['currency']
        self.status = self.get_status()

        self.address = self.property['address']
        self.street_address = self.address['streetAddress']
        self.city = self.address['city']
        self.state = self.address['state']
        self.zip = self.address['zopcode']

        self.bedrooms = self.property['bedrooms']
        self.bathrooms = self.property['bathrooms']

        self.interior_sqft = self.property['livingArea']

        self.appliances = self.property['appliances']
        self.cooling = self.property['cooling']
        self.community_features = self.property['communityFeatures']
        self.fireplaces = self.property['fireplaces']
        self.garage = self.property['hasGarage']
        self.interior_features = self.property['interiorFeatures']

        self.attic = self.property['attic']
        self.basement = self.property['basement']

        self.hoa_fee = self.property['hoaFee']

        self.levels = self.property['levels']

        self.lot_features = self.property['lotFeatures']
        # TODO have this parsed to number
        self.lot_size = self.property['lotSize']
        self.lot_size_dimensions = self.property['lotSizeDimensions']

        self.sewer = self.property['sewer']  # TODO consider parsing?
        # Todo consider parsing?
        self.water_source = self.property['waterSource']

        self.attribution = self.property['attributionInfo']

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

    def get_status(self) -> str:
        """Gets the status of the house listing.

        Returns:
            str: The house status
        """

        return self.soup.find("span", "iOiapS").text
