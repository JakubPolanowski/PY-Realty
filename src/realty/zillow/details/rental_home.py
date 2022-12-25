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
        self.year_built: int | None = self.property['yearBuilt']
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

        self.tags: List[str] = self.get_tags()  # TODO CHECK
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
        self.basement: str | None = self.property['basement']

        self.hoa_fee: Number | None = self.property['hoaFee']

        self.levels: str | None = self.property['levels']

        self.lot_features: List[str] | None = self.property['lotFeatures']
        self.lot_size: str | None = self.property['lotSize']
        self.lot_size_dimensions: str = self.property['lotSizeDimensions']
        self.lot_sqft: Number = self.parse_lot_size(self.lot_size)

        self.sewer: List[str] | None = self.property['sewer']
        self.water_source: List[str] | None = self.property['waterSource']

        self.attribution: Dict[str, Any] = self.property['attributionInfo']

        self.schools: List[Dict[str, Any]] = self.property['schools']
        self.similar: List[Dict[str, Any]] = self.property['comps']
        self.nearby: List[Dict[str, Any]] = self.property['nearbyHomes']
