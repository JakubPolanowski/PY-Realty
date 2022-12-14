import pytest
import random
from numbers import Number
from src.realty.zillow import Query
from src.realty.zillow.details import details_page
from src.realty.zillow.details import Sale, Rental_Home, Rental_Apartment
from src.realty.zillow import scrape_listing, scrape_listings, lazy_scrape_listings

# Since there is no great source of truth, the goal of the tests here are for the most part just to ensure errors are not encountered when dealing with typical listings/queries


@pytest.fixture(scope="module")
def reasonable_query():
    q = Query()

    q.set_page(1) \
        .set_search_term("Columbus, OH") \
        .set_map_bounds(west=-83.33248072216797, east=-83.33248072216797, south=39.66914522069816, north=40.29576580257015)
    return q.get_response("request")


@pytest.fixture(scope="module")
def reasonable_sale_results():
    q = Query()

    q.set_page(1) \
        .set_search_term("Columbus, OH") \
        .set_map_bounds(west=-83.33248072216797, east=-83.33248072216797, south=39.66914522069816, north=40.29576580257015)
    return q.get_response("results")


@pytest.fixture(scope="module")
def reasonable_rental_home_results():
    q = Query()
    q.set_page(1) \
        .set_search_term("Columbus, OH") \
        .set_map_bounds(west=-83.33248072216797, east=-83.33248072216797, south=39.66914522069816, north=40.29576580257015) \
        .set_filter_preset(for_sale=False, home_type={"SingleFamily"})
    r = q.get_response(returns='results')
    return [x for x in r if "homedetails" in x['detailUrl']]


@pytest.fixture(scope="module")
def reasonable_rental_apartment_results():
    q = Query()
    q.set_page(1) \
        .set_search_term("Columbus, OH") \
        .set_map_bounds(west=-83.33248072216797, east=-83.33248072216797, south=39.66914522069816, north=40.29576580257015) \
        .set_filter_preset(for_sale=False, home_type={"Apartment"})
    r = q.get_response(returns='results')
    return [x for x in r if "/b/" in x['detailUrl']]


class TestQuery:

    @staticmethod
    def test_status_code(reasonable_query):
        assert reasonable_query.status_code == 200

    @staticmethod
    def test_expected_json_keys(reasonable_query):
        assert list(
            reasonable_query.json().keys()
        ) == ['user', 'mapState', 'regionState', 'searchPageSeoObject', 'cat1', 'categoryTotals']

    @staticmethod
    def test_expected_results(reasonable_query):
        assert isinstance(
            reasonable_query.json()['cat1']['searchResults']['listResults'],
            list
        )

    @staticmethod
    def test_more_than_zero_results(reasonable_query):
        assert len(reasonable_query.json()[
                   'cat1']['searchResults']['listResults']) > 0

    @staticmethod
    def test_expected_result_keys(reasonable_query):
        expected_keys = {'zpid', 'detailUrl', 'statusType'}

        results = reasonable_query.json().get("cat1").get(
            'searchResults').get('listResults')

        assert all([
            expected_keys - set(r.keys()) == set() for r in results
        ])


class TestDetailsPage:
    @staticmethod
    @pytest.fixture(scope="class")
    def page(reasonable_sale_results):
        url = reasonable_sale_results[0]['detailUrl']
        return details_page.Details_Page.get_page(url)

    @staticmethod
    def test_get_page_status_code(page):
        assert page.status_code == 200

    @staticmethod
    def test_make_soup(page):
        # This is just to test that no exceptions occur
        details_page.Details_Page.make_soup(page)

    @staticmethod
    def test_get_walk_and_bike_score(reasonable_sale_results):
        zpid = reasonable_sale_results[0]['zpid']

        wb_result = details_page.Details_Page.get_walk_and_bike_score(zpid)

        assert isinstance(wb_result, dict)
        assert 'property' in wb_result
        assert 'walkScore' in wb_result['property']
        assert 'bikeScore' in wb_result['property']


class TestNextJSDetailsPage:
    @staticmethod
    @pytest.fixture(scope="class")
    def page(reasonable_rental_apartment_results):
        url = reasonable_rental_apartment_results[0]['detailUrl']
        return details_page.NextJS_Detail_Page.get_page(f"https://www.zillow.com{url}")

    @staticmethod
    def test_get_next_data(page):
        assert isinstance(
            details_page.NextJS_Detail_Page.get_next_data(
                details_page.NextJS_Detail_Page.make_soup(page)
            ), dict
        )

    @staticmethod
    def test_get_initial_and_redux(page):

        data = details_page.NextJS_Detail_Page.get_next_data(
            details_page.NextJS_Detail_Page.make_soup(page)
        )
        initial, redux = details_page.NextJS_Detail_Page.get_initial_data_and_redux_state(
            data)

        assert isinstance(initial, dict)
        assert isinstance(redux, dict)


