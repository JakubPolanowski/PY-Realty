import requests
import json
import requests
from typing import Dict, Any, List, Literal, Set
from datetime import datetime
from . import defaults


class Sale_Query:

    def __init__(self) -> None:

        self.set_post_params()
        self.set_json_payload()
        self.set_graphql_query()

    def set_post_params(self, post_parms: Dict[str, Any] = {"client_id": "rdc-x", "schema": "vesta"}) -> 'Sale_Query':
        """Sets the post request parameters, the dictionary that will be passed to the 'param' parameter in the post request call. The exact effect of these is not entirely clear and therefore it is recommended to left as default.

        Args:
            post_parms (Dict[str, Any], optional): The dictionary of post request paramters. Defaults to {"client_id": "rdc-x", "schema": "vesta"}.

        Returns:
            Query: Returns self
        """

        if not post_parms:
            self.post_params = {"client_id": "rdc-x", "schema": "vesta"}
        else:
            self.post_params = post_parms

        return self

    def set_json_payload(self, payload: Dict[str, Any] = defaults.LISTING_SEARCH_PAYLOAD) -> 'Sale_Query':
        """Sets the request payload, this is the body of the request, sent as a POST. Note that this is rather complicated as the Realotr PUBLIC API is not documented therefore it is recommended to use the default. Also when setting the payload, there are two key keys that are missing real values, 'query' (GraphQL query - see set_graphql_query) and 'variables' --> 'query' (fitler criteria - see set_filter_query and set_filter_query_preset)

        Args:
            payload (Dict[str, Any], optional): The POST request JSON payload. Defaults to defaults.LISTING_SEARCH_PAYLOAD.

        Returns:
            Query: Returns self
        """

        self.payload = payload
        return self

    def set_payload_variables(self, **kwargs) -> 'Sale_Query':
        """Sets variable key value pairs inside the POST request payload. This is not recommended to do manually, for advanced use only.

        Returns:
            Query: Returns self
        """

        for key, item in kwargs.items():
            self.payload['variables'][key] = item

        return self

    def remove_payload_variables(self, *args) -> 'Sale_Query':
        """Removes variable keys inside the POST request payload. This is not recommended to do manually (as in using this function), for advanced use only.

        Returns:
            Query: Returns self
        """

        for key in args:
            if key in self.payload['variables']:
                self.payload['variables'].pop(key)

        return self

    def set_var_client_data(self, client_data: Dict[str, Any] = {"device_data": {"device_type": "web"}, "user_data": {}}) -> 'Sale_Query':
        """Sets the 'client_data' var in payload variables. The exact effect of this is not clear, but if this variable is excluded, the response will fail.

        Args:
            client_data (Dict[str, Any]): The client_data dictionary. Defaults to {"device_data": {"device_type": "web"}, "user_data": {}}

        Returns:
            Query: Returns self
        """

        if client_data is None:
            return self.remove_payload_variables('client_data')

        self.payload['variables']['client_data'] = client_data
        return self

    def set_var_limit(self, limit: int = 42) -> 'Sale_Query':
        """Sets the limit variable in payload variables. This is the max number of results that will be returned. Note that if a query has less results than the limit, then the number of results will be less than the limit.

        Args:
            limit (int, optional): The limit. Defaults to 42, which is the realtor.com default.

        Returns:
            Query: Return self
        """

        if limit is None:
            return self.remove_payload_variables('limit')

        self.payload['variables']['limit'] = limit
        return self

    def set_var_offset(self, offset: int = 0) -> 'Sale_Query':
        """Sets the result offset in the payload variables. This is essentially how pagination works in realtor.com, for instance if the limit is 42, page 2 starts on offset=42 (counting from 0).

        Args:
            offset (int, optional): The result offset. Defaults to 0.

        Returns:
            Query: Returns self
        """

        if offset is None:
            return self.remove_payload_variables('offset')

        self.payload['variables']['offset'] = offset
        return self

    def set_var_sort_type(self, sort_type: str | Dict[str, Any]) -> 'Sale_Query':
        """Sets the sort_type in the payload variables. Note that this is mutually exclusive with sort_type. This is an advanced function, for regular usage, use set_var_sort_preset.

        Args:
            sort_type (str | Dict[str, Any]): The sort_type paramter that specifies how the results will be sorted

        Returns:
            Query: Returns self
        """

        if sort_type is None:
            return self.remove_payload_variables('sort_type')

        self.payload['variables']['sort_type'] = sort_type
        return self

    def set_var_sort(self, sort: Dict[str, Any]) -> 'Sale_Query':
        """Sets the sort in payload variables. Note that this is mutually exclusive with sort_type. This function is for advanced usage only, set_var_sort_preset is recommended for regular usage.

        Args:
            sort (Dict[str, Any]): The sort parameter dictionary

        Returns:
            Query: Returns self
        """
        if sort is None:
            return self.remove_payload_variables('sort')

        self.payload['variables']['sort'] = sort
        return self

    def set_var_sort_preset(self, by: Literal["relevant", "price", "listing age", "open house date", "last reduced", "interior sqft", "lot_size"] = "relevant", ascending=False) -> 'Sale_Query':
        """Sets the sorting and therefore the order of the results.

        Args:
            by (Literal[&quot;relevant&quot;, &quot;price&quot;, &quot;listing age&quot;, &quot;open house date&quot;, &quot;last reduced&quot;, &quot;interior sqft&quot;, &quot;lot_size&quot;], optional): The criteria by which to sort. Defaults to "relevant".
            ascending (bool, optional): If results should be sorted in ascending order or (False) descening. Note that this doesn't have an effect on 'relevant'. Defaults to False.

        Returns:
            Query: Returns self
        """

        sort_direction = 'asc' if ascending else 'desc'

        if by == "relevant":
            self.set_var_sort(None)
            return self.set_var_sort_type('relevant')
        elif by == "price":
            self.set_var_sort_type(None)
            return self.set_var_sort(
                {
                    "field": "list_price",
                    "direction": sort_direction,
                }
            )
        elif by == "listing age":
            self.set_var_sort_type(None)
            return self.set_var_sort(
                {
                    "field": "list_date",
                    "direction": sort_direction,
                }
            )
        elif by == "open house date":
            self.set_var_sort_type(None)
            return self.set_var_sort(
                {
                    "field": "open_house_date",
                    "direction": sort_direction,
                }
            )
        elif by == "last reduced":
            self.set_var_sort_type(None)
            return self.set_var_sort(
                {
                    "field": "price_reduced_date",
                    "direction": sort_direction,
                }
            )
        elif by == "interior sqft":
            self.set_var_sort_type(None)
            return self.set_var_sort(
                {
                    "field": "sqft",
                    "direction": sort_direction,
                }
            )
        elif by == "lot_size":
            self.set_var_sort_type(None)
            return self.set_var_sort(
                {
                    "field": "lot_sqft",
                    "direction": sort_direction,
                }
            )
        else:
            raise ValueError("Invalid 'by' value")

    def set_var_zoho_query(self, zoho_query: Dict[str, Any]) -> 'Sale_Query':
        """Sets the zohoQuery in payload variables. The effect of this variable is unclear and is not required. For advanced usage only. This function was only included because this variable is used by realtor.com web, although it is excluded from the defaults in the 'Query' class.

        Args:
            zoho_query (Dict[str, Any]): The zohoQuery

        Returns:
            Query: Returns self
        """
        if zoho_query is None:
            return self.remove_payload_variables('zohoQuery')

        self.payload['variables']['zohoQuery'] = zoho_query
        return self

    def set_var_geo_supported_slug(self, geo_supported_slug: Dict[str, Any]) -> 'Sale_Query':
        """Sets the geoSupportedSlug in payload variables. The effect of this variable is unclear and is not required. For advanced usage only. This function was only included because this variable is used by realtor.com web, although it is excluded from the defaults in the 'Query' class.

        Args:
            geo_supported_slug (Dict[str, Any]): The geoSupportedSlug

        Returns:
            Query: Returns self
        """
        if geo_supported_slug is None:
            return self.remove_payload_variables('geoSupportedSlug')

        self.payload['variables']['geoSupportedSlug'] = geo_supported_slug
        return self

    def set_var_by_prop_type(self, by_prop_type: Dict[str, Any]) -> 'Sale_Query':
        """Sets the by_prop_type in payload variables. The effect of this variable is unclear and is not required. For advanced usage only. This function was only included because this variable is used by realtor.com web, although it is excluded from the defaults in the 'Query' class.

        Args:
            by_prop_type (Dict[str, Any]): The by_prop_type

        Returns:
            Query: Returns self
        """
        if by_prop_type is None:
            return self.remove_payload_variables('by_prop_type')

        self.payload['variables']['by_prop_type'] = by_prop_type
        return self

    def set_graphql_query(self, query: str = defaults.GRAPHQL_LISTING_SEARCH_QUERY) -> 'Sale_Query':
        """Sets the GraphQL query. Note that this is rather complicated as the Realtor PUBLIC API is not documented therefore it is recommended to use the default.

        Args:
            query (str, optional): The GraphQL query for the listings search. Defaults to defaults.GRAPHQL_LISTING_SEARCH_QUERY.

        Returns:
            Query: Returns self
        """

        self.payload['query'] = query
        return self

    def set_filter_query(self, query: Dict[str, Any]) -> 'Sale_Query':
        """Sets the filter query within 'payload' -> 'variables' -> 'query'. This is used to filter which results should be returned by the search. Note that this is a complex function to use as the PUBLIC Realor.com isn't documented therefore using set_filter_query_preset is recommended as it builds a filter query based on simple parameters.

        Args:
            query (Dict[str, Any]): The filter for the listings query

        Returns:
            Query: Returns self
        """

        self.payload['variables']['query'] = query
        return self

    def set_filter_query_preset(  # search loc, cities, and state code mutually exclusive
        self,
        search_location: str = None,
        location_radius: int = None,  # expand by x miles, only if search_location
        # cluster of one or more cities to include
        cities: List[Dict[str, str]] = None,
        state_code: str = None,
        primary: bool = True,
        new_construction: bool = None,
        foreclosure: bool = None,
        senior_community: bool = None,  # 55+ age
        contingent: bool = None,
        has_tour: bool = None,  # virtual toor
        single_story: bool = None,
        multi_story: bool = None,
        open_house_date_min: datetime = None,
        open_house_date_max: datetime = None,
        list_date_min: datetime = None,
        list_date_max: datetime = None,
        price_min: int = None,
        price_max: int = None,
        price_reduce_date_min: datetime = None,
        price_reduce_date_max: datetime = None,
        hoa_fee_min: int = None,
        hoa_fee_max: int = None,
        # if should show properties with incomplete HOA data
        include_incomplete_hoa: bool = True,
        bedrooms_min: int = None,
        bedrooms_max: int = None,
        bathrooms_min: int = None,
        bathrooms_max: int = None,
        interior_sqft_min: int = None,
        interior_sqft_max: int = None,
        lot_sqft_min: int = None,
        lot_sqft_max: int = None,
        year_built_min: int = None,
        year_built_max: int = None,
        min_garages: int = 0,
        has_carport: bool = None,
        has_rv_or_boat_parking: bool = None,
        has_central_air: bool = None,
        has_forced_air: bool = None,
        has_central_heat: bool = None,
        has_basement: bool = None,
        has_hardwood_floors: bool = None,
        has_fireplace: bool = None,
        has_disability_features: bool = None,
        has_dining_room: bool = None,
        has_family_room: bool = None,
        has_den_or_office: bool = None,
        has_swimming_pool: bool = None,
        has_spa_or_hot_tub: bool = None,
        has_horse_facilities: bool = None,
        has_hill_or_mountain_view: bool = None,
        has_ocean_view: bool = None,
        has_lake_view: bool = None,
        has_river_view: bool = None,
        has_golf_course_lot_or_frontage: bool = None,
        has_corner_lot: bool = None,
        is_cul_de_sac: bool = None,
        has_waterfront: bool = None,
        has_community_swimming_pool: bool = None,
        has_community_spa_or_hot_tub: bool = None,
        has_community_golf: bool = None,
        has_community_security_features: bool = None,
        has_community_clubhouse: bool = None,
        has_tennis_court: bool = None,
        has_community_boat_facilities: bool = None,
        status: Set[Literal[
            "for_sale",
            "ready_to_build",
            "sold"

        ]] = {"for_sale"},
        sold_date_min: datetime = None,
        sold_date_max: datetime = None,
        prop_type: Set[Literal[
            "farm",
            "mobile",
            "multi_family",
            "townhomes",
            "duplex_triplex",
            "single_family",
            "condos",
            "condo_townhome_rowhome_coop",
            "condo_townhome",
            "land"
        ]] = None,  # all -> not specified in query
        keywords: List[str] = None,
        tags: List[str] = [],
        exclude_tags: List[str] = []
    ) -> 'Sale_Query':
        """Sets the filter based on the parameters provided.

        Args:
            search_location (str, optional): The location to search, for example "Charolette, NC". Mutally exclusive with with 'cities'. Defaults to None. NOTE: Either search_location or cities must be specified for query to succeed
            location_radius (int, optional): The radius in miles around the search_location to expand the search to. This is in addition to the Realtor.com default scope of the search, so 0 gives the results without any expansion of the search area/circle. Defaults to 0
            cities (List[Dict[str, str]], optional): List of cities to include in the search. This is mutally exclusive with 'search_location'. Cities are to be specified as [{"city": "CITY_NAME", "state_code": "STATE_CODE}]. NOTE: Either cities or search_location must be specified for query to succeed
            state_code (str, optional): The state code to filter result to. Defaults to None
            primary (bool): Unclear what this represents. Realtor.com queries use primary=True. Defaults to True
            new_construction (bool, optional): If new constructions should be included or excluded. Defaults to None
            foreclosure (bool, optional): If foreclosures should be included or excluded. Default to None
            senior_community (bool, optional): If senior_community (55+) properties should be included or excluded. Defaults to None
            contingent (bool, optional): If properties that have a contingent status should be included or excluded. Defaults to None
            has_tour (bool, optional): If properties filter properties on if they have a tour or if they do not. Defaults to None
            single_story (bool, optional): If properties should only be single story. Defaults to None
            multi_story (bool, optional): If properties should only be multi story. Defaults to None
            open
            open_house_date_min (datetime, optional): Filter based on start date range of open houses. Defaults to None
            open_house_date_max (datetime, optional): Filter based on end date range of open houses. Defaults to None
            list_date_min (datetime, optional): Filter based on the minumum (at least as old as) listing date. Defaults to None
            listing_date_max (datetime, optional): Filter absed on the maximum (at most as young as) listing date. Defaults to None
            price_min (int, optional): The minumum price. Defaults to None
            price_max (int, optional): The maximum price. Defaults to None
            hoa_fee_min (int, optional): The minumum hoa fee. Defaults to None
            hoa_fee_max (int, optional): The maximum hoa fee. Defaults to None
            include_incomplete_hoa (bool, optional): If houses with incomplete (ergo likely inaccurate) hoa information should be included or filtered out. Defaults to None
            bedrooms_min (int, optional): The minumum number of bedrooms. Defaults to None
            bedrooms_max (int, optional): The maximum number of bedrooms. Defaults to None
            bathrooms_min (int, optional): The minumum number of bathrooms. Defaults to None
            bathrooms_max (int, optional): The maximum number of bathrooms. Defaults to None
            interior_sqft_min (int, optional): Interior sqft min. Defaults to None
            interior_sqft_max (int, optional): Interior sqft max. Defaults to None
            lot_sqft_min (int, optional): Lot sqft min. Defaults to None
            lot_sqft_max (int, optional): Lot sqft max. Defaults to None
            year_built_min (int, optional): Year built min. Defaults to None
            year_built_max (int, optional): Year built max. Defaults to None
            min_garages (int, optional): The minimum garages/number of cars that can fit in garage. Defaults to None
            has_carport (bool, optional): Defaults to None
            has_rv_or_boat_parking (bool, optional): Defaults to None
            has_central_air (bool, optional): Defaults to None
            has_forced_air (bool, optional): Defaults to None
            has_central_heat (bool, optional): Defaults to None
            has_basement (bool, optional): Defaults to None
            has_hardwood_floors (bool, optional): Defaults to None
            has_fireplace (bool, optional): Defaults to None
            has_disability_features (bool, optional): Defaults to None
            has_dining_room (bool, optional): Defaults to None
            has_family_room (bool, optional): Defaults to None
            has_den_or_office (bool, optional): Defaults to None
            has_swimming_pool (bool, optional): Defaults to None
            has_spa_or_hot_tub (bool, optional): Defaults to None
            has_horse_facilities (bool, optional): Defaults to None
            has_hill_or_mountain_view (bool, optional): Defaults to None
            has_ocean_view (bool, optional): Defaults to None
            has_lake_view (bool, optional): Defaults to None
            has_river_view (bool, optional): Defaults to None
            has_golf_course_lot_or_frontage (bool, optional): Defaults to None
            has_corner_lot (bool, optional): Defaults to None
            is_cul_de_sac (bool, optional): Defaults to None
            has_waterfront (bool, optional): Defaults to None
            has_community_swimming_pool (bool, optional): Defaults to None
            has_community_spa_or_hot_tub (bool, optional): Defaults to None
            has_community_golf (bool, optional): Defaults to None
            has_community_security_features (bool, optional): Defaults to None
            has_community_clubhouse (bool, optional): Defaults to None
            has_tennis_court (bool, optional): Defaults to None
            has_community_boat_facilities (bool, optional): Defaults to None
            status (Set["for_sale" | "ready_to_build" | "sold"]): Filter based on status. Defaults to ('for_sale')
            sold_date_min (datetime, optional): The sold date is min/start of range. Note that this only works if status is 'sold'. Defaults to None
            sold_date_max (datetime, optional): The sold date max/end of range. Note that this only works if status is 'sold'. Defaults to None
            prop_type (Set["farm" | "mobile" | "multi_family" | "townhomes" | "duplex_triplex" | "single_family" | "condos" | "condo_townhome_rowhome_coop" | "condo_townhome" | "land"]): The property types to include. Defaults to None (includes all)
            keywords (List[str]): List of keywords to require properties to have. Defaults to None
            tags (List[str]): List of tags to require properties to have. Defaults to None
            exlcude_tag (List[str]): List of tags require properties to NOT have. Defaults to None

        Returns:
            Sale_Query: Returns self
        """

        query = {}

        if senior_community is True:
            tags.append('senior_community')
        if single_story is True:
            tags.append('single_story')
        if multi_story is True:
            tags.append('two_or_more_stories')
        if min_garages >= 1:
            tags.append(f'garage_{min_garages}_or_more')
        if has_carport is True:
            tags.append('carport')
        if has_rv_or_boat_parking is True:
            tags.append('rv_or_boat_parking')
        if has_central_air is True:
            tags.append('central_air')
        if has_forced_air is True:
            tags.append('forced_air')
        if has_central_heat is True:
            tags.append('central_heat')
        if has_basement is True:
            tags.append('basement')
        if has_hardwood_floors is True:
            tags.append('hardwood_floors')
        if has_fireplace is True:
            tags.append('fireplace')
        if has_disability_features is True:
            tags.append('disability_features')
        if has_dining_room is True:
            tags.append('dining_room')
        if has_family_room is True:
            tags.append('family_room')
        if has_den_or_office is True:
            tags.append('den_or_office')
        if has_swimming_pool is True:
            tags.append('swimming_pool')
        if has_spa_or_hot_tub is True:
            tags.append('spa_or_hot_tub')
        if has_horse_facilities is True:
            tags.append('horse_facilities')
        if has_hill_or_mountain_view is True:
            tags.append('hill_or_mountain_view')
        if has_ocean_view is True:
            tags.append('ocean_view')
        if has_lake_view is True:
            tags.append('lake_view')
        if has_river_view is True:
            tags.append('river_view')
        if has_golf_course_lot_or_frontage is True:
            tags.append('golf_course_lot_or_frontage')
        if has_corner_lot is True:
            tags.append('corner_lot')
        if is_cul_de_sac is True:
            tags.append('cul_de_sac')
        if has_waterfront is True:
            tags.append('waterfront')
        if has_community_swimming_pool is True:
            tags.append('community_swimming_pool')
        if has_community_spa_or_hot_tub is True:
            tags.append('community_spa_or_hot_tub')
        if has_community_golf is True:
            tags.append('community_golf')
        if has_community_security_features is True:
            tags.append('community_security_features')
        if has_community_clubhouse is True:
            tags.append('community_clubhouse')
        if has_tennis_court is True:
            tags.append('tennis_court')
        if has_community_boat_facilities is True:
            tags.append('community_boat_facilities')

        if senior_community is False:
            exclude_tags.append('senior_community')

        if tags:
            query['tags'] = list(set(tags))
        if exclude_tags:
            query[exclude_tags] - list(set(exclude_tags))

        if search_location:
            query['search_location'] = {'location': search_location}

            if location_radius:
                query['search_location']['buffer'] = location_radius

        if cities:
            for city in cities:
                if 'city' not in city:
                    raise KeyError(
                        "city is a required key when specifying cities")
                if 'state_code' not in city:
                    raise KeyError(
                        'state_code is a required key when specifying cities')

            query['locations'] = cities

        if state_code:
            query['state_code'] = state_code

        query['primary'] = primary

        if new_construction is not None:
            query['new_construction'] = new_construction

        if foreclosure is not None:
            query['foreclosure'] = foreclosure

        if contingent is not None:
            query['contingent'] = contingent

        if has_tour is not None:
            query['has_tour'] = has_tour

        if open_house_date_min or open_house_date_max:
            query['open_house'] = {}
            if open_house_date_min:
                query['open_house']['min'] = open_house_date_min.strftime(
                    "%Y-%m-%d")
            if open_house_date_max:
                query['open_house']['max'] = open_house_date_max.strftime(
                    "%Y-%m-%d")

        if list_date_min or list_date_max:
            query['list_date'] = {}
            if list_date_min:
                query['list_date'] = list_date_min.strftime(
                    "%Y-%m-%d")
            if list_date_max:
                query['list_date'] = list_date_max.strftime(
                    "%Y-%m-%d")

        if price_min or price_max:
            query['listing_price'] = {}
            if price_min:
                query['listing_price']['min'] = price_min
            if price_max:
                query['listing_price']['max'] = price_max

        if price_reduce_date_min or price_reduce_date_max:
            query['price_reduced_date'] = {}
            if price_reduce_date_min:
                query['price_reduced_date']['min'] = price_reduce_date_min.strftime(
                    "%Y-%m-%d")
            if price_reduce_date_max:
                query['price_reduced_date']['max'] = price_reduce_date_max.strftime(
                    "%Y-%m-%d")

        if hoa_fee_min or hoa_fee_max:
            if include_incomplete_hoa:
                hoa_key = "hoa_fee_optional"
            else:
                hoa_key = "hoa_fee"

            query[hoa_key] = {}
            if hoa_fee_min:
                query[hoa_key]['min'] = hoa_fee_min
            if hoa_fee_max:
                query[hoa_key]['max'] = hoa_fee_max

        if interior_sqft_max or interior_sqft_min:
            query['sqft'] = {}

            if interior_sqft_min:
                query['sqft']['min'] = interior_sqft_min
            if interior_sqft_max:
                query['sqft']['max'] = interior_sqft_max

        if lot_sqft_max or lot_sqft_min:
            query['lot_sqft'] = {}

            if lot_sqft_min:
                query['lot_sqft']['min'] = lot_sqft_min
            if lot_sqft_max:
                query['lot_sqft']['max'] = lot_sqft_max

        if year_built_min or year_built_max:
            query['year_built'] = {}

            if year_built_min:
                query['year_built']['min'] = year_built_min
            if year_built_max:
                query['year_built']['max'] = year_built_max

        if bedrooms_min or bedrooms_max:
            query['beds'] = {}
            if price_min:
                query['beds']['min'] = bedrooms_min
            if price_max:
                query['beds']['max'] = bedrooms_max

        if bathrooms_min or bathrooms_max:
            query['baths'] = {}
            if price_min:
                query['baths']['min'] = bathrooms_min
            if price_max:
                query['baths']['max'] = bathrooms_max

        query['status'] = list(status)

        if sold_date_min or sold_date_max:
            query['sold_date'] = {}
            if price_min:
                query['sold_date']['min'] = sold_date_min
            if price_max:
                query['sold_date']['max'] = sold_date_max

        if prop_type:
            query['type'] = list(prop_type)

        if keywords:
            query['keywords'] = keywords

        self.payload['variables']['query'] = query
        return self

    def set_operation_name(self, name: str = "ConsumerSearchMainQuery") -> 'Sale_Query':
        """Sets the operationName in the request payload. Not recommended to change.

        Args:
            name (str, optional): operationName. Defaults to "ConsumerSearchMainQuery".

        Returns:
            Query: Returns self
        """

        if name is None:
            try:
                self.payload.pop('operationName')
            except KeyError:
                pass
        else:
            self.payload['operationName'] = name

        return self

    def set_call_from(self, call_from: str = "SRP") -> 'Sale_Query':
        """Sets the callfrom in the request payload. Not recommended to change.

        Args:
            call_from (str, optional): call_from. Defaults to "SRP".

        Returns:
            Query: Returns self
        """

        if call_from is None:
            try:
                self.payload.pop('callfrom')
            except KeyError:
                pass
        else:
            self.payload['callfrom'] = call_from

        return self

    def set_nr_query_type(self, nr_query_type: str = None) -> 'Sale_Query':
        """Sets the nrQueryType in the request payload. Not recommended to change.

        Args:
            nr_query_type (str, optional): nr_query_type. Defaults to None.

        Returns:
            Query: Returns self
        """

        if nr_query_type is None:
            try:
                self.payload.pop('nrQueryType')
            except KeyError:
                pass
        else:
            self.payload['nrQueryType'] = nr_query_type

        return self

    def set_visitor_id(self, visitor_id: str = None) -> 'Sale_Query':
        """Sets the visitor_id in the request payload. Unless set via this method, no visitor_id will be included in the payload

        Args:
            visitor_id (str, optional): visitor_id. Defaults to None.

        Returns:
            Query: Returns self
        """

        if visitor_id is None:
            try:
                self.payload.pop('visitor_id')
            except KeyError:
                pass
        else:
            self.payload['visitor_id'] = visitor_id

        return self

    def set_is_client(self, is_client: bool = True) -> 'Sale_Query':
        """Sets the isClient in the request payload. Unclear as it what this does.

        Args:
            is_client (bool, optional): isClient. Defaults to True.

        Returns:
            Query: Returns self
        """

        if is_client is None:
            try:
                self.payload.pop('isClient')
            except KeyError:
                pass
        else:
            self.payload['isClient'] = is_client

        return self

    def set_seo_payload(self, seo_payload: Dict[str, Any] = None) -> 'Sale_Query':
        """Sets the seoPayload in the request payload. It is unclear what this does. This is also by default excluded from the payload unless specifically added by this method.

        Args:
            seo_payload (Dict[str, Any], optional): seoPayload. Defaults to None.

        Returns:
            Query: Returns self
        """

        if seo_payload is None:
            try:
                self.payload.pop('seoPayload')
            except KeyError:
                pass
        else:
            self.payload['seoPayload'] = seo_payload

        return self

    def get_payload(self) -> Dict[str, Any]:
        """Returns the query POST request JSON payload.

        Returns:
            Dict[str, Any]: The query POST request JSON payload
        """
        return self.payload

    def get_post_params(self) -> Dict[str, Any]:
        """Returns the query POST request parameters.

        Returns:
            Dict[str, Any]: The query POST request paramters
        """
        return self.post_params

    def get_request(self, url: str = defaults.SEARCH_URL, headers: Dict = defaults.HEADER) -> requests.Response:
        """Sends a POST request to the Realtor.com GRAPHQL PUBLIC API and returns the response.

        Args:
            url (str, optional): The GRAPHQL API URL. Defaults to defaults.URL.
            headers (Dict, optional): The header parameters as a dictionary. Defaults to defaults.HEADER.

        Returns:
            requests.Response: The request response
        """
        return requests.post(url, json=self.payload, headers=headers, params=self.post_params)

    def get_response(self, returns: Literal["full", "results"] = "results", url: str = defaults.SEARCH_URL, headers: Dict = defaults.HEADER) -> Dict[str, Any]:
        """Sends a POST request to Realtor.com GRAPHQL Public API and returns the JSON content of the response.

        Args:
            returns (Literal[&quot;full&quot;, &quot;results&quot;], optional): This determines if the full json dictionary will be returned ("full") or just the search results ("results"). Note that the search results include the count, total, and 'results' which contains the list of acutal results. Defaults to "results".
            url (str, optional): The GRAPHQL API URL. Defaults to defaults.URL.
            headers (Dict, optional): The header parameters as a dictionary. Defaults to defaults.HEADER.

        Returns:
            Dict[str, Any]: The request response json data
        """

        data = self.get_request(url, headers).json()

        if returns == "full":
            return data
        elif returns == "results":
            return data.get('data', {}).get('home_search')
        else:
            raise ValueError(
                f"returns param must be either 'full' or 'results', was {returns}")
