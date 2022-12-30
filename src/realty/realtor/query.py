import requests
import json
import requests
from typing import Dict, Any, List, Literal, Set
from . import defaults


class Query:

    def __init__(self) -> None:

        self.set_post_params()
        self.set_json_payload()
        self.set_graphql_query()

        pass  # TODO

    def set_post_params(self, post_parms: Dict[str, Any] = {"client_id": "rdc-x", "schema": "vesta"}) -> 'Query':
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

    def set_json_payload(self, payload: Dict[str, Any] = defaults.LISTING_SEARCH_PAYLOAD) -> 'Query':
        """Sets the request payload, this is the body of the request, sent as a POST. Note that this is rather complicated as the Realotr PUBLIC API is not documented therefore it is recommended to use the default. Also when setting the payload, there are two key keys that are missing real values, 'query' (GraphQL query - see set_graphql_query) and 'variables' --> 'query' (fitler criteria - see set_filter_query and set_filter_query_preset)

        Args:
            payload (Dict[str, Any], optional): The POST request JSON payload. Defaults to defaults.LISTING_SEARCH_PAYLOAD.

        Returns:
            Query: Returns self
        """

        self.payload = payload
        return self

    def set_payload_variables(self, **kwargs) -> 'Query':
        """Sets variable key value pairs inside the POST request payload. This is not recommended to do manually, for advanced use only.

        Returns:
            Query: Returns self
        """

        for key, item in kwargs.items():
            self.payload['variables'][key] = item

        return self

    def remove_payload_variables(self, *args) -> 'Query':
        """Removes variable keys inside the POST request payload. This is not recommended to do manually (as in using this function), for advanced use only.

        Returns:
            Query: Returns self
        """

        for key in args:
            if key in self.payload['variables']:
                self.payload['variables'].pop(key)

        return self

    def set_var_client_data(self, client_data: Dict[str, Any] = {"device_data": {"device_type": "web"}, "user_data": {}}) -> 'Query':
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

    def set_var_limit(self, limit: int = 42) -> 'Query':
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

    def set_var_offset(self, offset: int = 0) -> 'Query':
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

    def set_var_sort_type(self, sort_type: str | Dict[str, Any]) -> 'Query':
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

    def set_var_sort(self, sort: Dict[str, Any]) -> 'Query':
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

    def set_var_sort_preset(self, by: Literal["relevant", "price", "listing age", "open house date", "last reduced", "interior sqft", "lot_size"] = "relevant", ascending=False) -> 'Query':
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

    def set_var_zoho_query(self, zoho_query: Dict[str, Any]) -> 'Query':
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

    def set_var_geo_supported_slug(self, geo_supported_slug: Dict[str, Any]) -> 'Query':
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

    def set_var_by_prop_type(self, by_prop_type: Dict[str, Any]) -> 'Query':
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

    def set_graphql_query(self, query: str = defaults.GRAPHQL_LISTING_SEARCH_QUERY) -> 'Query':
        """Sets the GraphQL query. Note that this is rather complicated as the Realtor PUBLIC API is not documented therefore it is recommended to use the default.

        Args:
            query (str, optional): The GraphQL query for the listings search. Defaults to defaults.GRAPHQL_LISTING_SEARCH_QUERY.

        Returns:
            Query: Returns self
        """

        self.payload['query'] = query
        return self

    def set_filter_query(self, query: Dict[str, Any]) -> 'Query':
        """Sets the filter query within 'payload' -> 'variables' -> 'query'. This is used to filter which results should be returned by the search. Note that this is a complex function to use as the PUBLIC Realor.com isn't documented therefore using set_filter_query_preset is recommended as it builds a filter query based on simple parameters.

        Args:
            query (Dict[str, Any]): The filter for the listings query

        Returns:
            Query: Returns self
        """

        self.payload['variables']['query'] = query
        return self

    def set_filter_query_preset(self) -> 'Query':
        ...  # TODO

    def set_operation_name(self, name: str = "ConsumerSearchMainQuery") -> 'Query':
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

    def set_call_from(self, call_from: str = "SRP") -> 'Query':
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

    def set_nr_query_type(self, nr_query_type: str = None) -> 'Query':
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

    def set_visitor_id(self, visitor_id: str = None) -> 'Query':
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

    def set_is_client(self, is_client: bool = True) -> 'Query':
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

    def set_seo_payload(self, seo_payload: Dict[str, Any] = None) -> 'Query':
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

    def get_request(self, url: str = defaults.URL, headers: Dict = defaults.HEADER) -> requests.Response:
        """Sends a POST request to the Realtor.com GRAPHQL PUBLIC API and returns the response.

        Args:
            url (str, optional): The GRAPHQL API URL. Defaults to defaults.URL.
            headers (Dict, optional): The header parameters as a dictionary. Defaults to defaults.HEADER.

        Returns:
            requests.Response: The request response
        """
        return requests.post(url, json=self.payload, headers=headers, params=self.post_params)

    def get_response(self, returns: Literal["full", "results"] = "results", url: str = defaults.URL, headers: Dict = defaults.HEADER) -> Dict[str, Any]:
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
