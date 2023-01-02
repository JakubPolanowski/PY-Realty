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

        # description
        self.description = self.property_details['description']
        self.location = self.property_details['location']

        # quick access values

        self.property_id: str = self.property_details['property_id']
        self.listing_date: str = self.property_details['listing_date']

        self.status: str = self.property_details['status']
        self.price: int = self.property_details['list_price']
        self.price_per_sqft: int = self.property_details['price_per_sqft']
        self.yearly_property_tax: Number = self.property_details['source']['raw']['tax_amount']
        self.year_built: int = self.description['year_built']
        self.open_houses: Any = self.property_details['open_houses']

        self.listing_description = self.description['text']
        self.details = self.property_details['details']
        self.beds: int = self.description['beds']
        self.baths: int = self.description['baths']
        self.garage: int = self.description['garage']
        self.interior_sqft: int = self.description['sqft']
        self.lot_sqft: int = self.description['lot_sqft']

        self.address = self.location['address']
        self.city = self.address['city']
        self.state_code = self.address['state_code']
        self.state = self.address['state']
        self.county = self.address['county']
        self.latitude = self.address['coordinate']['lat']
        self.longitude = self.address['coordinate']['lon']
        self.zip = self.address['postal_code']
        self.street_address = f"{self.address['line']}, {self.city}, {self.state_code} {self.zip}"
        self.fips: str = self.location['county']['fips_code']

        self.hoa_fee: int = self.property_details['hoa'].get('fee', 0)

        self.property_history = self.property_details['property_history']
        self.tax_history = self.property_details['tax_history']

        self.area_market_status = self.location.get('postal_code', {}).get(
            'geo_statistics', {}).get('housing_market')

        self.noise: str = self.get_noise_metrics(
            self.latitude, self.longitude).get('local_text', 'Unknown')

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
        return response.data()

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
        return response.data()
