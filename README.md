# PY-Realty

This is a library designed to scrape publicly available Real Estate listing information. 

Specifically, all this library does is send the bare minimum/near bare minimum requests to the public web servers of supported listing websites. Meaning that is is effectively the same as visiting the website (such as Zillow) manually with a web browser with the exception that with `PY-Realty` you can avoid loading unnecessary JavaScript and media (images, etc.). 

That being said scrapping large number of listings with no delays may result in the source (Zillow, Realtor.com, etc.) blocking your IP address (Zillow can probably figure out you're not manually looking at listings if you're querying thousands a minute.), although this has not been tested.

## Status

**VERSION:** 0.1.0

Early development. The library is still in early development and is missing key features and may not be working entirely as expected.

This library is now somewhat usable (mileage may vary) and can be installed (and built) via pip, see installation instructions below.

## Road Map

- [x] Zillow
  - [x] Zillow Search Query
    - [x] Implementation
    - [x] Manual Testing
    - [x] Unit Testing
  - [x] Zillow Listing Details Parsing
    - [x] Property Sale Listing
      - [x] Implementation
      - [x] Manual Testing
      - [x] Unit Testing
    - [x] Property Rental Listing
      - [x] Implementation
      - [x] Manual Testing
      - [x] Unit Testing
    - [x] Apartment Rental Listing
      - [x] Implementation
      - [x] Manual Testing
      - [x] Unit Testing
- [ ] Realtor.com
  - [x] Realtor.com Sale Search Query
      - [x] Implementation
      - [x] Manual Testing
      - [x] Unit Testing
  - [ ] Realtor.com Rental Search Query
      - [ ] Implementation
      - [ ] Manual Testing
      - [ ] Unit Testing
  - [x] Property Sale Listing
    - [x] Implementation
    - [x] Manual Testing
    - [x] Unit Testing
  - [ ] Property Rental Listing
    - [ ] Implementation
    - [ ] Manual Testing
    - [ ] Unit Testing
- [x] LandWatch
  - [x] LandWatch search Query
    - [x] Implementation
    - [x] Manual Testing
    - [x] Unit Testing
  - [x] LandWatch Listing Details Parsing
    - [x] Implementation
    - [x] Manual Testing
    - [x] Unit Testing
- [ ] Apartments.com
  - [ ] Apartments.com Search Query 
    - [ ] Implementation
    - [ ] Manual Testing
    - [ ] Unit Testing
  - [ ] Apartments.com Listing Details Parsing
    - [ ] Implementation
    - [ ] Manual Testing
    - [ ] Unit Testing

### Regarding Unit Tests

Due to the nature of the data, it is impractical to have Unit tests check if data is extracted correctly. If testing against a source of Truth, say a listing, that listing may change over time. Additionally even though Zillow and Realtor.com may have similar data, if there is a mismatch it does not necessarily mean that scraping is done incorrectly, could just be a mismatch between the two websites. 

Therefore Unit tests will check against unexpected behavior as opposed to extraction correctness. This meaning that they will check against exceptions and check if value types are correct. That being said the Unit Test criteria still needs to ensure reasonable robustness. 

## Usage

More detailed documentation will follow as development continues. However attributes and functions are well documented withing class and function doc-strings. 

### Zillow

Inside `zillow` the `Query` class is used to construct and send query request to Zillow's public API. Once the `Query` is configured as desired, the `get_response` method will return the search results.

The search results can then be scraped via the functions `details.crapes_listing` , `details.scrape_listings`, and `details.lazy_scrape_listings`.

## Installation

1. Clone this repository 
2. Within the repository folder, run `pip install .`