import json
import requests
from bs4 import BeautifulSoup
from numbers import Number
from typing import Dict, Any, Tuple, List
from datetime import datetime
from .. import defaults


class Sale:
    """This class extracts the properties/details of for sale property from Realtor.com's detail URL page.

    While most of the key details can be easily accessed via the class attribute or functions, there are some bit of data that are not readily assigned to class attributes. This includes details of appliances, which can be found in the details attribute (Dict[str, Any]).

    Attribute:
        url (str): The detail URL that this class has parsed
        soup (BeautifulSoup): The html content of this page parsed to a soup object

        ndata (Dict): The __NEXT_DATA__ data dictionary pulled from the html soup
        initial_state (Dict): The initial state dictionary component of ndata
        property_details (Dict): propertyDetails component of the initial_state dictionary
        description (Dict): description component of the property_details dictionary. Contains key value pairs regarding to the description of the property
        location (Dict): location component of the property_details dictionary. Contains key value pairs regarding to the location of the property

        property_id (str): The realtor.com property id
        listing_date (str): The date the property was listed

        status (str): The status of the property
        price (int): The price of the property, in USD
        price_per_sqft (int): The price per sqft, rounded, in USD
        yearly_property_tax (Number): The yearly property tax - how much tax is paid on the property each year
        open_houses (Any): The open house information

        listing_description (str): The text description of the property
        details (Dict[str, Any]): The details of the property, including appliances, cooling, septic, etc.
        beds (int): Number of bedrooms
        baths (int): Number of bathrooms
        garage (int): The number of garages/number of car spaces that fit in the garage
        interior_sqft (int): The total sqft area of the interior
        lot_sqft (int): The total sqft area of the lot

        address (Dict[str, Any]): Data dictionary of key value pairs relating to the property's address
        city (str): The city 
        state_code (str): The state code
        state (str): The state
        county (str): The county
        latitude (float): The latitude coordinate of the property
        longitude (float): The longitude coordinate of the property
        zip (str): The zip code
        street_address (str): The street address
        fips (str): Federal Information Processing System code

        hoa_fee (int): The hoa fee (0 if none)

        property_history (List[Dict]): The property history (include sales, listing added, removed, etc.)
        tax_history (List[Dict]): The tax history of the property

        area_market_status (Dict): Realtor.com's description of the area's market status (for example it may state the housing market is 'hot')

        noise (str): The noise level status in the area

        schools (Dict): Nearby schools
        similar (Dict): Similar homes, according to Realtor.com

    """

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
        self.initial_state: Dict[str,
                                 Any] = self.ndata['props']['pageProps']['initialState']
        self.property_details: Dict[str,
                                    Any] = self.initial_state['propertyDetails']

        # additional important keys
        self.description: Dict[str, Any] = self.property_details['description']
        self.location: Dict[str, Any] = self.property_details['location']

        # quick access values

        self.property_id: str = self.property_details['property_id']
        self.listing_date: str = self.property_details['list_date']

        self.status: str = self.property_details['status']
        self.price: int = self.property_details['list_price']
        self.price_per_sqft: int = self.property_details['price_per_sqft']
        self.yearly_property_tax: Number = self.property_details['source']['raw']['tax_amount']
        self.year_built: int = self.description['year_built']
        self.open_houses: Any = self.property_details['open_houses']

        self.listing_description: str = self.description['text']
        self.details: Dict[str, Any] = self.property_details['details']
        self.beds: int = self.description['beds']
        self.baths: int = self.description['baths']
        self.garage: int = self.description['garage']
        self.interior_sqft: int = self.description['sqft']
        self.lot_sqft: int = self.description['lot_sqft']

        self.address: Dict[str, Any] = self.location['address']
        self.city: str = self.address['city']
        self.state_code: str = self.address['state_code']
        self.state: str = self.address['state']
        self.county: str = self.address['county']
        self.latitude: float = self.address['coordinate']['lat']
        self.longitude: float = self.address['coordinate']['lon']
        self.zip: str = self.address['postal_code']
        self.street_address = f"{self.address['line']}, {self.city}, {self.state_code} {self.zip}"
        self.fips: str = self.location['county']['fips_code']

        self.hoa_fee: int = self.property_details['hoa'].get('fee', 0)

        self.property_history: List[Dict[str, Any]
                                    ] = self.property_details['property_history']
        self.tax_history: List[Dict[str, Any]
                               ] = self.property_details['tax_history']

        self.area_market_status: Dict[str, Any] = self.location.get('postal_code', {}).get(
            'geo_statistics', {}).get('housing_market')

        self.noise: str = self.get_noise_metrics(
            self.latitude, self.longitude).get('local_text', 'Unknown')

        self.schools: Dict[str, Any] = self.property_details['schools']
        self.similar = self.get_similar_homes(self.property_id)

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

    @staticmethod
    def get_loan_estimates(
        home_price: int,
        down_payment: int,
        fips: str,
        state_code: str,
        yearly_property_tax: int | float,
        hoa_fee: int = 0,
    ) -> Dict[str, Any]:
        """Gets the loan estimates from Realtor.com

        Args:
            home_price (int): The home price
            down_payment (int): The downpayment amount. Note that Realtor.com typically uses 20%, smaller downpayments may not be handled by Realtor.com's API correctly.
            fips (str): The FIPS (Federal Information Processing System) code 
            state_code (str): The state code
            yearly_property_tax (int | float): The yearly property tax ammount
            hoa_fee (int, optional): The hoa fee. Defaults to 0.

        Returns:
            Dict[str, Any]: Returns the API response json
        """

        url = "https://www.realtor.com/api/v1/payments/calculate_property_loan"

        querystring = {
            "hoa_fees": hoa_fee,
            "fips": fips,
            "state": state_code,
            "home_price": home_price,
            "down_payment": down_payment,
            "veterans_benefits": "false",
            "property_tax": yearly_property_tax,
            "is_fees_included": "true",
            "app_name": "realtor_dot_com",
            "app_version": "0.0.1"
        }

        response = requests.request("GET", url, params=querystring)
        return response.json()['results']

    def get_estimated_monthly_payment(self, down_payment: int = None) -> Number:
        """Gets the estimated monthly payment.

        Args:
            down_payment (int, optional): The downpayment on the purchase. If set to None, will default to 20% of the home price. Defaults to None.

        Returns:
            Number: Returns the monthly payment estimate
        """

        if down_payment is None:
            down_payment = round(self.price * .2)

        results = self.get_loan_estimates(
            self.price,
            down_payment,
            self.fips,
            self.state_code,
            self.yearly_property_tax,
            self.hoa_fee
        )

        return results['mortgage_data']['monthly_payment']

    @staticmethod
    def get_noise_metrics(latitude: float, longitude: float) -> Dict[str, Any]:
        """Gets the noise metrics for the coordinates specified.

        Args:
            latitude (float): The latitude
            longitude (float): The longitude

        Returns:
            Dict[str, Any]: The noise metrics
        """

        noise_query = f"https://www.realtor.com/api/v1/maps/gstat/noise?lat={latitude}&lon={longitude}"

        response = requests.get(noise_query).json()

        return response['result']

    @staticmethod
    def get_flood_risk(property_id: str, headers: Dict = defaults.HEADER) -> Dict[str, Any]:
        """Gets the flood risk from Realtor.com's PUBLIC API

        Args:
            property_id (str): The Realtor.com property ID
            headers (Dict, optional): The request headers. Incorrect headers may lead to invalid results. It is recommended to leave as default. Defaults to defaults.HEADER.

        Returns:
            Dict[str, Any]: The flood risk data
        """

        url = "https://www.realtor.com/api/v1/hulk"

        querystring = {"client_id": "rdc-x", "schema": "vesta"}

        payload = {
            "query": "query GetLocalData($propertyId: ID!) {  home(property_id: $propertyId) {    local {      flood {        fsid        flood_factor_score        flood_factor_severity        flood_cumulative_30        flood_trend        flood_trend_paragraph        fema_zone        firststreet_url        flood_insurance_text        environmental_risk      trend_direction      insurance_requirement      insurance_rates {          provider_logo          provider_url          providers        }        insurance_quotes {          provider_name          provider_url          provider_logo          expires          price          home_coverage          contents_coverage          disclaimer        }      }    }  }}",
            "variables": {"propertyId": property_id}
        }

        response = requests.request(
            "POST", url, json=payload, headers=headers, params=querystring)
        return response.json()

    @staticmethod
    def get_fire_risk(property_id: str, headers: Dict = defaults.HEADER) -> Dict[str, Any]:
        """Gets the fire risk from Realtor.com's PUBLIC API

        Args:
            property_id (str): The Realtor.com property ID
            headers (Dict, optional): The request headers. Incorrect headers may lead to invalid results. It is recommended to leave as default. Defaults to defaults.HEADER.

        Returns:
            Dict[str, Any]: The fire risk data
        """

        url = "https://www.realtor.com/api/v1/hulk"

        querystring = {"client_id": "rdc-x", "schema": "vesta"}

        payload = {
            "query": "query GetLocalData($propertyId: ID!) {  home(property_id: $propertyId) {    local {      wildfire {        fsid        fire_factor_score        fire_factor_severity        fire_cumulative_30        fire_trend        fire_trend_paragraph        usfs_relative_risk        firststreet_url        fire_insurance_text        insurance_rates {          provider_logo          provider_url          providers        }      }    }  }}",
            "propertyId": property_id,
            "callfrom": "LDP",
            "nrQueryType": "WILDFIRE_RISK",
            "variables": {"propertyId": property_id},
            "isClient": True
        }

        response = requests.request(
            "POST", url, json=payload, headers=headers, params=querystring)
        return response.json()

    @staticmethod
    def get_value_estimates(
        property_id: str,
        start: datetime = datetime(datetime.now().year-3, 1, 1),
        end: datetime = datetime.now(),
        forecast_max: datetime = datetime(
            datetime.now().year, datetime.now().month + 6, 1),
        headers: Dict = defaults.HEADER
    ) -> Dict[str, Any]:
        """Gets the Realtor.com RealEstimate current and historic property value estimates

        Args:
            property_id (str): The Realtor.com property ID
            start (datetime, optional): The start time for the historic range. Defaults to datetime(datetime.now().year-3, 1, 1).
            end (datetime, optional): The end time for the historic range. Defaults to datetime.now().
            forecast_max (datetime, optional): The forecasting max. Defaults to datetime(datetime.now().year, datetime.now().month + 6, 1)
            headers (Dict, optional): The request headers. Incorrect headers may lead to invalid results. It is recommended to leave as default. Defaults to defaults.HEADER.

        Returns:
            Dict[str, Any]: The Relotr.com RealEstimate data
        """

        url = "https://www.realtor.com/api/v1/hulk"

        querystring = {"client_id": "rdc-x", "schema": "vesta"}

        payload = {
            "query": None,
            "queryLoader": {
                "appType": "FOR_SALE",
                "pageType": "LDP",
                "serviceType": "HOME_ESTIMATES"
            },
            "propertyId": property_id,
            "callfrom": "LDP",
            "nrQueryType": "HOME_ESTIMATES",
            "variables": {
                "propertyId": property_id,
                "historicalMin": start.strftime("%Y-%m-%d"),
                "historicalMax": end.strftime("%Y-%m-%d"),
                "forecastMax": forecast_max.strftime("%Y-%m-%d")
            },
            "isClient": True
        }

        response = requests.request(
            "POST", url, json=payload, headers=headers, params=querystring)
        return response.json()

    @staticmethod
    def get_nearby_home_values(property_id: str, headers: Dict = defaults.HEADER) -> List[Dict[str, Any]]:
        """Gets a list of nearby homes and their values

        Args:
            property_id (str): The Realtor.com property ID
            headers (Dict, optional): The request headers. Incorrect headers may lead to invalid results. It is recommended to leave as default. Defaults to defaults.HEADER.

        Returns:
            List[Dict[str, Any]]: The list of nearby homes and their values
        """

        url = "https://www.realtor.com/api/v1/hulk"

        querystring = {"client_id": "rdc-x", "schema": "vesta"}

        payload = {
            "query": None,
            "queryLoader": {
                "appType": "FOR_SALE",
                "pageType": "LDP",
                "serviceType": "NEARBY_HOME_VALUES"
            },
            "propertyId": property_id,
            "callfrom": "LDP",
            "nrQueryType": "NEARBY_HOME_VALUES",
            "variables": {"query": {
                "type": "nearby_homes",
                "property_id": property_id,
            }},
            "isClient": True,
            "isBot": "false"
        }

        response = requests.request(
            "POST", url, json=payload, headers=headers, params=querystring)
        return response.json()['data']['linked_homes']['results']

    @staticmethod
    def get_similar_homes(property_id: str, headers: Dict = defaults.HEADER) -> Dict[str, Any]:
        """Gets similar homes

        Args:
            property_id (str): The Realtor.com property ID
            headers (Dict, optional): The request headers. Incorrect headers may lead to invalid results. It is recommended to leave as default. Defaults to defaults.HEADER.

        Returns:
            List[Dict[str, Any]]: Similar
        """

        url = "https://www.realtor.com/api/v1/hulk"

        querystring = {"client_id": "rdc-x", "schema": "vesta"}

        payload = {
            "query": None,
            "propertyId": property_id,
            "callfrom": "LDP",
            "nrQueryType": "SIMILAR_HOMES",
            "ab_test_variation": None,
            "variables": {
                "propertyId": property_id,
                "relatedHomesQuery": {"type": "similar_homes"}
            },
            "isClient": True,
            "queryLoader": {
                "appType": "FOR_SALE",
                "pageType": "LDP",
                "serviceType": "SIMILAR_HOMES"
            },
            "isBot": "false"
        }

        response = requests.request(
            "POST", url, json=payload, headers=headers, params=querystring)
        return response.json()['data']['home']['related_homes']

    @staticmethod
    def get_homes_in_area_with_price(
        zip_code: str, price_min: int, price_max: int, limit: int = 15, offset: int = 0, headers: Dict = defaults.HEADER
    ) -> Dict[str, Any]:
        """Gets homes in a zip code that have a price within the specified range.

        Args:
            zip_code (str): The zip code to find homes in
            price_min (int): The minimum price
            price_max (int): The maximum price
            limit (int, optional): The limit of the number of results. Defaults to 15 (Realtor.com default)
            offset (int, optional): The offset on the results. If offset is 2, the first result will be the 3rd result. Defaults to 0.
            headers (Dict, optional): The request headers. Incorrect headers may lead to invalid results. It is recommended to leave as default. Defaults to defaults.HEADER.

        Returns:
            Dict[str, Any]: The homes in the zip code with price in range
        """

        url = "https://www.realtor.com/api/v1/hulk"

        querystring = {"client_id": "rdc-x", "schema": "vesta"}

        payload = {
            "callfrom": "LDP",
            "nrQueryType": "HOMES_AROUND_VALUE",
            "query": None,
            "queryLoader": {
                "appType": "FOR_SALE",
                "pageType": "LDP",
                "serviceType": "HOMES_AROUND_VALUE"
            },
            "variables": {
                "query": {
                    "primary": True,
                    "status": ["for_sale", "ready_to_build"],
                    "postal_code": zip_code,
                    "list_price": {
                        "min": price_min,
                        "max": price_max
                    }
                },
                "limit": limit,
                "offset": offset,
                "sort": {
                    "field": "list_date",
                    "direction": "desc"
                }
            }
        }

        response = requests.request(
            "POST", url, json=payload, headers=headers, params=querystring)
        return response.json()['data']['home_search']
