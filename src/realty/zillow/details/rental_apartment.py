# This handles parsing of rental apartments data
from typing import Dict, Any, List
from numbers import Number
from details_page import Details_Page


class Rental_Apartment(Details_Page):

    def __init__(self, url: str) -> None:
        """This initializes the Rental_Apartment object, which call a GET request on the Zillow detail URL. 

        Args:
            url (str): The Zillow Rental Apartments details URL.
        """

        self.url = url

        # get soup
        self.soup = self.make_soup(self.get_page(self.url))

        # get ndata and initial
        self.ndata = self.get_next_data(self.soup)
        self.data, self.redux_state = self.get_initial_data_and_redux_state(
            self.ndata)

        self.building: Dict[str, Any] = self.data['building']
        self.building_attributes: Dict[str,
                                       Any] = self.building['buildingAttributes']
        self.building_name: str = self.building['buildingName']

        self.zpid: str = self.building['zpid']
        self.description: str = self.building['desciption']
        self.low_income: bool = self.building['isLowIncome']
        self.senior_housing: bool = self.building['isSeniorHousing']
        self.student_housing: bool = self.building['isStudentHousing']

        self.office_hours: List[str] = self.building['amenityDetails']['hours']
        self.office_number: str = self.building['buildingPhoneNumber']

        self.unit_features: List[str] = self.building['amenityDetails']['unitFeatures']

        self.city: str = self.building['city']
        self.county: str = self.building['county']
        self.state: str = self.building['state']
        self.zip: str = self.building['zipcode']
        self.street_address: str = self.building['fullAddress']

        self.application_fee: Number | None = self.building_attributes['applicationFee']
        self.administrative_fee: Number | None = self.building_attributes['administrativeFee']
        self.deposite_fee_min: Number | None = self.building_attributes['depositFeeMin']
        self.deposite_fee_max: Number | None = self.building_attributes['depositFeeMax']

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

        self.floorplans: List[Dict[str, Any]] = self.building['floorplans']
