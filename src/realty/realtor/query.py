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