class TestPreloadDetailsPage:
    @staticmethod
    @pytest.fixture(scope="class")
    def preload_details_subset(reasonable_sale_results):
        return [
            details_page.Preload_Detail_Page(r['detailUrl']) for r in reasonable_sale_results[:3]
        ]

    @staticmethod
    def test_init(preload_details_subset):
        # just a basic check if init doesn't run into errors
        preload_details_subset

    @staticmethod
    def test_get_at_a_glance(preload_details_subset):
        for p in preload_details_subset:
            assert isinstance(p.get_at_a_glance(), dict)

    @staticmethod
    def test_get_tags(preload_details_subset):
        for p in preload_details_subset:
            assert isinstance(p.get_tags(), list)

    @staticmethod
    def test_get_facts_and_features(preload_details_subset):
        for p in preload_details_subset:
            assert isinstance(p.get_facts_and_features(), dict)


class TestSale:
    @staticmethod
    @pytest.fixture(scope="class")
    def sale_subset(reasonable_sale_results):
        return [
            Sale(r['detailUrl']) for r in reasonable_sale_results[:3]
        ]

    @staticmethod
    def test_init(sale_subset):
        # just a basic check if init doesn't run into errors
        sale_subset

    @staticmethod
    def test_get_likely_to_sell(sale_subset):
        for p in sale_subset:
            assert isinstance(p.get_likely_to_sell(), (str, type(None)))

    @staticmethod
    def test_get_monthly_estimated_cost(sale_subset):
        # this is primarily to test if function runs without error as opposed
        # to function calculation validity
        for p in sale_subset:
            assert isinstance(
                p.get_monthly_estimated_cost(p.price*.2),
                Number
            )


class TestRentalHome:
    @staticmethod
    @pytest.fixture(scope="class")
    def rental_subset(reasonable_rental_home_results):
        return [
            Rental_Home(r['detailUrl']) for r in reasonable_rental_home_results[:3]
        ]

    @staticmethod
    def test_init(rental_subset):
        # just a basic check if init doesn't run into errors
        rental_subset


class TestRentalApartment:
    @staticmethod
    @pytest.fixture(scope="class")
    def rental_subset(reasonable_rental_apartment_results):
        return [
            Rental_Apartment(f"https://www.zillow.com{r['detailUrl']}") for r in reasonable_rental_apartment_results[:3]
        ]

    @staticmethod
    def test_init(rental_subset):
        # just a basic check if init doesn't run into errors
        rental_subset

    @staticmethod
    def test_get_key_features(rental_subset):
        for p in rental_subset:
            assert isinstance(p.get_key_features(), dict)


class TestScrape:
    @staticmethod
    def test_scrape_sale(reasonable_sale_results):
        # this checks if correct class is return and no exception occurs
        assert isinstance(
            scrape_listing(
                reasonable_sale_results[0]["detailUrl"], 'FOR_SALE'),
            Sale
        )

    @staticmethod
    def test_scrape_rental_home(reasonable_rental_home_results):
        # this checks if correct class is return and no exception occurs
        assert isinstance(
            scrape_listing(
                reasonable_rental_home_results[0]["detailUrl"], 'FOR_RENT'),
            Rental_Home
        )

    @staticmethod
    def test_scrape_rental_apartment(reasonable_rental_apartment_results):
        # this checks if correct class is return and no exception occurs
        assert isinstance(
            scrape_listing(
                reasonable_rental_apartment_results[0]["detailUrl"], 'FOR_RENT'),
            Rental_Apartment
        )

    @staticmethod
    def test_scrape_listings(reasonable_sale_results):
        details = scrape_listings(reasonable_sale_results[:3])
        assert all([isinstance(x, Sale) for x in details])

    @staticmethod
    def test_lazy_scraping_indexing(reasonable_sale_results):
        lazy_details = lazy_scrape_listings(reasonable_sale_results)

        test_indexes = set(
            [random.randrange(len(reasonable_sale_results)) for _ in range(3)])
        for ti in test_indexes:
            assert isinstance(lazy_details[ti], Sale)

    @staticmethod
    def test_lazy_scraping_slicing(reasonable_sale_results):
        lazy_details = lazy_scrape_listings(reasonable_sale_results)

        details = lazy_details[:3]
        for d in details:
            assert isinstance(d, Sale)

    @staticmethod
    def test_lazy_scraping_iterating(reasonable_sale_results):
        lazy_details = lazy_scrape_listings(reasonable_sale_results)

        for detail in lazy_details[:min(3, len(lazy_details))]:
            assert isinstance(detail, Sale)
