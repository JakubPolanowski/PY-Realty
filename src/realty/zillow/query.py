import json
import requests
from typing import Dict, Any, List, Literal, Union, Set
from . import defaults


class Query:

    def __init__(self):
        """Initializes defaults. Note that defaults are based on assumptions of how the Zillow API works, and are not necessarily optimal. 
        """

        # TODO further experiment to reduce unnecessary params

        self.sub_parms = {
            "pagination": {"currentPage": 1},
            "isMapVisible": "true",
            "isListVisible": "true",
            "mapZoom": 11,
        }

        self.wants = {
            "cat1": ["listResults", "mapResults"],
            "cat2": ["total"]
        }

    def set_page(self, current_page: int) -> 'Query':
        """Sets current page of paginated search results

        Args:
            current_page (int): Page of results to lookup

        Returns:
            Query: Returns self
        """
        self.sub_parms["pagination"] = {"currentPage": current_page}

    def set_search_term(self, term: str) -> 'Query':
        """Sets the query search term.

        Args:
            term (str): The search term for the query

        Returns:
            Query: Returns self
        """

        self.sub_parms["usersSearchTerm"] = term
        return self

    def set_map_bounds(self, west: float, east: float, south: float, north: float) -> 'Query':
        """Sets the map bounds for the query

        Args:
            west (float): West bound, longitude
            east (float): East bound, longitude
            south (float): South bound, latitude
            north (float): North bound, latitude 

        Returns:
            Query: Returns self
        """
        self.sub_parms["mapBounds"] = {
            "west": -85.58309022900734,
            "east": -85.18483583447609,
            "south": 34.73748469750508,
            "north": 35.40678434232889,
        }
        return self

    def set_region(self, region_id: int, region_type: int) -> 'Query':
        """Sets the region. Note that the region ID and Type appear to be internal to Zillow, therefore this is a difficult query param to use

        Args:
            region_id (int): Zillow Region ID value
            region_type (int): Zillow Region Type value

        Returns:
            Query: Returns self
        """
        self.sub_parms["regionSelection"] = [
            {"regionId": region_id, "regionType": region_type}]
        return self

    def set_map_visable(self, map_visible: bool) -> 'Query':
        # TODO determine what impact this has
        self.sub_parms["isMapVisible"] = map_visible
        return self

    def set_filter(self, filter_dict: Dict[str, Any]) -> 'Query':
        """Sets the filter state. This works by expanding the filter_dict from {key: value} to {key: {'value': value}} which is the format that the API accepts.

        Args:
            filter_dict (Dict[str, Any]): Filter parameters given as a dictionary of keys and values

        Returns:
            Query: Returns self
        """

        self.sub_parms["filterState"] = {
            k: {"value": v} for k, v in filter_dict.items()}
        return self

    def set_filter_preset(
            self,
            for_sale: bool = True,
            all_homes: bool = True,
            sale_options: Set[Literal[
                "ForSaleByAgent",
                "ForSaleByOwner",
                "NewConstruction",
                "ComingSoon",
                "Auction",
                "ForSaleForeclosure",
                "RecentlySold"
            ]] = {"ForSaleByAgent", "ForSaleByOwner", "NewConstruction", "ComingSoon", "Auction", "ForSaleForeclosure"},
            solid_in_last_x_days: Union[None, int] = None,
            price_max: Union[None, int] = None,
            price_min: Union[None, int] = None,
            monthly_payment_max: Union[None, int] = None,
            monthly_payment_min: Union[None, int] = None,
            beds: Union[None, int] = None,
            baths: Union[None, int] = None,
            home_type: Set[Literal[
                "SingleFamily",
                "Townhouse",
                "MultiFamily",
                "Condo",
                "LotLand",
                "Apartment",
                "Manufactured",
                "ApartmentOrCondo",
            ]] = {"SingleFamily", "Townhouse", "MultiFamily", "Condo", "LotLand", "Apartment", "Manufactured", "ApartmentOrCondo"},
            hoa: Union[None, int] = None,
            parking_spots: Union[None, int] = None,
            features: Set[Literal[
                "Garage",
                "BasementFinished",
                "BasementUnfinished",
                "SingleStory",
                "AgeRestricted55Plus",
                "AirConditioning",
                "Pool",
                "Waterfront",
                "CityView",
                "ParkView",
                "MountainView",
                "WaterView",
            ]] = set(),
            house_sqft_max: Union[None, int] = None,
            house_sqft_min: Union[None, int] = None,
            lot_sqft_max: Union[None, int] = None,
            lot_sqft_min: Union[None, int] = None,
            year_built_start: Union[None, int] = None,
            year_built_end: Union[None, int] = None,
            keywords: Set[str] = set(),
    ):

        # TODO refactor export logic to helpers and constants

        filter_state = {"isAllHomes": all_homes}

        if for_sale:

            possible_sale_options = {"ForSaleByAgent", "ForSaleByOwner", "NewConstruction",
                                     "ComingSoon", "Auction", "ForSaleForeclosure", "RecentlySold"}

            diff = possible_sale_options - set(sale_options)
            for opt in diff:
                filter_state[f"is{opt}"] = {"value": False}

            if solid_in_last_x_days:
                filter_state["doz"] = {"value": str(solid_in_last_x_days)}

        else:
            filter_state["isForRent"] = True
            filter_state["isForSaleByAgent"] = {"value": False}
            filter_state["isForSaleByOwner"] = {"value": False}
            filter_state["isNewConstruction"] = {"value": False}
            filter_state["isComingSoon"] = {"value": False}
            filter_state["isAuction"] = {"value": False}
            filter_state["isForSaleForeclosure"] = {"value": False}

        if price_max or price_min:
            price = {}
            if price_max:
                price["max"] = price_max
            if price_min:
                price["min"] = price_min

            filter_state["price"] = price

        if monthly_payment_max or monthly_payment_min:
            monthly = {}
            if monthly_payment_max:
                monthly["max"] = monthly_payment_max
            if monthly_payment_min:
                monthly["min"] = monthly_payment_min

            filter_state["monthlyPayment"] = monthly

        if beds:
            filter_state["beds"] = {"min": beds}

        if baths:
            filter_state["baths"] = {"min": baths}

        if home_type:
            possible_home_types = {"SingleFamily", "Townhouse", "MultiFamily",
                                   "Condo", "LotLand", "Apartment", "Manufactured", "ApartmentOrCondo"}

            diff = possible_home_types - set(home_type)
            for opt in diff:
                filter_state[f"is{opt}"] = {"value": False}

        if hoa:
            filter_state["hoa"] = {"max": hoa}

        if parking_spots:
            filter_state["parkingSpots"] = {"min": parking_spots}

        if features:
            feature_dict = {
                "Garage": "hasGarage",
                "BasementFinished": "isBasementFinished",
                "BasementUnfinished": "isBasementUnfinished",
                "SingleStory": "singleStory",
                "AgeRestricted55Plus": "ageRestricted55Plus",
                "AirConditioning": "hasAirConditioning",
                "Pool": "hasPool",
                "Waterfront": "isWaterfront",
                "CityView": "isCityView",
                "ParkView": "isParkView",
                "MountainView": "isMountainView",
                "WaterView": "isWaterView",
            }

            for f in features:
                if f_key := feature_dict.get(f, None):
                    filter_state[f_key] = {"value": True}

        if house_sqft_max or house_sqft_min:
            house_sqft = {}
            if house_sqft_max:
                house_sqft["max"] = house_sqft_max
            if house_sqft_min:
                house_sqft["min"] = house_sqft_min

            filter_state["sqft"] = house_sqft

        if lot_sqft_max or lot_sqft_min:
            lot_sqft = {}
            if lot_sqft_max:
                lot_sqft["max"] = lot_sqft_max
            if lot_sqft_min:
                lot_sqft["min"] = lot_sqft_min

            filter_state["lotSize"] = lot_sqft

        if year_built_start or year_built_end:
            year_range = {}
            if year_built_start:
                year_range["min"] = year_built_start
            if year_built_end:
                year_range["max"] = year_built_end

            filter_state["built"] = year_range

        if keywords:
            filter_state["keywords"] = {
                "value": f"{' ,'.join(keywords)}"
            }

        self.sub_parms["filterState"] = filter_state

        return self

    def set_list_visable(self, list_visible: bool) -> 'Query':
        # TODO determine what impact this has
        self.sub_parms["isListVisible"] = list_visible
        return self

    def set_map_zoom(self, zoom: int) -> 'Query':
        # TODO determine what impact this has
        self.sub_parms["mapZoom"] = zoom
        return self

    def set_wants(self, wants: dict) -> 'Query':
        # TODO make this more user friendly and determine the effect of wants
        self.wants = wants
        return self

    def get_params_string(self) -> str:
        """Generates the parameters JSON string according to the values set within the query

        Returns:
            str: The parameters JSON string
        """
        return {
            "searchQueryState": json.dumps(self.sub_parms),
            "wants": json.dumps(self.wants)
        }

    def get_response(self, url: str = defaults.URL, headers: Dict = defaults.HEADER):
        """Returns the requests response object for the query with the configured params

        Args:
            url (str, optional): The Zillow URL for the API request. The default can be found within defaults.py within the Zillow module
            headers (Dict, optional): The headers parameters as a dictionary. The Defaults can be found within defaults.py within the Zillow module.

        Returns:
            _type_: _description_
        """
        return requests.request(
            "GET",
            url,
            headers=headers,
            params=self.get_params_string()
        )
