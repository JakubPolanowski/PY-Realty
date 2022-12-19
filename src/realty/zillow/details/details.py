# this file is responsible for parsing the detailUrl page found in the query results.
from typing import Literal, List, Dict, Any


class Details:
    # TODO
    # This gets the detail for a single page given detail_url and status_type

    def __init__(self, detail_url: str, status_type: Literal["FOR_RENT", "FOR_SALE"]) -> None:
        pass  # TODO


class Results:
    # TODO
    # This gets the details for all the results, fetching results fo all

    def __init__(self, results: List[Dict[Any, Any]]) -> None:
        pass  # TODO


class Results_Lazy:
    # TODO
    # This gets the details for all results, but will only fetch when specific detail is fetched

    def __init__(self, results: List[Dict[Any, Any]]) -> None:
        pass  # TODO
