# This handles parsing of sale data
from typing import Dict, Any, List
from numbers import Number
from .details_page import Preload_Detail_Page


class Sale(Preload_Detail_Page):
    """This class extracts the properties/details of a property Sale from Zillow's detail URL page. 

    While most of the key details can be easily access via the class attributes or functions, there are some more advanced details that not parsed/organized by this class. For the full html page, see the soup attribute. Additionally check the variant_cache and the full_cache for the complete dictionaries of the api cache. 

    Attributes:
        url (str): The detail URL that this class has parsed
        soup (BeautifulSoup): The html content of this page parsed to a soup object
        preload (Dict[Any, Any]): The complete api cache preload

        zpid (int): The Zillow property ID

        variant_cache (Dict[Any, Any]): The variant api cache
        full_cache (Dict[Any, Any]): The full api cache

        property (Dict[Any, Any]): The property data dictionary

        status (str) : The home status, for example: FOR_SALE or FOR_RENT
        home_type (str): The home type
        year_built (int): Year home was built
        parcel_number (str): The parcel number

        price (int): The home price
        zestimate (int): Zillow's estimated home value
        rental_zestimate (int): Zillow's estimated monthly rental value
        tax_history (List[Dict[str, Number]]): The tax history of the property
        price_history (List[Dict[str, Any]]): The price history of the property
        currency (str): The currency the price, zestimate, etc. are in

        status (str): The status of the listing. For example - for sale.
        days_on_zillow (int): The number of days on Zillow
        views (int): The number of views on Zillow
        saves (int): The number of saves/favorites on Zillow

        tags (List[str]): The tags on the property. For example - "Rolling Hills".
        description (str): The property description

        address (Dict[str, Any]): Dictionary of data related to the address of the property
        street_address (str): The street address
        city (str): City
        state (str): State
        zip (str): zip code
        latitude (float): The latitude
        longitude (float): The longitude

        bedrooms (Number): The number of bedrooms
        bathrooms (Number): The number of bathrooms

        interior_sqft (Number): The SQFT area of the interior of the property

        appliances (List[str]): The list of appliances that are included with the property
        cooling (List[str]): The list of cooling related features 
        heating (List[str]): The list of heating related features
        community_features (List[str]): The list of community features
        fireplaces (Number): The number of fireplaces. Note: this can often be incorrect or misleading
        garage (bool): True if has garage, False if doesn't
        interior_features (List[str]): List of interior features

        attic (str | None): None if has no attic, otherwise will have a string specification of attic type
        basement (str): Specification of basement type

        hoa_fee (Number | None): If has a hoa fee, will be the monthly fee as a number. If not, then will be None

        levels (str): The number of levels given as a string

        parking (List[str]): The parking features, for example ["OFF_STREET"]
        lot_features (List[str] | None): List of lot features, if there are none, will be None
        lot_size (str): Lot size as as a string with units
        lot_size_dimensions (str): Dimensions of the lot as a string
        lot_sqft (Number): The SQFT area of the lot

        sewer (List[str]): The list of sewer systems. Typically this will just be a list of one element.
        water_source (List[str]): The list of water sources. Typically this will just be a list of one element.

        attribution (Dict[str, Any]): The attribution details of the listing agent/agency

        schools (List[Dict[str, Any]]): The nearby schools
        similar (List[Dict[str, Any]]): Similar properties
        nearby (List[Dict[str, Any]]): Nearby properties
    """

    def __init__(self, url: str) -> None:
        """This initializes the sale object, which call a GET request on the Zillow detail URL. 

        Args:
            url (str): The Zillow Property Sale details URL.
        """

        super().__init__(url)
        self.parcel_number: str = self.property['resoFacts']['parcelNumber']

    def get_likely_to_sell(self) -> str | None:
        """Gets the Zillow likely to sell estimation.

        Returns:
            str | None: Zillow likely to sell estimation. Returns None if there is none
        """
        tag = self.soup.find("p", "kHeRng")

        if not tag:
            return tag
        else:
            return tag.text.replace(u'\u200a', '')

    @staticmethod
    def calculate_monthly_mortgage(principal: Number, interest: Number, months: Number) -> Number:
        """Calculates the monthly mortgage payment. Formula from https://www.bankrate.com/mortgages/mortgage-calculator/#how-mortgage-calculator-help

        Args:
            principal (Number): The principal for the mortgage (in this case home price minus the down payment)
            interest (Number): The interest rate as a monthly percentage (5% -> (5/100)/12)
            months (Number): Number of months on the mortagage

        Returns:
            Number: The monthly mortgage payment
        """
        return principal * (interest * (1+interest)**months) / ((1+interest)**months-1)

    def get_monthly_estimated_cost(self, down: Number, interest: Number = None, months: Number = 30*12, tax: Number = None, home_insurance: Number = None, mortgage_insurance: Number = 0, hoa_fee: Number = None, utilies: Number = 0) -> Number:
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
        if not interest:
            interest = self.property['mortgageRates']['thirtyYearFixedRate']
            if interest:  # check if had actual value
                interest /= 100  # zillow gives as a percentage so need to divide by 100
            else:
                interest = 0.06  # just some value to fall back on

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
