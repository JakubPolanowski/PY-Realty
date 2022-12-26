import pytest
from numbers import Number
from src.realty.zillow import Query
from src.realty.zillow.details import details_page
from src.realty.zillow.details import Sale, Rental_Home, Rental_Apartment
# from src.realty.zillow import details
# Since there is no great source of truth, the goal of the tests here are to ensure that a reasonable query will return results in the expected format


@pytest.fixture(scope="module")
def reasonable_query():
    q = Query()

    q.set_page(1) \
        .set_search_term("Chattanooga, TN") \
        .set_map_bounds(west=-85.58309022900734, east=-85.18483583447609, south=34.73748469750508, north=35.40678434232889)
    return q.get_response("request")


@pytest.fixture(scope="module")
def reasonable_sale_results():
    q = Query()

    q.set_page(1) \
        .set_search_term("Chattanooga, TN") \
        .set_map_bounds(west=-85.58309022900734, east=-85.18483583447609, south=34.73748469750508, north=35.40678434232889)
    return q.get_response("results")


@pytest.fixture(scope="module")
def reasonable_rental_home_results():
    q = Query()
    q.set_page(1) \
        .set_search_term("Chattanooga, TN") \
        .set_map_bounds(west=-85.58309022900734, east=-85.18483583447609, south=34.73748469750508, north=35.40678434232889) \
        .set_filter_preset(for_sale=False, home_type={"SingleFamily"})
    r = q.get_response(returns='results')
    return [x for x in r if "homedetails" in x['detailUrl']]


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
    ...  # TODO


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
    ...  # TODO


class TestScrape:
    ...  # TODO
