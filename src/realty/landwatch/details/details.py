from typing import Dict, Any


class Listing_Details:

    def __init__(self, property_result: Dict[str, Any]) -> None:

        self.check_property_results_keys(property_result)

        self.price: int = property_result['price']

        self.acres: int = property_result['acres']
        self.sqft: int = property_result['homesqft']

        self.address: str = property_result['address']
        self.city: str = property_result['city']
        self.county: str = property_result['county']
        self.state: str = property_result['state']
        self.state_code: str = property_result['stateCode']
        self.zip: str = property_result['zip']
        self.lake: str = property_result['lake']
        self.longitude: float = property_result['longitude']
        self.latitude: float = property_result['latitude']

        self.auction_date: str = property_result['auctionDate']

        self.description: str = property_result['description']
        self.has_house: bool = property_result['hasHouse']
        self.has_video: bool = property_result['hasVideo']
        self.has_virtual_tour: bool = property_result['hasVirtualTour']
        self.labels: str = property_result['propertyTypesLabel']

        self.baths: float = property_result['baths']
        self.half_baths: float = property_result['halfBaths']
        self.beds: float = property_result['beds']

        self.broker_company: str = property_result['brokerCompany']
        self.broker_name: str = property_result['brokerName']

        self.url: str = f"https://www.landwatch.com{property_result['canonicalUrl']}"

    @staticmethod
    def check_property_results_keys(property_result: Dict[str, Any]) -> None:
        """Checks for the expected keys in a Landwatch property_result dictionary/json structure

        Args:
            property_result (Dict[str, Any]): Landwatch property_result dictionary/json

        Raises:
            KeyError: Missing keys
        """

        EXPECTED_KEYS = {
            'accountId', 'acres', 'acresDisplay', 'adTargetingCountyId', 'address', 'auctionDate', 'baths', 'bathsDisplay', 'bedsDisplay', 'beds', 'brokerCompany', 'brokerName', 'canonicalUrl', 'city', 'cityID', 'companyLogoDocumentId', 'county', 'countyId', 'countyLabel', 'description', 'encodedBoundaryPoints', 'externalSourceId', 'halfBaths', 'halfBathsDisplay', 'hasHouse', 'hasVideo', 'hasVirtualTour', 'homesqft', 'homesqftDisplay', 'imageCount', 'imageAltTextDisplay',
            'id', 'isALC', 'isDiamond', 'isFirstFreeListing', 'isGold', 'isHeadlineAd', 'isLiked', 'isPlatinum', 'isShowcase', 'lake', 'latitude', 'listHubListingKey', 'listingLevel', 'listingLevelTitle', 'longitude', 'partnerId', 'portraitDocumentId', 'price', 'priceChange', 'priceDisplay', 'propertyTypes', 'propertyTypesLabel', 'schemaData', 'shortPrice', 'siteListingId', 'state', 'stateAbbreviation', 'stateCode', 'stateId', 'status', 'thumbnailDocumentId', 'title', 'types', 'zip'
        }

        if EXPECTED_KEYS == set(property_result.keys()):
            return  # all expected keys are there

        missing = EXPECTED_KEYS - set(property_result.keys())

        raise KeyError(
            f'property_result is missing the following keys: {", ".join(missing)}')
