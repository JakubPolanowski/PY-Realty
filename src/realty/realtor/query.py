import requests
import json
import requests
from typing import Dict, Any, List, Literal, Union, Set
from . import defaults


class Query:

    def __init__(self) -> None:

        self.set_post_params()

        pass  # TODO

    def set_post_params(self, post_parms: Dict[str, Any] = None) -> 'Query':
        """Sets the post request parameters, the dictionary that will be passed to the 'param' parameter in the post request call. The exact effect of these is not entirely clear and therefore it is recommended to left as default.

        Args:
            post_parms (Dict[str, Any], optional): The dictionary of post request paramters. If None, will fall back on defaults -> {"client_id": "rdc-x", "schema": "vesta"}. Defaults to None.

        Returns:
            Query: Returns self
        """

        if not post_parms:
            self.post_params = {"client_id": "rdc-x", "schema": "vesta"}
        else:
            self.post_params = post_parms

        return self
