# This handles parsing of rental apartments data
import requests
from typing import Dict, Any, List
from numbers import Number
from .details_page import NextJS_Detail_Page
from .. import defaults


class Rental_Apartment(NextJS_Detail_Page):

    def __init__(self, url: str) -> None:
        """This initializes the Rental_Apartment object, which call a GET request on the Zillow detail URL. 

        Attributes:
            url (str): The detail URL that this class has parsed
            soup (BeautifulSoup): The html content of this page parsed to a soup object

            ndata (Dict): The __NEXT_DATA__ data dictionary scraped from html soup
            idata (Dict): The initial data dictionary component of ndata
            redux_state (Dict): the redux state dictionary component of ndata

            zpid (str): The Zillow property ID
            lot_id (str): The Zillow lot ID

            data (Dict): The API data dictionary. Will be result of a fresh API call unless no data is returned, in which case will fall back to idata (initial data)

            building (Dict): The building data dictionary, found within data
            building_attributes (Dict): The building attributes data dictioanry, found within building

            building_name (str): The building name

            description (str): The apartment building description
            low_income (bool): If apartment building is low income
            senior_housing (bool): If building is senior housing
            student_housing (bool): If building is student housing

            office_hours (List[str]): List of the building's office hours
            office_number (str): The phone number of the building's office

            key_features (Dict): Key features of the building
            unit_features (List[str]): The universal features of the apartment units

            city (str): The city
            county (str): The county
            state (str): The state
            zip (str): The zip code
            street_address (str): The street address of the building

            application_fee (Number | None): The application fee
            administrative_fee (Number | None): The administrative fee 
            deposit_fee_min (Number | None): The min deposit fee
            deposit_fee_max (Number | None): The max deposit fee
            lease_terms (List[str]): The lease teams. Note that is is more a keyword/descriptor as opposed to a legal lease contract terms. So you might expected something like ['Flexable'] if the terms are flexable/negotiable
            utilities_included (List[str]): The included utilities

            parking_policies (List[dict]): List of parking policies
            parking_types (List[str]): List of parking types available, for example "off_road"
            pet_policies (List[dict]): The list of pet policies

            shared_laundry (bool): Is there shared laundry, True/False
            air_conditioning (str): Air conditioning description
            appliances (List[str]): List of appliances
            outdoor_common_areas (List[str]): List of outdoor common areas
            barbecue (bool): If there a/are barbecue(s) in the common areas, True/False
            heating_source (str): The heating source
            elevator (Any): The elevator specification of the building
            community_rooms (List[str]): List of community rooms available
            sports_courts (List[str]): List of sports courts available
            bicycle_storage (Any | None): Bicycle storage specification
            guest_suite (Any | None): Guest Suite specification
            storage (Any | None): Storage specification
            pet_park (Any | None): Pet park specification
            maintenance_24_7 (Any | None): Specification of 24/7 maintenance availability
            dry_cleaning_drop_off (Any | None): Specification of dry cleaning drop off availability
            online_rent_payment (Any | None): Specification of online rent payment availability
            online_maintenance_portal (Any | None): Specification of online maintenance portal availability
            onsite_management (bool): If management is onsite, True/False
            package_service (Any | None): Specification of package service availability
            valet_trash (Any | None): Specification of valet trash availability
            spanish_speaking_staff (Any | None): Specification of spanish speaking staff availability
            security_types (List[str]): The types of security that building has
            view_types (List[str]): List of views (scenic) that the building has
            hot_tub (Any | None): Specification of hot tub availability
            sauna (Any | None): Specification of sauna availability
            swimming_pool (bool): If has swimming pool, True/False
            assisted_living (bool): If building has assisted living, True/False
            disabled_access (Any | None): The specification of disabled access availablity
            floor_covering (List[str]): The list of floor coverings that the building has
            communication_types (List[str]): The list of communication types the building has/supports. For instance "high speed internet"
            ceiling_fan (Any | None): Specification of ceiling fan availability
            fire_place (Any | None): Specification of fire place availability
            patio_balcony (bool): If building has patio balcony, True/False
            furnished (Any | None): Specification of if/how is furnished
            custom_ammenites (str): Description of custom ammenites

            floorplans (List[dict]): List of available floor plans

            management (dict): Management details

            schools (List[dict]): The list of nearby schools
            nearby_cities (List[dict]): The list of nearby cities
            nearby_neighborhoods (List[dict]): The list of nearby neighborhoods
            nearby_zip (List[dict]): The list of nearby zip codes
            nearby_rental_buildings (List[dict]): The list of nearby rental homes and apartments
            nearby_amenities (List[dict]): The list of nearby amenities 

            review_info (dict): The data dictionary of reviews
        """

        self.url = url

        # get soup
        self.soup = self.make_soup(self.get_page(self.url))

        # get ndata and initial
        self.ndata = self.get_next_data(self.soup)
        self.idata, self.redux_state = self.get_initial_data_and_redux_state(
            self.ndata)

        # get ids
        self.zpid: str = self.idata['building']['zpid']
        self.lot_id: str = self.idata['building']['lotId']

        # if fresh data available, get fresh
        self.data = self.get_fresh_graphQL_data(self.lot_id)
        if not self.data:  # if empty dictionary fall back to initial data
            self.data = self.idata

        self.building: Dict[str, Any] = self.data['building']
        self.building_attributes: Dict[str,
                                       Any] = self.building['buildingAttributes']
        self.building_name: str = self.building['buildingName']

        self.description: str = self.building['description']
        self.low_income: bool = self.building['isLowIncome']
        self.senior_housing: bool = self.building['isSeniorHousing']
        self.student_housing: bool = self.building['isStudentHousing']

        self.office_hours: List[str] = self.building['amenityDetails']['hours']
        self.office_number: str = self.building['buildingPhoneNumber']

        self.key_features = self.get_key_features()
        self.unit_features: List[str] = self.building['amenityDetails']['unitFeatures']

        self.city: str = self.building['city']
        self.county: str = self.building['county']
        self.state: str = self.building['state']
        self.zip: str = self.building['zipcode']
        self.street_address: str = self.building['fullAddress']

        self.application_fee: Number | None = self.building_attributes['applicationFee']
        self.administrative_fee: Number | None = self.building_attributes['administrativeFee']
        self.deposit_fee_min: Number | None = self.building_attributes['depositFeeMin']
        self.deposit_fee_max: Number | None = self.building_attributes['depositFeeMax']
        self.lease_terms: List[str] = self.building_attributes.get(
            'leaseTerms', [])
        self.utilities_included: List[str] = self.building_attributes.get(
            'utilitiesIncluded', [])

        self.parking_policies: List[Dict[str, Any]
                                    ] = self.building_attributes['detailedParkingPolicies']
        self.parking_types: List[str] = self.building_attributes['parkingTypes']

        self.pet_policies: List[Dict[str, Any]
                                ] = self.building_attributes['detailedPetPolicy']

        self.shared_laundry: bool = self.building_attributes['hasSharedLaundry']
        self.air_conditioning: str = self.building_attributes['airConditioning']
        self.appliances: List[str] = self.building_attributes['appliances']
        self.outdoor_common_areas: List[str] = self.building_attributes['outdoorCommonAreas']
        self.barbecue: bool = self.building_attributes['hasBarbecue']
        self.heating_source: str = self.building_attributes['heatingSource']
        self.elevator: Any | None = self.building_attributes['hasElevator']
        self.community_rooms: List[str] = self.building_attributes['communityRooms']
        self.sports_courts: List[str] = self.building_attributes['sportsCourts']
        self.bicycle_storage: Any | None = self.building_attributes['hasBicycleStorage']
        self.guest_suite: Any | None = self.building_attributes['hasGuestSuite']
        self.storage: Any | None = self.building_attributes['hasStorage']
        self.pet_park: Any | None = self.building_attributes['hasPetPark']
        self.maintenance_24_7: Any | None = self.building_attributes[
            'hasTwentyFourHourMaintenance']
        self.dry_cleaning_drop_off: Any | None = self.building_attributes[
            'hasDryCleaningDropOff']
        self.online_rent_payment: Any | None = self.building_attributes['hasOnlineRentPayment']
        self.online_maintenance_portal: Any | None = self.building_attributes[
            'hasOnlineMaintenancePortal']
        self.onsite_management: bool = self.building_attributes['hasOnsiteManagement']
        self.package_service: Any | None = self.building_attributes['hasPackageService']
        self.valet_trash: Any | None = self.building_attributes['hasValetTrash']
        self.spanish_speaking_staff: Any | None = self.building_attributes[
            'hasSpanishSpeakingStaff']
        self.security_types: List[str] = self.building_attributes['securityTypes']
        self.view_types: List[str] = self.building_attributes['viewType']
        self.hot_tub: Any | None = self.building_attributes['hasHotTub']
        self.sauna: Any | None = self.building_attributes['hasSauna']
        self.swimming_pool: bool = self.building_attributes['hasSwimmingPool']
        self.assisted_living: bool = self.building_attributes['hasAssistedLiving']
        self.disabled_access: Any | None = self.building_attributes['hasDisabledAccess']
        self.floor_covering: List[str] = self.building_attributes['floorCoverings']
        self.communication_types: List[str] = self.building_attributes['communicationTypes']
        self.ceiling_fan: Any | None = self.building_attributes['hasCeilingFan']
        self.fire_place: Any | None = self.building_attributes['hasFireplace']
        self.patio_balcony: bool = self.building_attributes['hasPatioBalcony']
        self.furnished: Any | None = self.building_attributes['isFurnished']
        self.custom_ammenites: str = self.building_attributes['customAmenities']

        self.floorplans: List[Dict[str, Any]] = self.building['floorPlans']

        self.management: Dict[str, Any] = self.get_management_company(
            self.zpid).get('rentalListingOwnerContact', {})

        self.schools: List[Dict[str, Any]
                           ] = self.building.get('assignedSchools', [])
        self.nearby_cities: List[Dict[str, Any]
                                 ] = self.building.get('nearbyCities', [])
        self.nearby_neighborhoods: List[Dict[str, Any]
                                        ] = self.building.get('nearbyNeighborhoods', [])
        self.nearby_zip: List[Dict[str, Any]
                              ] = self.building.get('nearbyZipcodes', [])
        self.nearby_rental_buildings: List[Dict[str, Any]
                                           ] = self.building.get('nearbyBuildingLinks', [])
        self.nearby_amenities: List[Dict[str, Any]
                                    ] = self.building.get('nearbyAmenities', [])

        self.review_info: Dict[str, Any] = self.building.get('reviewsInfo', {})

    @staticmethod
    def get_fresh_graphQL_data(lot_id: str) -> Dict[str, str]:
        """Sends a GRAPHQL query to get the fresh data, as opposed to the initial data which may be stale or incomplete (for instance, lease terms are missing in initial data)

        Args:
            lot_id (str): The lot id

        Returns:
            Dict[str, str]: The data dictionary
        """

        url = "https://www.zillow.com/graphql"

        payload = {
            "operationName": "BuildingQuery",
            "variables": {
                "cache": False,
                "lotId": lot_id,
                "update": False},
            "queryId": "efbb40baf8ba7747347be4d8b170edc9"
        }

        return requests.request(
            "POST", url, json=payload, headers=defaults.GRAPHQL_HEADER
        ).json().get('data', {})

    def get_key_features(self) -> Dict[str, str]:
        """Gets the key features dictionary from the detail page.

        Returns:
            Dict[str, str]: Key features
        """
        return {
            t.title.text: t.span.text for t in self.soup.find(
                "div", id="bdp-building-facts-and-features"
            ).ul.find_all('li')
        }

    @staticmethod
    def get_management_company(zpid: str) -> Dict[str, Any]:
        """Gets the management details via a GRAPHQL query

        Args:
            zpid (str): The zillow ID

        Returns:
            Dict[str, Any]: The management details JSON
        """

        url = "https://www.zillow.com/graphql"

        payload = {
            "operationName": "ListingContactDetailsQuery",
            "variables": {"zpid": zpid},
            "query": r"query ListingContactDetailsQuery($zpid: ID!) {  viewer {    roles {      isLandlordLiaisonMember      isLlpRenter      __typename    }    __typename  }  property(zpid: $zpid) {    zpid    brokerId    isHousingConnector    isIncomeRestricted    rentalListingOwnerReputation {      responseRate      responseTimeMs      contactCount      applicationCount      isLandlordIdVerified      __typename    }    isFeatured    isListedByOwner    rentalListingOwnerContact {      displayName      businessName      phoneNumber      agentBadgeType      photoUrl      reviewsReceivedCount      reviewsUrl      ratingAverage      isBrokerLocalCompliance      __typename    }    postingProductType    postingContact {      brokerName      brokerageName      name      __typename    }    postingUrl    rentalMarketingTreatments    building {      bdpUrl      buildingName      housingConnector {        hcLink {          text          __typename        }        __typename      }      ppcLink {        text        __typename      }      __typename    }    __typename  }}"
        }

        return requests.request(
            "POST", url, json=payload, headers=defaults.GRAPHQL_HEADER,)\
            .json().get('data', {}).get('property', {})
