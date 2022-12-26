# this file is responsible for parsing the detailUrl page found in the query results.
from typing import Literal, List, Dict, Any
import numpy as np
from time import sleep
from numbers import Number
from . import Sale, Rental_Home, Rental_Apartment


def scrape_listing(detail_url: str, status_type: Literal["FOR_RENT", "FOR_SALE"]) -> Sale | Rental_Apartment | Rental_Home:
    """Scrapes a listing based on the Zillow Detail URL

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
        elif '/b/' in detail_url:
            return Rental_Apartment(f"https://www.zillow.com{detail_url}")
        else:
            raise ValueError(
                "FOR_RENTAL listing detail URL is missing expected keywords")

    raise ValueError(
        f"status_type should be either FOR_RENT or FOR_SALE, was {status_type}")


def scrape_listings(query_results: List[Dict[str, Any]], delay: Number = 0, jitter: Number = 1, verbose=False) -> List[Sale] | List[Rental_Home] | List[Rental_Apartment]:
    """Scrapes a list of Zillow Detail URLs

    Args:
        query_results (List[Dict[str, Any]]): Results of the Query, see Query class
        delay (Number, optional): The static delay amount. This is to help prevent Zillow from blocking scraping due to high number of requests in rapid succession. Defaults to 0.
        jitter (Number, optional): The jitter factor for the delay time. Defaults to 1.
        verbose (bool, optional): If function should be verbose, printing out the progress of parsing the listings. Defaults to False.

    Returns:
        List[Sale] | List[Rental_Home] | List[Rental_Apartment]: List of scraped listing, which typically will be of one type, Sale, Rental_home, or Rental_Apartment, that being said if multiple types are mixed in query_results, the resulting list will be of multiple types.
    """

    delay_array = delay * np.random.rand(len(query_results)) * jitter
    # last delay should be zero since no more details to scrape
    delay_array[-1] = 0

    results = []
    for dtime, (i, result) in zip(delay_array, enumerate(query_results, 1)):

        results.append(
            scrape_listing(result["detailUrl"], result['statusType'])
        )

        if verbose:
            print(f"Parsed {i} of {len(query_results)}, delaying for {dtime}s")

        sleep(dtime)

    return results


class Lazy_Listings(list):
    """Lazy Listings is a list child class that takes a list of Query results and will return the scraped listing details based on the index or slice.
    """

    def __getitem__(self, n):
        result = super().__getitem__(n)

        if isinstance(result, list):
            return [scrape_listing(r["detailUrl"], r['statusType']) for r in result]
        else:
            return scrape_listing(result["detailUrl"], result['statusType'])

    def __iter__(self):
        for result in super().__iter__():
            yield scrape_listing(result["detailUrl"], result['statusType'])


def lazy_scrape_listings(query_results: List[Dict[str, Any]]) -> Lazy_Listings:
    """Scapes Zillow listing details with Lazy Evaluation. The Lazy_Listing class it returns can be used to scrape the details of the query results list by either iteration or indexing/slicing.

    Args:
        query_results (List[Dict[str, Any]]): Results of the Query, see Query class

    Returns:
        Lazy_Listings: Lazy_Listing list of query_results
    """
    return Lazy_Listings(query_results)
