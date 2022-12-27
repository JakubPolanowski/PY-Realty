import json
import requests
from bs4 import BeautifulSoup
from numbers import Number
from typing import Dict, Any, Tuple, List
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
    def get_walk_and_bike_score(zpid: str) -> Dict[str, Any]:
        """Gets the walk and bike details that appears on the Zillow details page

        Args:
            zpid (str): The Zillow property ID.

        Returns:
            Dict[str, Any]: Walk and bike score response dictionary
        """

        url = "https://www.zillow.com/graphql"

        payload = {
            "clientVersion": "home-details/6.1.1569.master.099cd8a",
            "operationName": "WalkTransitAndBikeScoreQuery",
            "query": "query WalkTransitAndBikeScoreQuery($zpid: ID!) {\n  property(zpid: $zpid) {\n    id\n    walkScore {\n      walkscore\n      description\n      ws_link\n    }\n    transitScore {\n      transit_score\n      description\n      ws_link\n    }\n    bikeScore {\n      bikescore\n      description\n    }\n  }\n}\n",
            "variables": {"zpid": zpid}
        }

        return requests.request(
            "POST", url, json=payload, headers=defaults.HEADER
        ).json()['data']

    @classmethod
    def parse_lot_size(cls, lot_size: str) -> Number:
        """Parses lot size string to sqft. Assumes that lot size will follow format of 'x Acres' or 'x.x Acres'.

        Args:
            lot_size (str): Zillow lot size string.

        Returns:
            Number: Lot size in sqft
        """
        if not lot_size:
            return None

        lot_size = lot_size.lower()

        if 'acres' in lot_size:
            acres = float(lot_size.replace(
                "acres", "").replace(",", "").strip())
            return cls.calculate_acres_to_sqft(acres)
        elif "sqft" in lot_size:
            sqft = float(lot_size.replace("sqft", "").replace(",", "").strip())
            return sqft
        else:
            raise ValueError(
                f"Expected to find 'acres' or 'sqft' but found neither - {lot_size}")

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


class NextJS_Detail_Page(Details_Page):

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


class Preload_Detail_Page(Details_Page):

    def __init__(self, url: str) -> None:
        """This initializes the Preload_Detail_Page object, which call a GET request on the Zillow detail URL. 

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

        self.price: int = self.property['price']
        self.zestimate: int = self.property['zestimate']
        self.rental_zestimate: int = self.property['rentZestimate']
        self.tax_history: List[Dict[str, Number]] = self.property['taxHistory']
        self.price_history: List[Dict[str, Any]
                                 ] = self.property['priceHistory']
        self.currency: str = self.property['currency']

        self.status: str = self.property['homeStatus']
        self.days_on_zillow: int = self.property['daysOnZillow']
        self.views: int = self.property['pageViewCount']
        self.saves: int = self.property['favoriteCount']

        self.tags: List[str] = self.get_tags()
        self.description: str = self.property['description']

        self.address: Dict[str, Any] = self.property['address']
        self.street_address: str = self.address['streetAddress']
        self.city: str = self.address['city']
        self.state: str = self.address['state']
        self.zip: str = self.address['zipcode']
        self.latitude: float = self.property['latitude']
        self.longitutde: float = self.property['longitude']

        self.bedrooms: Number = self.property['bedrooms']
        self.bathrooms: Number = self.property['bathrooms']

        self.interior_sqft: Number = self.property['livingArea']

        self.appliances: List[str] = self.property['resoFacts']['appliances']
        self.cooling: List[str] = self.property['resoFacts']['cooling']
        self.heating: List[str] = self.property['resoFacts']['heating']
        self.community_features: List[str] = self.property['resoFacts']['communityFeatures']
        self.fireplaces: Number = self.property['resoFacts']['fireplaces']
        self.garage: bool = self.property['resoFacts']['hasGarage']
        self.interior_features: List[str] = self.property['resoFacts']['interiorFeatures']

        self.attic: str | None = self.property['resoFacts']['attic']
        self.basement: str | None = self.property['resoFacts']['basement']

        self.hoa_fee: Number | None = self.property['resoFacts']['hoaFee']

        self.levels: str | None = self.property['resoFacts']['levels']

        self.parking: List[str] | None = self.property['resoFacts']['parkingFeatures']
        self.lot_features: List[str] | None = self.property['resoFacts']['lotFeatures']
        self.lot_size: str | None = self.property['resoFacts']['lotSize']
        self.lot_size_dimensions: str = self.property['resoFacts'].get(
            'lotSizeDimensions', None)
        self.lot_sqft: Number = self.parse_lot_size(self.lot_size)

        self.sewer: List[str] | None = self.property['resoFacts']['sewer']
        self.water_source: List[str] | None = self.property['resoFacts']['waterSource']

        self.attribution: Dict[str, Any] = self.property['attributionInfo']

        self.schools: List[Dict[str, Any]] = self.property['schools']
        self.similar: List[Dict[str, Any]] = self.property['comps']
        self.nearby: List[Dict[str, Any]] = self.property['nearbyHomes']

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

    def get_at_a_glance(self) -> Dict[str, Any]:
        """Gets the Zillow at a glance facts.

        Returns:
            Dict[str, Any]: Returns a dictionary of the at a glance facts.
        """

        at_a_glance_dict = self.property['resoFacts']['atAGlanceFacts']

        if at_a_glance_dict:
            glance = {}
            for pair in at_a_glance_dict:
                glance[pair['factLabel']] = pair['factValue']

            return glance
        else:
            return {}

    def get_tags(self) -> List[str]:
        """Gets the taglines on the page

        Returns:
            List[str]: List of taglines
        """
        homeinsights = self.property.get('homeInsights', [{}])
        if not homeinsights:
            return []

        return list(
            {
                tag for tag_model in homeinsights[0]
                .get('insights', {}) for tag in tag_model.get('phrases', [])
            }
        )

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
