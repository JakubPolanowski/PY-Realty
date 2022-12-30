import requests
import json
import requests
from typing import Dict, Any, List, Literal, Union, Set
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
