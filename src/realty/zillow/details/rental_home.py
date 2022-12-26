# This handles parsing of rental homes data
from typing import Dict, Any, List
from numbers import Number
from .details_page import Preload_Detail_Page


class Rental_Home(Preload_Detail_Page):
    """This class extracts the properties/details of a rental property from Zillow's detail URL page. 

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

        price (int): The monthly rent
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

        fees_and_dues (List[Dict[str, Any]]): Fees/dues associated with property
    """

    def __init__(self, url: str) -> None:
        """This initializes the Rental_Home object, which call a GET request on the Zillow detail URL. 

        Args:
            url (str): The Zillow Rental Property details URL.
        """

        super().__init__(url)

        self.fees_and_dues: List[Dict[str, Any]
                                 ] = self.property['resoFacts']['feesAndDues']
