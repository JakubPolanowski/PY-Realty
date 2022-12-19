# This handles parsing of sale data
import json
import requests
from typing import Dict, Any, List, Literal, Union, Set, Tuple
from numbers import Number
from bs4 import BeautifulSoup
from .. import defaults


class Sale:
    """This class extracts the properties/details of a property Sale from Zillow's detail URL page. 

    While most of the key details can be easily access via the class attributes or functions, there are some more advanced details that not parsed/organized by this class. For the full html page, see the soup attribute. Additionally check the variant_cache and the full_cache for the complete dictionaries of the api cache. 

    Attributes:
        url (str): The detail URL that this class has parsed
        soup (BeautifulSoup): The html content of this page parsed to a soup object
        preload (Dict[Any, Any]): The complete api cache preload
        zpid (int): The Zillow property ID
        variant_cache (Dict[Any, Any])
    """

    def __init__(self, url: str) -> None:
        """This initializes the sale object, which call a GET request on the Zillow detail URL. 

        Args:
            url (str): The Zillow Property Sale details URL.
        """

        self.url = url

        # get soup
        self.soup = self.make_soup(self.get_page(self.url))

        # get api preload
        self.preload = self.get_api_preload(self.soup)
        self.zpid: int = self.preload['zpid']

        # get caches
        self.variant_cache, self.full_cache = self.get_variant_and_full_from_preload(
            self.preload)

        # quick access values
        self.property: Dict[Any, Any] = self.full_cache['property']

        self.home_type: str = self.property['homeType']
        self.year_built: int = self.property['yearBuilt']
        self.parcel_number: str = self.property['parcelNumber']

        self.price: int = self.property['price']
        self.zestimate: int = self.property['zestimate']
        self.rental_zestimate: int = self.property['rentZestimate']
        self.tax_history: List[Dict[str, Number]] = self.property['taxHistory']
        self.price_history: List[Dict[str, Any]
                                 ] = self.property['priceHistory']
        self.currency: str = self.property['currency']

        self.status: str = self.get_status()
        self.days_on_zillow: int = self.property['daysOnZillow']
        self.views: int = self.property['pageViewCount']
        self.saves: int = self.property['favoriteCount']

        self.tags: List[str] = self.get_tags()
        self.description: str = self.property['description']

        self.address: Dict[str, Any] = self.property['address']
        self.street_address: str = self.address['streetAddress']
        self.city: str = self.address['city']
        self.state: str = self.address['state']
        self.zip: str = self.address['zopcode']
        self.latitude: float = self.property['latitude']
        self.longitutde: float = self.property['longitude']

        self.bedrooms: Number = self.property['bedrooms']
        self.bathrooms: Number = self.property['bathrooms']

        self.interior_sqft: Number = self.property['livingArea']

        self.appliances: List[str] = self.property['appliances']
        self.cooling: List[str] = self.property['cooling']
        self.heating: List[str] = self.property['heating']
        self.community_features: List[str] = self.property['communityFeatures']
        self.fireplaces: Number = self.property['fireplaces']
        self.garage: bool = self.property['hasGarage']
        self.interior_features: List[str] = self.property['interiorFeatures']

        self.attic: str | None = self.property['attic']
        self.basement: str = self.property['basement']

        self.hoa_fee: Number | None = self.property['hoaFee']

        self.levels: str = self.property['levels']

        self.lot_features: List[str] | None = self.property['lotFeatures']
        self.lot_size: str = self.property['lotSize']
        self.lot_size_dimensions: str = self.property['lotSizeDimensions']
        self.lot_sqft: Number = self.parse_lot_size(self.lot_size)

        self.sewer: List[str] = self.property['sewer']
        if self.sewer:
            self.sewer = self.sewer[0]
        self.water_source: List[str] = self.property['waterSource']
        if self.water_source:
            self.water_source = self.water_source[0]

        self.attribution: Dict[str, Any] = self.property['attributionInfo']

        self.schools: List[Dict[str, Any]] = self.property['schools']
        self.similar: List[Dict[str, Any]] = self.property['comps']
        self.nearby: List[Dict[str, Any]] = self.property['nearbyHomes']

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

    def get_status(self) -> str | None:
        """Gets the status of the house listing.

        Returns:
            str: The house status
        """

        return self.soup.find("span", "iOiapS").text

    def get_likely_to_sell(self) -> str:
        """Gets the Zillow likely to sell estimation.

        Returns:
            str | None: Zillow likely to sell estimation. Returns None if there is none
        """
        tag = self.soup.find("p", "kHeRng")

        if not tag:
            return tag
        else:
            return tag.text.replace(u'\u200a', '')

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

    def get_at_a_glance(self) -> Dict[str, Any]:
        """Gets the Zillow at a glance facts.

        Returns:
            Dict[str, Any]: Returns a dictionary of the at a glance facts.
        """

        glance = {}
        for pair in self.property['atAGlanceFacts']:
            for key, value in pair.items():
                glance[key, value]

        return glance

    def get_tags(self) -> List[str]:
        """Gets the taglines on the page

        Returns:
            List[str]: List of taglines
        """

        return [tag.text for tag in self.soup.find("div", "jOTCMt").find_all("span")]

    def get_facts_and_features(self) -> Dict[str, Any]:
        """Gets the Zillow facts and features section of the webpage as a dictionary

        Returns:
            Dict[str, Any]: Facts and features dictionary
        """

        return {tag.h5.text: {
            stag.h6.text: [
                li.text for li in stag.ul.find_all('li')
            ] for stag in tag.find_all("div")
        } for tag in self.soup.find_all("div", "jCOrgb")}

    def get_walk_and_bike_score(self) -> Dict[str, Any]:
        """Gets the walk and bike details that appears on the Zillow details page

        Returns:
            Dict[str, Any]: Walk and bike score response dictionary
        """

        url = "https://www.zillow.com/graphql"
        querystring = {"zpid": self.zpid,
                       "operationName": "WalkTransitAndBikeScoreQuery"}

        payload = {
            "clientVersion": "home-details/6.1.1569.master.099cd8a",
            "operationName": "WalkTransitAndBikeScoreQuery",
            "query": "query WalkTransitAndBikeScoreQuery($zpid: ID!) {\n  property(zpid: $zpid) {\n    id\n    walkScore {\n      walkscore\n      description\n      ws_link\n    }\n    transitScore {\n      transit_score\n      description\n      ws_link\n    }\n    bikeScore {\n      bikescore\n      description\n    }\n  }\n}\n",
            "variables": {"zpid": self.zpid}
        }

        return requests.request(
            "POST", url, json=payload, headers=defaults.HEADER, params=querystring
        ).json()['data']

    @staticmethod
    def calculate_monthly_mortgage(principal: Number, interest: Number, months: Number) -> Number:
        """Calculates the monthly mortgage payment. Formula from 

        Args:
            principal (Number): The principal for the mortgage (in this case home price minus the down payment)
            interest (Number): The interest rate as a monthly percentage (5% -> (5/100)/12)
            months (Number): Number of months on the mortagage

        Returns:
            Number: The monthly mortgage payment
        """
        return principal * (interest * (1+interest)**months) / ((1+interest)**months-1)

    def get_monthly_estimated_cost(self, down: Number, interest: Number = None, months: Number = 30, tax: Number = None, home_insurance: Number = None, mortgage_insurance: Number = 0, hoa_fee: Number = None, utilies: Number = 0) -> Number:
        """Estimates the monthly cost of buying the property. 

        Home insurance Zillow estimation formula based on Zillow javascript code:
        https://www.zillowstatic.com/s3/hdp/home-details/components/for-sale-shopper-platform/app-df284a1fbb.js 

        Args:
            down (Number): The money down. Typically 20%.
            interest (Number, optional): The interest rate. If not specifed (None) will use Zillow's estimated 30 year fixed rate. NOTE: Interest rate should be given as a decimal, so 5% -> 0.05. Defaults to None.
            months (Number, optional): The number of months on the mortgage. Defaults to 30.
            tax (Number, optional): The property tax rate. NOTE: tax rate should be given as a decimal so 5% -> 0.05. If not specified (None) will use property's current tax rate. Defaults to None.
            home_insurance (Number, optional): Home insurance monthly cost. If not specified (None) will estimate as 0.0042 * property price. This is how Zillow estimates. Defaults to None.
            mortgage_insurance (Number, optional): The mortgage monthly insurance cost. Typically this only occurs when the downpayment is less than 20% otherwise will be 0. Defaults to 0.
            hoa_fee (Number, optional): The monthly HOA fee. If not specified (None) will lookup the property HOA fee, if any. Defaults to None.
            utilies (Number, optional): The monthly cost of utilities. Should be manually specified otherwise will not be accounted for. Defaults to 0.

        Returns:
            Number: The estimated monthly cost
        """

        mortgage_monthly = self.calculate_monthly_mortgage(
            self.price - down, interest/12, months
        )
        if tax:
            pass
        elif not self.property['propertyTaxRate']:
            tax = 0
        else:
            tax = self.property['propertyTaxRate'] / 100

        tax_monthly = tax * self.price / 12

        if not home_insurance:
            home_insurance = self.price * 0.0042

        if hoa_fee:
            pass
        elif not self.property['monthlyHoaFee']:
            hoa_fee = 0
        else:
            hoa_fee = self.property['monthlyHoaFee']

        return sum([
            mortgage_monthly,
            mortgage_insurance,
            tax_monthly,
            home_insurance,
            hoa_fee,
            utilies
        ])
