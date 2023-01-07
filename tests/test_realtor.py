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
    @staticmethod
    @pytest.fixture(scope="class")
    def sale_subset(reasonable_sale_results):
        return [
            Sale(f"https://www.realtor.com/realestateandhomes-detail/{r['permalink']}") for r in reasonable_sale_results['results'][:3]
        ]

    @staticmethod
    def test_init(sale_subset):
        # just a basic check if init doesn't run into errors
        sale_subset

    @staticmethod
    def test_get_loan_estimates(sale_subset):
        p: Sale
        for p in sale_subset:
            assert isinstance(p.get_loan_estimates(p.price, round(
                p.price*.2), p.fips, p.state_code, p.yearly_property_tax, p.hoa_fee), dict)

    @staticmethod
    def test_get_estimate_monthly_payment(sale_subset):
        p: Sale
        for p in sale_subset:
            assert isinstance(p.get_estimated_monthly_payment(), float)

    @staticmethod
    def test_get_noise_metrics(sale_subset):
        p: Sale
        for p in sale_subset:
            assert isinstance(p.get_noise_metrics(
                p.latitude, p.longitude), dict)

    @staticmethod
    def test_get_flood_risk(sale_subset):
        p: Sale
        for p in sale_subset:
            assert isinstance(p.get_flood_risk(p.property_id), dict)

    @staticmethod
    def test_get_fire_risk(sale_subset):
        p: Sale
        for p in sale_subset:
            assert isinstance(p.get_fire_risk(p.property_id), dict)

    @staticmethod
    def test_get_value_estimates(sale_subset):
        p: Sale
        for p in sale_subset:
            assert isinstance(p.get_value_estimates(p.property_id), dict)

    @staticmethod
    def test_get_nearby_home_values(sale_subset):
        p: Sale
        for p in sale_subset:
            assert isinstance(p.get_nearby_home_values(p.property_id), list)

    @staticmethod
    def test_get_similar_homes(sale_subset):
        p: Sale
        for p in sale_subset:
            assert isinstance(p.get_similar_homes(p.property_id), dict)

    @staticmethod
    def test_get_homes_in_area_with_price(sale_subset):
        p: Sale
        for p in sale_subset:
            assert isinstance(p.get_homes_in_area_with_price(
                p.zip, p.price*.8, p.price*1.2), dict)
