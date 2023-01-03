import requests
from typing import List, Literal, Set, Dict, Any
from . import defaults
import re


class Query:

    def __init__(self) -> None:

        self.page: int = 1

        self.state: str | None = None
        self.region: str | None = None
        self.county: str | None = None
        self.city: str | None = None

        self.price_max: int | None = None
        self.price_min: int | None = None

        self.acres_max: int | None = None
        self.acres_min: int | None = None

        self.sqft_max: int | None = None
        self.sqft_min: int | None = None

        self.property_type: Set[Literal[
            "Commerical",
            "Farms and Ranches",
            "Homesite",
            "Horse",
            "House",
            "Hunting",
            "Lakefront",
            "Oceanfront",
            "Recreational",
            "Riverfront",
            "Timberland",
            "Undeveloped",
            "Waterfront",
        ]] | Literal[
            "Commerical",
            "Farms and Ranches",
            "Homesite",
            "Horse",
            "House",
            "Hunting",
            "Lakefront",
            "Oceanfront",
            "Recreational",
            "Riverfront",
            "Timberland",
            "Undeveloped",
            "Waterfront",
        ] | None = None

        self.beds_max: int | None = None
        self.beds_min: int | None = None

        self.baths_max: int | None = None
        self.baths_min: int | None = None

        self.activity: Literal[
            "boating",
            "fishing",
            "beach",
            "horseback riding",
            "rving",
            "canoeing/kayaking",
            "off-roading",
            "camping",
            "conservation",
            "aviation",
        ] | None = None

        self.available = True
        self.under_contract = False
        self.off_market = False
        self.sold = False

        self.sale_type: Literal['sale', 'auction', 'both'] = 'sale'

        self.owner_financing = False
        self.mineral_rights = False
        self.virtual_tour = False

        self.keywords: List[str] = []

    def create_url(self) -> str:
        """Creates the Landwatch GET request URL based on the query attributes

        Returns:
            str: The Landwatch GET request URL
        """

        url = defaults.ROOT_URL

        if self.state is None and self.property_type is None:
            url += "/land"

        if self.state is not None:
            url += Query_Helpers.get_link_for_state(self.state)

            if self.city is not None:
                url += Query_Helpers.get_link_for_city(self.city)
            elif self.county is not None:
                url += Query_Helpers.get_link_for_county(self.county)
            elif self.region is not None:
                url += Query_Helpers.get_link_for_region(self.region)

        if self.property_type is not None:
            url += Query_Helpers.get_link_for_property(self.property_type)

        if self.activity is not None:
            url += Query_Helpers.get_link_for_activity(self.activity)

        if self.price_min is not None or self.price_max is not None:
            url += Query_Helpers.get_link_for_price(
                self.price_min, self.price_max)

        if self.acres_min is not None or self.acres_max is not None:
            url += Query_Helpers.get_link_for_acres(
                self.acres_min, self.acres_max)

        if self.sqft_min is not None or self.sqft_max is not None:
            url += Query_Helpers.get_link_for_sqft(
                self.sqft_min, self.sqft_max)

        if self.beds_min is not None or self.beds_max is not None:
            url += Query_Helpers.get_link_for_beds(
                self.beds_min, self.beds_max)

        if self.baths_min is not None or self.baths_max is not None:
            url += Query_Helpers.get_link_for_baths(
                self.baths_min, self.baths_max)

        if self.keywords:
            url += Query_Helpers.get_link_for_keywords(self.keywords)

        if self.available:
            url += '/available'

        if self.under_contract:
            url += '/under-contract'

        if self.off_market:
            url += '/under-contract'

        if self.sold:
            url += '/sold'

        url += Query_Helpers.get_link_for_sale_type(self.sale_type)

        if self.mineral_rights:
            url += '/mineral-rights'

        if self.owner_financing:
            url += '/owner-financing'

        if self.virtual_tour:
            url += '/virtual-tour'

        if self.page > 1:
            url += f'/page-{self.page}'

        return url

    def set_page(self, page: int) -> 'Query':
        """Sets the page of the results

        Args:
            page (int): Page, must be 1 or greater

        Raises:
            ValueError: Page value less than 1

        Returns:
            Query: Returns self
        """

        if page < 1:
            raise ValueError(f'page must be 1 or greater, was {page}')

        self.page = page
        return self

    def set_state(self, state: str) -> 'Query':
        """Sets the state for the filter.

        Args:
            state (str): The state name

        Raises:
            ValueError: Invalid state name

        Returns:
            Query: Returns self
        """

        if state.lower() in Query_Helpers.state_dict:
            self.state = state
            return self
        else:
            raise ValueError(
                f'Invalid state name "{state}", valid names are {", ".join(Query_Helpers.state_dict.keys())}')

    def set_region(self, region: str) -> 'Query':
        """Sets the region for the filter. Note for this to work, must have a state specified and the region must be valid for said state

        Args:
            region (str): Region name

        Returns:
            Query: Returns self
        """

        self.region = region
        return self

    def set_county(self, county: str) -> 'Query':
        """Sets the county for the filter. Note for this to work, must have state specified and the county name must be valid for said state

        Args:
            county (str): County name

        Returns:
            Query: Returns self
        """

        self.county = county
        return self

    def set_city(self, city: str) -> 'Query':
        """Sets the city for the filter. Note for this to work, must have state specified and the city name must be valid for said state

        Args:
            city (str): City name

        Returns:
            Query: Returns self
        """

        self.city = city
        return self

    def set_price(self, price_min: int | None = None, price_max: int | None = None) -> 'Query':
        """Sets the price range for the filter

        Args:
            price_min (int | None, optional): Price min. If not specified, this end of the range will be left open. Defaults to None.
            price_max (int | None, optional): Price max. If not specified, this end of the range will be left open. Defaults to None.

        Returns:
            Query: Returns self
        """

        self.price_max = price_max
        self.price_min = price_min
        return self

    def set_acres(self, acres_min: int | None = None, acres_max: int | None = None) -> 'Query':
        """Sets the acres (lot area) for the filter

        Args:
            acres_min (int | None, optional): Acres min. If not specified, this end of the range will be left open. Defaults to None.
            acres_max (int | None, optional): Acres max. If not specified, this end of the range will be left open. Defaults to None.

        Returns:
            Query: Returns self
        """

        self.acres_max = acres_max
        self.acres_min = acres_min
        return self

    def set_sqft(self, sqft_min: int | None = None, sqft_max: int | None = None) -> 'Query':
        """Sets the sqft (interior area) for the filter

        Args:
            sqft_min (int | None, optional): Sqft min. If not specified, this end of the range will be left open. Defaults to None.
            sqft_max (int | None, optional): Sqft max. If not specified, this end of the range will be left open. Defaults to None.

        Returns:
            Query: Returns self
        """

        self.sqft_max = sqft_max
        self.sqft_min = sqft_min
        return self

    def set_property_type(self, property_type: Set[Literal[
            "Commerical",
            "Farms and Ranches",
            "Homesite",
            "Horse",
            "House",
            "Hunting",
            "Lakefront",
            "Oceanfront",
            "Recreational",
            "Riverfront",
            "Timberland",
            "Undeveloped",
            "Waterfront",
        ]] | Literal[
            "Commerical",
            "Farms and Ranches",
            "Homesite",
            "Horse",
            "House",
            "Hunting",
            "Lakefront",
            "Oceanfront",
            "Recreational",
            "Riverfront",
            "Timberland",
            "Undeveloped",
            "Waterfront",
    ]) -> 'Query':
        """Sets the property_type for the filter

        Args:
            property_type (Set[Literal[ &quot;Commerical&quot;, &quot;Farms and Ranches&quot;, &quot;Homesite&quot;, &quot;Horse&quot;, &quot;House&quot;, &quot;Hunting&quot;, &quot;Lakefront&quot;, &quot;Oceanfront&quot;, &quot;Recreational&quot;, &quot;Riverfront&quot;, &quot;Timberland&quot;, &quot;Undeveloped&quot;, &quot;Waterfront&quot;, ]] | Literal[ &quot;Commerical&quot;, &quot;Farms and Ranches&quot;, &quot;Homesite&quot;, &quot;Horse&quot;, &quot;House&quot;, &quot;Hunting&quot;, &quot;Lakefront&quot;, &quot;Oceanfront&quot;, &quot;Recreational&quot;, &quot;Riverfront&quot;, &quot;Timberland&quot;, &quot;Undeveloped&quot;, &quot;Waterfront&quot;, ]): The property type(s) either a single type given as a string or a set given as a set of strings.

        Raises:
            ValueError: Invalid property_type
            TypeError: Invalid property_type type given

        Returns:
            Query: Returns self
        """

        if isinstance(property_type, str):
            if property_type not in Query_Helpers.property_type_dict:
                raise ValueError(
                    f'Invalid property_type "{property_type}", valid property types are {", ".join(Query_Helpers.property_type_dict.keys())}')

            self.property_type = property_type
            return self

        elif isinstance(property_type, set):
            diff = property_type - set(Query_Helpers.property_type_dict.keys())
            if diff != set():
                raise ValueError(
                    f'Invalid property_types {", ".join(diff)}, valid property types are {", ".join(Query_Helpers.property_type_dict.keys())}'
                )

            self.property_type = property_type
            return self

        else:
            raise TypeError(
                f'property_type should either be a str or a Set[str], was {type(property_type)}')

    def set_beds(self, beds_min: int | None = None, beds_max: int | None = None) -> 'Query':
        """Sets the beds range for the filter

        Args:
            beds_min (int | None, optional): Beds min. If not specified, this end of the range will be left open. Defaults to None.
            beds_max (int | None, optional): Beds max. If not specified, this end of the range will be left open. Defaults to None.

        Returns:
            Query: Returns self
        """

        self.beds_max = beds_max
        self.beds_min = beds_min
        return self

    def set_baths(self, baths_min: int | None = None, baths_max: int | None = None) -> 'Query':
        """Sets the baths range for the filter

        Args:
            baths_min (int | None, optional): Baths min. If not specified, this end of the range will be left open. Defaults to None.
            baths_max (int | None, optional): Baths max. If not specified, this end of the range will be left open. Defaults to None.

        Returns:
            Query: Returns self
        """

        self.baths_max = baths_max
        self.baths_min = baths_min
        return self

    def set_activity(self, activity: Literal[
        "boating",
        "fishing",
        "beach",
        "horseback riding",
        "rving",
        "canoeing/kayaking",
        "off-roading",
        "camping",
        "conservation",
        "aviation",
    ]) -> 'Query':
        """Sets the activity for the filter

        Args:
            activity (Literal[ &quot;boating&quot;, &quot;fishing&quot;, &quot;beach&quot;, &quot;horseback riding&quot;, &quot;rving&quot;, &quot;canoeing): Activity

        Raises:
            ValueError: Invalid activity

        Returns:
            Query: Returns self
        """

        if activity not in Query_Helpers.activity_dict:
            raise ValueError(
                f'Invalid activity "{activity}", valid activities are {", ".join(Query_Helpers.activity_dict.keys())}')

        self.activity = activity
        return self

    def set_status(self, available=True, under_contract=False, off_market=False, sold=False) -> 'Query':
        """Sets the status of the property filter

        Args:
            available (bool, optional): If available. Defaults to True.
            under_contract (bool, optional): If under contract. Defaults to False.
            off_market (bool, optional): If off market. Defaults to False.
            sold (bool, optional): If sold. Defaults to False.

        Returns:
            Query: Returns self
        """

        self.available = available
        self.under_contract = under_contract
        self.off_market = off_market
        self.sold = sold
        return self

    def set_sale_type(self, sale_type: Literal['sale', 'auction', 'both']) -> 'Query':
        """Sets the sale type for the filter

        Args:
            sale_type (Literal[&#39;sale&#39;, &#39;auction&#39;, &#39;both&#39;]): The sale type

        Raises:
            ValueError: Invalid sales type

        Returns:
            Query: Returns self
        """

        valid = ['sale', 'auction', 'both']
        if sale_type not in valid:
            raise ValueError(
                f'Invalid sale type "{sale_type}", valid types are {", ".join(valid)}')

        self.sale_type = sale_type
        return self

    def set_owner_financing(self, owner_financing: bool) -> 'Query':
        """Sets if the owner is financing for the filter

        Args:
            owner_financing (bool): Owner financing

        Returns:
            Query: Returns self
        """

        self.owner_financing = owner_financing
        return self

    def set_mineral_rights(self, mineral_rights: bool) -> 'Query':
        """Sets if mineral rights are part of the property for the filter

        Args:
            mineral_rights (bool): Mineral rights

        Returns:
            Query: Returns self
        """

        self.mineral_rights = mineral_rights
        return self

    def set_virtual_tour(self, virtual_tour: bool) -> 'Query':
        """Sets if there is a virtual tour for the property for the filter

        Args:
            virtual_tour (bool): Virtual tour

        Returns:
            Query: Returns self
        """

        self.virtual_tour = virtual_tour
        return self

    def set_keywords(self, keywords: List[str]) -> 'Query':
        """Sets the keywords for the filter

        Args:
            keywords (List[str]): List of keywords. These must be alphanumeric with no spaces.

        Raises:
            ValueError: Invalid format for keyword

        Returns:
            Query: Returns self
        """

        for keyword in keywords:
            if not re.match(r'[A-Za-z0-9]+', keyword):
                raise ValueError(
                    f'Keywords must be alphanumeric with no spaces or symbols, keyword "{keyword}" was not')

        self.keywords = keywords

    def set_all(self, **kwargs) -> 'Query':
        """Meta setter function that can set all attributes

        Returns:
            Query: Returns self
        """

        if x := kwargs.get('page'):
            self.set_page(x)

        if x := kwargs.get('state'):
            self.set_state(x)

        if x := kwargs.get('region'):
            self.set_region(x)

        if x := kwargs.get('county'):
            self.set_county(x)

        if x := kwargs.get('city'):
            self.set_city(x)

        self.set_price(kwargs.get('price_min'), kwargs.get('price_max'))
        self.set_acres(kwargs.get('acres_min'), kwargs.get('acres_max'))
        self.set_sqft(kwargs.get('sqft_min'), kwargs.get('sqft_max'))

        if x := kwargs.get('property_type'):
            self.set_property_type(x)

        self.set_beds(kwargs.get('beds_min'), kwargs.get('beds_max'))
        self.set_baths(kwargs.get('baths_min'), kwargs.get('baths_max'))

        if x := kwargs.get('activity'):
            self.set_activity(x)

        self.set_status(
            kwargs.get('available', True),
            kwargs.get('under_contract', False),
            kwargs.get('off_market', False),
            kwargs.get('sold', False)
        )

        if x := kwargs.get('sale_type'):
            self.set_sale_type(x)

        if x := kwargs.get('owner_financing'):
            self.set_owner_financing(x)

        if x := kwargs.get('mineral_rights'):
            self.set_mineral_rights(x)

        if x := kwargs.get('virtual_tour'):
            self.set_virtual_tour(x)

        if x := kwargs.get('keywords'):
            self.set_keywords(x)

        return self

    def get_response(self, headers: Dict = defaults.HEADER) -> requests.Response:
        """Gets the GET request response for the Landwatch API given filter parameters

        Args:
            headers (Dict, optional): The request headers. Incorrect headers may lead to the Landwatch PUBLIC api blocking the request. Defaults to defaults.HEADER.

        Returns:
            requests.Response: GET request response object
        """

        return requests.get(
            self.create_url(),
            headers=headers
        )

    def get_results(self, returns: Literal["full", "results"] = "results", headers: Dict = defaults.HEADER) -> Dict[str, Any]:
        """Gets the results from the GET request to the PUBLIC Landwatch API given filter parameters.

        Args:
            returns (Literal[&quot;full&quot;, &quot;results&quot;], optional): What it should return, either the 'full' json content of the response or 'results' - the part that pertains to the search results. Defaults to "results".
            headers (Dict, optional): The request headers. Incorrect headers may lead to the Landwatch PUBLIC api blocking the request. Defaults to defaults.HEADER.

        Raises:
            ValueError: Invalid returns parameter value

        Returns:
            Dict[str, Any]: The response data
        """

        data = self.get_response(headers).json()

        if returns == 'full':
            return data
        elif returns == 'results':
            return data['searchResults']
        else:
            raise ValueError(
                f'Invalid returns value "{returns}", valid options are "full" and "results"')

    def get_filter_options(self, headers: Dict = defaults.HEADER) -> Dict[str, Any]:
        """Gets the potential filter options, such as possible states (or regions if state was set).

        Args:
            headers (Dict, optional): The request headers. Incorrect headers may lead to the Landwatch PUBLIC api blocking the request. Defaults to defaults.HEADER.

        Returns:
            Dict[str, Any]: Dictionary of filter options
        """

        data = self.get_results('full')
        options = {}
        for fs in data['filterSections']:
            options[fs['section']] = fs['filterLinks']

        return options


