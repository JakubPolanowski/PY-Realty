import json
import requests
from typing import Dict
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

    def set_filter(self):
        return self  # TODO

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
