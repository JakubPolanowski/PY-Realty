# this file is responsible for parsing the detailUrl page found in the query results.
from typing import Literal, List, Dict, Any
from . import Sale, Rental_Home, Rental_Apartment


def parse_listing(detail_url: str, status_type: Literal["FOR_RENT", "FOR_SALE"]) -> Sale | Rental_Apartment | Rental_Home:
    """Parses a listing based on the Zillow Detail URL

    Args:
        detail_url (str): The URL with the listing detaill
        status_type (Literal[&quot;FOR_RENT&quot;, &quot;FOR_SALE&quot;]): The status type, which should be either FOR_RENT or FOR_SALE

    Raises:
        ValueError: Detail URL for FOR_RENT is missing expected keywords
        ValueError: Unhandled status_type/unexpected status_type

    Returns:
        Sale | Rental_Apartment | Rental_Home: _description_
    """

    if status_type == "FOR_SALE":
        return Sale(detail_url)

    if status_type == "FOR_RENT":
        if 'homedetails' in detail_url:
            return Rental_Home(detail_url)
        elif '\\b\\' in detail_url:
            return Rental_Apartment(f"https://www.zillow.com{detail_url}")
        else:
            raise ValueError(
                "FOR_RENTAL listing detail URL is missing expected keywords")

    raise ValueError(
        f"status_type should be either FOR_RENT or FOR_SALE, was {status_type}")


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