class Query_Helpers:

    state_dict = {
        "texas": "/texas-land-for-sale",
        "florida": "/florida-land-for-sale",
        "georgia": "/georgia-land-for-sale",
        "north carolina": "/north-carolina-land-for-sale",
        "california": "/california-land-for-sale",
        "tennessee": "/tennessee-land-for-sale",
        "south carolina": "/south-carolina-land-for-sale",
        "michigan": "/michigan-land-for-sale",
        "arizona": "/arizona-land-for-sale",
        "new york": "/new-york-land-for-sale",
        "arkansas": "/arkansas-land-for-sale",
        "virginia": "/virginia-land-for-sale",
        "kentucky": "/kentucky-land-for-sale",
        "missouri": "/missouri-land-for-sale",
        "oklahoma": "/oklahoma-land-for-sale",
        "pennsylvania": "/pennsylvania-land-for-sale",
        "indiana": "/indiana-land-for-sale",
        "wisconsin": "/wisconsin-land-for-sale",
        "alabama": "/alabama-land-for-sale",
        "ohio": "/ohio-land-for-sale",
        "illinois": "/illinois-land-for-sale",
        "oregon": "/oregon-land-for-sale",
        "mississippi": "/mississippi-land-for-sale",
        "colorado": "/colorado-land-for-sale",
        "idaho": "/idaho-land-for-sale",
        "new mexico": "/new-mexico-land-for-sale",
        "minnesota": "/minnesota-land-for-sale",
        "iowa": "/iowa-land-for-sale",
        "louisiana": "/louisiana-land-for-sale",
        "nevada": "/nevada-land-for-sale",
        "utah": "/utah-land-for-sale",
        "maryland": "/maryland-land-for-sale",
        "montana": "/montana-land-for-sale",
        "new jersey": "/new-jersey-land-for-sale",
        "washington": "/washington-land-for-sale",
        "west virginia": "/west-virginia-land-for-sale",
        "kansas": "/kansas-land-for-sale",
        "maine": "/maine-land-for-sale",
        "connecticut": "/connecticut-land-for-sale",
        "new hampshire": "/new-hampshire-land-for-sale",
        "massachusetts": "/massachusetts-land-for-sale",
        "wyoming": "/wyoming-land-for-sale",
        "south dakota": "/south-dakota-land-for-sale",
        "delaware": "/delaware-land-for-sale",
        "vermont": "/vermont-land-for-sale",
        "hawaii": "/hawaii-land-for-sale",
        "alaska": "/alaska-land-for-sale",
        "nebraska": "/nebraska-land-for-sale",
        "north dakota": "/north-dakota-land-for-sale",
        "rhode island": "/rhode-island-land-for-sale",
        "district of columbia": "/district-of-columbia-land-for-sale",
    }

    activity_dict = {
        "boating": "/boating-activity",
        "fishing": "/fishing-activity",
        "beach": "/beach-activity",
        "horseback riding": "/horseback-riding-activity",
        "rving": "/rving-activity",
        "canoeing/kayaking": "/canoeing-kayaking-activity",
        "off-roading": "/off-roading-activity",
        "camping": "/camping-activity",
        "conservation": "/conservation-activity",
        "aviation": "/aviation-activity",
    }

    property_type_dict = {
        "house": "/homes",
        "undeveloped": "/undeveloped-land",
        "homesite": "/homesites",
        "waterfront": "/waterfront-property",
        "lakefront": "/lakefront-property",
        "commercial": "/commercial-property",
        "recreational": "/recreational-property",
        "farms and ranches": "/farms-ranches",
        "hunting": "/hunting-property",
        "timberland": "/timberland-property",
        "horse": "/horse-property",
        "riverfront": "/riverfront-property",
        "oceanfront": "/oceanfront-property",
    }

    property_type_id_dict = {
        "house": 8192,
        "undeveloped": 32,
        "homesite": 4096,
        "waterfront": 3584,
        "lakefront": 512,
        "commercial": 64,
        "recreational": 4,
        "farms and ranches": 3,
        "hunting": 128,
        "timberland": 16,
        "horse": 256,
        "riverfront": 2048,
        "oceanfront": 1024,
    }

    @classmethod
    def get_link_for_state(cls, state: str) -> str:
        """Gets the relative link for the filtering for the state

        Args:
            state (str): The state name

        Raises:
            ValueError: Invalid state name

        Returns:
            str: relative link
        """

        try:
            return cls.state_dict[state.lower()]
        except KeyError:
            raise ValueError(
                f'{state} is not a valid state name, valid state names are {", ".join(cls.state_dict.keys())}')

    @classmethod
    def get_link_for_property(cls, property_type: Set[str] | str) -> str:
        """Gets the link for the property type filter

        Args:
            property_type (Set[str] | str): Either a single property type as a string or a set of property type strings

        Raises:
            ValueError: Not a valid property type
            TypeError: property_type is neither a str or a set

        Returns:
            str: _description_
        """

        if isinstance(property_type, str):
            try:
                return cls.property_type_dict[property_type.lower()]
            except KeyError:
                raise ValueError(
                    f'{property_type} is not a valid propety type, valid propety types are {", ".join(cls.property_type_dict.keys())}')

        elif isinstance(property_type, set):

            id_sum = 0

            for pt in property_type:
                try:
                    id_sum += cls.property_type_id_dict[pt]
                except KeyError:
                    raise ValueError(
                        f'{pt} is not a valid propety type, valid propety types are {", ".join(cls.property_type_dict.keys())}')

            if id_sum > 0:
                return f'/prop-types-{id_sum}'
            else:
                return ''

        else:
            raise TypeError(
                f'property_type parameter is an invalid type {type(property_type)}. Must be either a str or a Set[str]')

    @staticmethod
    def get_link_for_region(region: str) -> str:
        """Formats the region name as needed by the Landwatch api, all lower case, spaces replaced with -, '-region' added at the end.

        Args:
            region (str): Region name

        Returns:
            str: Region name formatted ('/region-name-region')
        """
        region = region.lower().replace(' ', '-')
        return f'/{region}-region'

    @staticmethod
    def get_link_for_county(county: str) -> str:
        """Formats the county name as needed by the Landwatch api, all lower case, spaces replaced with -, '-county' added at the end.

        Args:
            county (str): County name

        Returns:
            str: County name formatted ('/county-name-county')
        """
        county = county.lower().replace(' ', '-')
        return f'/{county}-county'

    @staticmethod
    def get_link_for_city(city: str) -> str:
        """Formats the city name as needed by the Landwatch api, all lower case, spaces replaced with -

        Args:
            city (str): The city name

        Returns:
            str: City name formatted for landwatch ('/city-name')
        """

        city = city.lower().replace(' ', '-')
        return f'/{city}'

    @staticmethod
    def get_link_for_price(price_min: int | None = None, price_max: int | None = None) -> str:
        """Gets the link for the price filter.

        Args:
            price_min (int | None, optional): Min price in USD. Defaults to None.
            price_max (int | None, optional): Max price in USD. Defaults to None.

        Returns:
            str: the link
        """

        if price_max is not None and price_min is not None:
            return f'/price-{price_min}-{price_max}'
        elif price_max is not None:
            return f'/price-under-{price_max}'
        elif price_min is not None:
            return f'/price-over-{price_min}'
        else:
            return ''

    @staticmethod
    def get_link_for_acres(acres_min: int | None = None, acres_max: int | None = None) -> str:
        """Gets the link for the lot size filter

        Args:
            acres_min (int | None, optional): Lot size area in Acres. Defaults to None.
            acres_max (int | None, optional): Lot size area in acres. Defaults to None.

        Returns:
            str: The link for the size filter
        """
        if acres_max is not None and acres_min is not None:
            return f'/acres-{acres_min}-{acres_max}'
        elif acres_max is not None:
            return f'/acres-under-{acres_max}'
        elif acres_min is not None:
            return f'/acres-over-{acres_min}'
        else:
            return ''

    @staticmethod
    def get_link_for_sqft(sqft_min: int | None = None, sqft_max: int | None = None) -> str:
        """Gets the link for the lot size filter

        Args:
            sqft_min (int | None, optional): Interior area min in sqft. Defaults to None.
            sqft_max (int | None, optional): Interior area max in sqft. Defaults to None.

        Returns:
            str: The link for the size filter
        """
        if sqft_max is not None and sqft_min is not None:
            return f'/sqft-{sqft_min}-{sqft_max}'
        elif sqft_max is not None:
            return f'/sqft-under-{sqft_max}'
        elif sqft_min is not None:
            return f'/sqft-over-{sqft_min}'
        else:
            return ''

    @staticmethod
    def get_link_for_beds(beds_min: int | None = None, beds_max: int | None = None) -> str:
        """Gets the link for the number of beds filter

        Args:
            beds_min (int | None, optional): Min number of beds. Defaults to None.
            beds_max (int | None, optional): Max number of beds. Defaults to None.

        Returns:
            str: The link for the number of beds filter
        """
        if beds_max is not None and beds_min is not None:
            return f'/beds-{beds_min}-{beds_max}'
        elif beds_max is not None:
            return f'/beds-under-{beds_max}'
        elif beds_min is not None:
            return f'/beds-over-{beds_min}'
        else:
            return ''

    @staticmethod
    def get_link_for_baths(baths_min: int | None = None, baths_max: int | None = None) -> str:
        """Gets the link for the number of baths filter

        Args:
            baths_min (int | None, optional): Min number of baths. Defaults to None.
            baths_max (int | None, optional): Max number of baths. Defaults to None.

        Returns:
            str: The link for the number of baths filter
        """
        if baths_max is not None and baths_min is not None:
            return f'/baths-{baths_min}-{baths_max}'
        elif baths_max is not None:
            return f'/baths-under-{baths_max}'
        elif baths_min is not None:
            return f'/baths-over-{baths_min}'
        else:
            return ''

    @classmethod
    def get_link_for_activity(cls, activity: str) -> str:
        """Gets the relative link for filtering based on the specified activity

        Args:
            activity (str): activity

        Raises:
            ValueError: Invalid activity name

        Returns:
            str: relative link
        """
        try:
            return cls.activity_dict[activity.lower()]
        except KeyError:
            raise ValueError(
                f'{activity} is not a valid activity name, valid activity names are {", ".join(cls.activity_dict.keys())}')

    @staticmethod
    def get_link_for_sale_type(sale_type: Literal['sale', 'auction', 'both']) -> str:
        """Gets the link for the specified sale type

        Args:
            sale_type (Literal[&#39;sale&#39;, &#39;auction&#39;, &#39;both&#39;]): The sale type

        Raises:
            ValueError: Invalid sale type given

        Returns:
            str: the link for the specified sale type
        """

        if sale_type == 'both':
            return ''
        elif sale_type == 'sale':
            return '/for-sale'
        elif sale_type == 'auction':
            return '/auctions'
        else:
            raise ValueError('Invalid sale type')

    @staticmethod
    def get_link_for_keywords(keywords: List[str]) -> str:
        """Gets the link for filtering based on specified keywords

        Args:
            keywords (List[str]): Keywords. Note that keywords can only be alphanumeric, no spaces or symbols. Keywords are case insensitive

        Raises:
            ValueError: Invalid keyword format

        Returns:
            str: Keyword filter link
        """

        link = '/keyword'

        for keyword in keywords:
            if re.match(r'[A-Za-z0-9]+', keyword):
                link += f'-{keyword.lower()}'
            else:
                raise ValueError(
                    f'Keywords must be alphanumeric with no spaces or symbols, keyword "{keyword}" was not')

        return link
