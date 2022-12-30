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
        """Sets the sort_type in the payload variables. This is an advanced function, for regular usage, use set_var_sort_type_preset.

        Args:
            sort_type (str | Dict[str, Any]): The sort_type paramter that specifies how the results will be sorted

        Returns:
            Query: Returns self
        """

        if sort_type is None:
            return self.remove_payload_variables('sort_type')

        self.payload['variables']['sort_type'] = sort_type
        return self

    def set_var_sort_type_preset(self) -> 'Query':
        ...  # TODO

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
