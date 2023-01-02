import requests
from typing import List, Literal, Set
from . import defaults


class Query:

    def __init__(self) -> None:

        self.state: str | None = None
        self.region: str | None = None
        self.county: str | None = None
        self.city: str | None = None

        self.price_max: int | None = None
        self.price_min: int | None = None

        self.size_max: int | None = None
        self.size_min: int | None = None

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

        self.activity: str | None = None

        self.available = True
        self.under_contract = False
        self.off_market = False
        self.sold = False

        self.sale_type: Literal['sale', 'auction', 'both'] = 'sale'

        self.owner_financing = False
        self.mineral_rights = False
        self.virtual_tour = False

        self.keywords: List[str] = []

    def create_url(self):

        url = defaults.ROOT_URL

        if self.state is None and self.property_type is None:
            url += "/land"

        if self.state is not None:
            url += self.get_link_for_state(self.state)

        if self.city is not None:
            url += self.get_link_for_city(self.city)
        elif self.county is not None:
            url += self.get_link_for_county(self.county)
        elif self.region is not None:
            url += self.get_link_for_region(self.region)

        if self.property_type is not None:
            url += self.get_link_for_property(self.property_type)

        # TODO remainder of filters

    @staticmethod
    def get_link_for_state(state: str) -> str:

        raise NotImplemented  # TODO

    @staticmethod
    def get_link_for_property(propety: Set[str] | str) -> str:

        raise NotImplemented  # TODO

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
    def get_link_for_size(size_min: int | None = None, size_max: int | None = None) -> str:
        """Gets the link for the lot size filter

        Args:
            size_min (int | None, optional): Size min in Acres. Defaults to None.
            size_max (int | None, optional): Size mac in acres. Defaults to None.

        Returns:
            str: The link for the size filter
        """
        if size_max is not None and size_min is not None:
            return f'/acres-{size_min}-{size_max}'
        elif size_max is not None:
            return f'/acres-under-{size_max}'
        elif size_min is not None:
            return f'/acres-over-{size_min}'
        else:
            return ''

    @staticmethod
    def get_link_for_beds(beds_min: int | None = None, beds_max: int | None = None) -> str:
        ...  # TODO

    @staticmethod
    def get_link_for_baths(baths_min: int | None = None, baths_max: int | None = None) -> str:
        ...  # TODO

    @staticmethod
    def get_link_for_activity(activity: str) -> str:
        ...  # TODO

    @staticmethod
    def get_link_for_sale_type(sale_type: str) -> str:
        ...  # TODO

    @staticmethod
    def get_link_for_keywords(keywords: List[str]) -> str:
        ...  # TODO
