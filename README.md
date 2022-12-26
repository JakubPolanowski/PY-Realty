# PY-Realty

This is a library designed to scrape publicly available Real Estate listing information. 

Specifically, all this library does is send the bare minimum/near bare minimum requests to the public web servers of supported listing websites. Meaning that is is effectively the same as visiting the website (such as Zillow) manually with a web browser with the exception that with `PY-Realty` you can avoid loading unnecessary JavaScript and media (images, etc.). 

That being said scrapping large number of listings with no delays may result in the source (Zillow, Realtor.com, etc.) blocking your IP address (Zillow can probably figure out you're not manually looking at listings if you're querying thousands a minute.), although this has not been tested.

## Status

Early development. The library is still in early development and is missing key features and may not working entirely as expected.

## Road Map

- [ ] Zillow
  - [ ] Zillow Search Query
    - [x] Implementation
    - [x] Manual Testing
    - [x] Unit Testing
  - [ ] Zillow Listing Details Parsing
    - [x] Property Sale Listing
      - [x] Implementation
      - [x] Manual Testing
      - [ ] Unit Testing
    - [x] Property Rental Listing
      - [x] Implementation
      - [x] Manual Testing
      - [ ] Unit Testing
    - [ ] Apartment Rental Listing
      - [ ] Implementation
        * Partial Implementation with some key details missing
      - [ ] Manual Testing
      - [ ] Unit Testing
- [ ] Realtor.com
  - [ ] Realtor.com Search Query
      - [ ] Implementation
      - [ ] Manual Testing
      - [ ] Unit Testing
    - [ ] Realtor.com Listing Details Parsing
      - [ ] Property Sale Listing
      - [ ] Implementation
      - [ ] Manual Testing
      - [ ] Unit Testing
    - [ ] Property Rental Listing
      - [ ] Implementation
      - [ ] Manual Testing
      - [ ] Unit Testing
    - [ ] Apartment Rental Listing
      - [ ] Implementation
      - [ ] Manual Testing
      - [ ] Unit Testing
- [ ] LandWatch
  - [ ] LandWatch search Query
    - [ ] Implementation
    - [ ] Manual Testing
    - [ ] Unit Testing
  - [ ] LandWatch Listing Details Parsing
    - [ ] Implementation
    - [ ] Manual Testing
    - [ ] Unit Testing
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

Therefore Unit tests will check against unexpected behavior as opposed to extraction correctness. This meaning that they will check against exceptions and check if value types are correct.

## Usage

More detailed documentation will follow as development continues. However attributes and functions are well documented withing class and function doc-strings. 

Currently only Zillow scraping in implemented. 

Check back soon for more information.

### Zillow

Inside `zillow` the `Query` class is used to construct and send query request to Zillow's public API. Once the `Query` is configured as desired, the `get_response` method will return the search results.

The search results can then be scraped via the functions `details.crapes_listing` , `details.scrape_listings`, and `details.lazy_scrape_listings`.

## Installation

Installation and package setup currently not implemented 