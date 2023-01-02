import pytest
from src.realty.realtor import Sale_Query
from src.realty.realtor.details import Sale


@pytest.fixture(scope="module")
def reasonable_sale_query():
    q = Sale_Query()
    q.set_filter_query_preset(
        search_location="Chattanooga, TN"
    )
    return q.get_request()


@pytest.fixture(scope="module")
def reasonable_sale_results():
    q = Sale_Query()
    q.set_filter_query_preset(
        search_location="Chattanooga, TN"
    )
    return q.get_response('results')


class TestSalesQuery:

    @staticmethod
    def test_status_code(reasonable_sale_query):
        assert reasonable_sale_query.status_code == 200

    @staticmethod
    def test_expected_json_keys(reasonable_sale_query):
        assert list(
            reasonable_sale_query.json().keys()
        ) == ['data']

    @staticmethod
    def test_expected_results(reasonable_sale_query):
        assert isinstance(
            reasonable_sale_query.json(
            )['data']['home_search']['results'],
            list
        )

    @staticmethod
    def test_more_than_zero_results(reasonable_sale_query):
        assert len(reasonable_sale_query.json()[
                   'data']['home_search']['results']) > 0

    @staticmethod
    def test_expected_result_keys(reasonable_sale_query):
        # just required ones
        expected_keys = {'property_id', 'permalink', }

        results = reasonable_sale_query.json(
        )['data']['home_search']['results']

        assert all([
            expected_keys - set(r.keys()) == set() for r in results
        ])


class TestSales:
    ...  # TODO
