import pytest
from src.realty.landwatch import Query
from src.realty.landwatch.details import Listing_Details


@pytest.fixture(scope="module")
def reasonable_query():
    q = Query()
    return q.get_response()


@pytest.fixture(scope="module")
def reasonable_results():
    q = Query()
    return q.get_results()['propertyResults']


class TestQuery:

    @staticmethod
    def test_status_code(reasonable_query):
        assert reasonable_query.status_code == 200

    @staticmethod
    def test_expected_json_keys(reasonable_query):
        assert list(
            reasonable_query.json().keys()
        ) == ['activeFilters', 'amChartMapData', 'breadCrumbSchema', 'brokerDetails', 'carouselCounts', 'collectionPageSchema', 'dataLayerSearchResponse', 'filterSections', 'footer', 'headlineAd', 'routeContext', 'searchResults', 'searchUI', 'seoLinkSections', 'seoTextSection', 'seoTextSection2', 'siteId']

    @staticmethod
    def test_expected_results(reasonable_query):
        assert isinstance(
            reasonable_query.json(
            )['searchResults']['propertyResults'],
            list
        )

    @staticmethod
    def test_more_than_zero_results(reasonable_query):
        assert len(reasonable_query.json(
        )['searchResults']['propertyResults']) > 0

    @staticmethod
    def test_expected_result_keys(reasonable_query):
        # just required ones
        expected_keys = {'accountId', 'acres', 'acresDisplay', 'adTargetingCountyId', 'address', 'auctionDate', 'baths', 'bathsDisplay', 'bedsDisplay', 'beds', 'brokerCompany', 'brokerName', 'canonicalUrl', 'city', 'cityID', 'companyLogoDocumentId', 'county', 'countyId', 'countyLabel', 'description', 'encodedBoundaryPoints', 'externalSourceId', 'halfBaths', 'halfBathsDisplay', 'hasHouse', 'hasVideo', 'hasVirtualTour', 'homesqft', 'homesqftDisplay', 'imageCount', 'imageAltTextDisplay',
                         'id', 'isALC', 'isDiamond', 'isFirstFreeListing', 'isGold', 'isHeadlineAd', 'isLiked', 'isPlatinum', 'isShowcase', 'lake', 'latitude', 'listHubListingKey', 'listingLevel', 'listingLevelTitle', 'longitude', 'partnerId', 'portraitDocumentId', 'price', 'priceChange', 'priceDisplay', 'propertyTypes', 'propertyTypesLabel', 'schemaData', 'shortPrice', 'siteListingId', 'state', 'stateAbbreviation', 'stateCode', 'stateId', 'status', 'thumbnailDocumentId', 'title', 'types', 'zip'}

        results = reasonable_query.json(
        )['searchResults']['propertyResults']

        assert all([
            expected_keys - set(r.keys()) == set() for r in results
        ])


class TestListingDetails:
    @staticmethod
    @pytest.fixture(scope="class")
    def listing_subset(reasonable_results):
        return [
            Listing_Details(lr) for lr in reasonable_results[:3]
        ]

    @staticmethod
    def test_init(listing_subset):
        # just a basic check if init doesn't run into errors
        listing_subset
