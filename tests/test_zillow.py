import pytest
from src.realty.zillow import Query
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


class TestQuery:

    @staticmethod
    def test_status_code(reasonable_query):
        assert reasonable_query.status_code == 200
