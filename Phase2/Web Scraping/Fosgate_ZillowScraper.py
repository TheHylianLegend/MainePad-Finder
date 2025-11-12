# NAME: Fosgate_ZillowScraper.py
# DATE COMMITTED: November 12, 2025
# DESCRIPTION: A simple web scraper that retrieves necessary data for several Zillow-listed rental apartments and properties in Maine.

### PROBLEMS ###
# * Some data is not completely sanitized; some trailing spaces are evident in some component of addresses, for instance.
# * This takes a while to completely finish -- above five minutes to generate ~300+ property listings.
# * "ADDR" needs to be broken down into "STREET", "CITY" and "ZIPCODE" in future uses of the data this generates.
# * There isn't much for outright error detection here; just ways to prevent errors from occurring in the first place.

# The heavy lifters for the actual web scraping.
from bs4 import BeautifulSoup
import requests

# For writing .CSV files and constructing their directories.
import os
import csv

# For identifying HTML tags with properties best represented as regular expressions.
import re

# Used to make it more convenient to translate information about a larger apartment complex to all of its individual units.
from copy import deepcopy

# These are all the fields that ZillowScraper retrieves. Many of them correspond with their listings on the MainePad Finder SQL schemas.
# "NAME" (string) is added just to make the properties more identifiable.
FIELDS_NEEDED = ["NAME","ADDR","RENT_COST","BEDROOMS","BATHROOMS","APT_NUM","SQFT"]

# These headers are configured for Firefox and included to bypass any bot detection present on Zillow.
# If this program doesn't work, try changing this information to reflect a different web browser.
# These specific headers were retrieved from GeeksForGeeks: see https://www.geeksforgeeks.org/python/implementing-web-scraping-python-beautiful-soup/
bs_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def GetPropDetails(prop_info): # A function used for finding pertinent details of individual properties (i.e., not part of a larger apartment complex)

    prop_dict = {}
    prop_dict["APT_NUM"] = "0" # Individual properties don't have apartment numbers; set this as "0".
    # Why is "APT_NUM" a string and not a number? Some apartment numnbers on Zillow are alphanumeric
    # and cannot be easily represented by a single number (i.e., 'N102', '105-T').

    # Address information for individual properties is typically represented within a single "AddressWrapper" of some sort.
    addr_text = prop_info.find("div",attrs={"class":re.compile("AddressWrapper")}).find("h1").get_text().split(",")
    # Strip the "ME" abbreviation from the ZIP code portion of addresses (because all of these properties are within Maine)
    # and remove the "non-breaking space" ('\xa0') character used by Zillow to represent these addresses.
    address = [addr_field.strip("\xa0").removeprefix(" ME ") for addr_field in addr_text]

    # The convention is used here that properties are named in accordance with the street name portion of their respective addresses,
    # assuming no unique name exists for the unit's building.
    prop_dict["ADDR"] = address
    prop_dict["NAME"] = address[0]

    # The process for retrieving the information here are designed similarly to how the process for apartment complexes is designed.
    # See my commentary below this method for more details on how all of this works.
    rent_cost_text = prop_info.find("span",attrs={"data-testid":"price"}).get_text()
    rent_cost = int(re.sub(r"\D", "", rent_cost_text))
    prop_dict["RENT_COST"] = rent_cost

    bed_bath_sqft_facts = prop_info.find("div", attrs={"data-testid":"bed-bath-sqft-facts"})
    for fact in bed_bath_sqft_facts.children:
        fact_text = fact.find_all("span",attrs={"class":re.compile("Text")})
        if len(fact_text) == 2:
            if fact_text[1].get_text() == "beds":
                bedrooms_text = re.sub(r"\D.", "", fact_text[0].get_text())
                if not (bedrooms_text == ""):
                    prop_dict["BEDROOMS"] = float(bedrooms_text)
                else:
                    prop_dict["BEDROOMS"] = 0.0
            elif fact_text[1].get_text() == "baths":
                bathrooms_text = re.sub(r"\D.", "", fact_text[0].get_text())
                if not (bathrooms_text == ""):
                    prop_dict["BATHROOMS"] = float(bathrooms_text)
                else:
                    prop_dict["BATHROOMS"] = 0.0
            else:
                sqft_text = re.sub(r"\D", "", fact_text[0].get_text())
                if not (sqft_text == ""):
                    prop_dict["SQFT"] = int(sqft_text)
                else:
                    prop_dict["SQFT"] = 0

        for dict_field in ["BEDROOMS","BATHROOMS","SQFT","RENT_COST"]:
            if dict_field not in unit_dict.keys():
                unit_dict[dict_field] = 0

    return prop_dict

### MAIN PROGRAM ###

scraping_finished = False
pagenum = 1

# A list of properties that will eventually be translated into rows within a .CSV file.
properties = []

print("Retrieving property data...")

while not scraping_finished:

    zillow_url = f"https://www.zillow.com/me/rentals/{pagenum}_p" # Header format for retrieving page (pagenum) of available Maine rentals.
    zillow_requests_response = requests.get(zillow_url, headers = bs_headers)

    # Retrieve the search results for page (pagenum).
    zillow_bs_searchresults = BeautifulSoup(zillow_requests_response.text, 'html.parser').find("div",attrs={"id":"search-page-list-container"})

    if zillow_bs_searchresults is None: # If there are no results in page (pagenum)... / if page (pagenum) is empty...
        scraping_finished = True # We've passed the final page of search results; we're done scraping through Zillow.
        break

    # On Zillow, search results all have individual links included within "property cards".
    # This list generator retrieves all the links within all property cards that can be found within this page.
    prop_links = ["https://www.zillow.com/" + prop_a_tag["href"].removeprefix("https://www.zillow.com").removeprefix("/") for prop_a_tag in zillow_bs_searchresults.find_all("a",attrs={"data-test":"property-card-link"})]
    
    for prop_link in prop_links:

        # Each property's information is collected within a dictionary unique to it, and appended to the end of the aforementioned 'properties' list.
        # This makes it more convenient to work with the property data while using 'csv'.
        prop_dict = {}
        prop_response = requests.get(prop_link, headers = bs_headers)

        # Retrieve the information for this specific found property.
        # Information for specific properties (once clicked on) are stored within a "layout content container", necessitating this specific 'find' statement.
        prop_info = BeautifulSoup(prop_response.text, 'html.parser').find("div",attrs={"class":"layout-content-container"})

        if prop_info is not None: # If this property has some information available about it... / if a "layout-content-container" exists for this property...

            # Find "bdp-building-units-table". This table contains all of the units within a rental property.
            unit_table = prop_info.find("div",attrs={"id":"bdp-building-units-table"})

            # If there are NO smaller rental units associated with this single property...
            if unit_table is None:

                #print("This is a house!")

                # ... then it must be an individual rental property.
                properties.append(GetPropDetails(prop_info))

            # If there ARE smaller rental units associated with this single property...
            else:

                #print("This is an apartment complex!")

                # ... then it must be an apartment complex of some kind.
            
                # Most apartment complexes have specific names which differ from their addresses. This .find() statement attempts to retrieve that name.
                title_tag = prop_info.find("h1",attrs={"data-test-id":"bdp-building-title"})
                name = title_tag.get_text().strip(" ")
                prop_dict["NAME"] = name

                # There are two interfaces used on Zillow for tabularizing all of the rental units affiliated with a single larger building.
                # One interface contains all relevant units within individual "unit cards", similarly to what is done for property search results.
                # The other uses a simpler table that displays all of the property information up-front and does not use unit cards.
                # "unit_card_container" contains all of the unit rental cards that can be found in this property listing.
                unit_card_container = prop_info.find("div",attrs={"data-test-id":"building-units-card-groups-container-for-rent"})

                # If some unit cards could be found / if units are represented using unit cards...
                if unit_card_container is not None:

                    # Perform a similar process to what was done above for retrieving property links.
                    # Each of these units have a link associated with them that provides detailed info about each rental unit.
                    unit_cards = unit_card_container.find_all("a",attrs={"class":"unit-card-link"})

                    addr_text = prop_info.find(attrs={"data-test-id":"bdp-building-address"}).get_text().split(",")
                    address = [addr_field.strip("\xa0").removeprefix(" ME ") for addr_field in addr_text]

                    # Some addresses within these unit cards are split between two headers; others are included within a single title.
                    # If the address is split between two headers, alter the address accordingly...
                    # ...otherwise, leave it alone.
                    if len(address) == 2:
                        prop_dict["ADDR"] = [prop_dict["NAME"], address[0], address[1]]
                    elif len(address) == 3:
                        prop_dict["ADDR"] = address

                    unit_links = ["https://www.zillow.com/" + unit_card["href"].removeprefix("https://www.zillow.com").removeprefix("/") for unit_card in unit_cards]
                    unit_cnt = 1

                    for unit_link in unit_links:

                        # Why is this done? Because information taken about a larger property (namely, "ADDR") is also descriptive of its rental units.
                        # A DEEP copy is needed to ensure that altering a single unit's dictionary does not inadvertently alter the larger property's dictionary.
                        unit_dict = deepcopy(prop_dict)

                        # A convention of "NAME" = <prop_name> (<unit_cnt>) is used for apartment complexes to differentiate rental units from each other, name-wise.
                        unit_dict["NAME"] = prop_dict["NAME"] + f" ({unit_cnt})"
                        unit_cnt += 1
                        
                        # Get the information for this specific unit.
                        unit_response = requests.get(unit_link, headers = bs_headers)
                        unit_info = BeautifulSoup(unit_response.text, 'html.parser').find("div",attrs={"class":"layout-content-container"})

                        # Addresses of units are usually represented using the street of its larger property, following by an apartment or room number for that unit.
                        # These apartment and room numbers are invariably displayed in the form of, for example, "123 John Doe St. #1" OR "123 John Doe. St. APT 1"
                        # These lines find this address line and distill the apartment number of the unit from it, assuming this format holds for every property.
                        unit_address = unit_info.find("div",attrs={"class":re.compile("AddressWrapper")}).find("h1").get_text()
                        if "#" not in unit_address and "APT " not in unit_address:
                            unit_dict["APT_NUM"] = "0"
                        else:
                            apt_num = "0"
                            if "#" in unit_address:
                                apt_num = unit_address[unit_address.index("#")+1:unit_address.index(",")]
                            else:
                                apt_num = unit_address[unit_address.index("APT")+4:unit_address.index(",")]
                            unit_dict["APT_NUM"] = apt_num


                        rent_cost_text = unit_info.find("span",attrs={"data-testid":"price"}).find().get_text()
                        # In 're', the '\D' special character denotes all individual digit characters ('0', '1', ...).
                        # re.sub() provides a string in which all characters from an original string which do not satisfy the regex provided are removed.
                        # Thus, the below statement removes all non-digit characters from the string retrieved for the rent cost (per month).
                        # These regex statements are very useful for "RENT_COST", "SQFT", "BEDROOMS" and "BATHROOMS".
                        rent_cost = int(re.sub(r"\D", "", rent_cost_text))
                        unit_dict["RENT_COST"] = rent_cost

                        # When a unit is represented within a unit card, its bedroom, bathroom and square footage information are all
                        # represented within a single 'bed-bath-sqft-facts' division tag.
                        # These statements examine this tag within a unit card and extract all pertinent unit information from it.
                        bed_bath_sqft_facts = unit_info.find("div", attrs={"data-testid":"bed-bath-sqft-facts"})
                        
                        # Each individual piece of information is represented within its own 'bed-bath-sqft-fact-container'.
                        # For each piece of information found...
                        for fact in bed_bath_sqft_facts.find_all("div",attrs={"data-testid":"bed-bath-sqft-fact-container"}):

                            # Find all of the 'span' tags within which the information text is contained.
                            fact_text = fact.find_all("span",attrs={re.compile("Text")})

                            # If there are two tags in total -- one for the numerical value and one for the datum that number represented ('sqft', 'beds', 'baths')...
                            if len(fact_text) == 2:

                                # If this is referencing the unit's number of bedrooms...
                                if "beds" in fact_text[1].get_text():
                                    bedrooms_text = re.sub(r"\D", "", fact_text[0].get_text())
                                    if not (bedrooms_text == ""):
                                        unit_dict["BEDROOMS"] = float(bedrooms_text)
                                    else:
                                        unit_dict["BEDROOMS"] = 0.0

                                # If this is referencing the unit's number of bathrooms...
                                elif "baths" in fact_text[1].get_text():
                                    bathrooms_text = re.sub(r"\D", "", fact_text[0].get_text())
                                    if not (bathrooms_text == ""):
                                        unit_dict["BATHROOMS"] = float(bathrooms_text)
                                    else:
                                        unit_dict["BATHROOMS"] = 0.0

                                # If this is referencing the unit's square footage...
                                elif "sqft" in fact_text[1].get_text():
                                    sqft_text = re.sub(r"\D", "", fact_text[0].get_text())
                                    if not (sqft_text == ""):
                                        unit_dict["SQFT"] = int(sqft_text)
                                    else:
                                        unit_dict["SQFT"] = 0

                            # A final failsafe.
                            # If any of these numerical fields were not found at all after all this work, they'll be represented as "0".
                            for dict_field in ["BEDROOMS","BATHROOMS","SQFT","RENT_COST"]:
                                if dict_field not in unit_dict.keys():
                                    unit_dict[dict_field] = 0

                        # Add this unit to the list of properties found.
                        properties.append(unit_dict)

                # If no unit cards could be found / if this unit is represented by the simpler tabular interface...
                else:

                    # Most of the information pertaining to units represented in this format can be retrieved without finding a specific link for each unit.
                    # All of the following takes that approach to finding unit data.

                    addr_text = prop_info.find("h2",attrs={"data-test-id":"bdp-building-address"}).get_text().split(",")
                    address = [addr_field.strip("\xa0 ").removeprefix("ME ") for addr_field in addr_text]
                    prop_dict["ADDR"] = address

                    units_tablerows = unit_table.find("tbody",attrs={"data-testid":"unit-table-body"}).find_all("tr")
                    unit_cnt = 1

                    for unit_listing in units_tablerows:

                        default_aptnum = 1
                        unit_dict = deepcopy(prop_dict)
                        unit_dict["NAME"] = prop_dict["NAME"] + f" ({unit_cnt})"
                        unit_cnt += 1

                        unit_data = unit_listing.find_all("td")

                        # In this simpler table design, most Zillow units belonging to the same property are tabularized into a table with four headers (Apt. Num / Beds / Baths, Sq. Ft., Availability, Rent Cost).
                        # This statement checks if all four headers are actually present with no extras, and skips any that are not structured in this way. 
                        if len(unit_data) == 4:

                            num_beds_baths = [datum.get_text() for datum in unit_data[0].find_all("span")]
                            for datum in num_beds_baths:
                                if " ba" in datum or " bd" in datum:
                                    beds_baths = datum.split(", ")
                                    for beds_baths_datum in beds_baths:
                                        if " bd" in beds_baths_datum: 
                                            bedrooms = float(beds_baths_datum.removesuffix(" bd"))
                                            unit_dict["BEDROOMS"] = bedrooms
                                        elif " ba" in beds_baths_datum:
                                            bathrooms = float(beds_baths_datum.removesuffix(" ba"))
                                            unit_dict["BATHROOMS"] = bathrooms
                                else:
                                    # The first element of each unit row on the table contains two bits of information: a unit number, and the number of beds / baths that unit has.
                                    # The unit number is often purely numerical, but can sometimes be alphanumerical.
                                    # The same assumption is made here that if the text where the unit number is supposed to be is mostly (at least half) non-numerical (i.e., "Special offer..."),
                                    # it is probably referring to something other than the actual unit number. In those cases, the unit number is represented as "0".
                                    datum_wo_letters = re.sub(r"\D","",datum)
                                    if len(datum_wo_letters) < len(datum) / 2:
                                        unit_dict["APT_NUM"] = "0"
                                    else:
                                        unit_dict["APT_NUM"] = datum

                            sqft = re.sub(r"\D","",unit_data[1].find("div").get_text())
                            if not (sqft == ""):
                                unit_dict["SQFT"] = int(sqft)
                            else:
                                unit_dict["SQFT"] = 0

                            rent_cost = re.sub(r"\D","",unit_data[3].find("div").get_text())
                            if not (rent_cost == ""):
                                unit_dict["RENT_COST"] = int(rent_cost)
                            else:
                                unit_dict["RENT_COST"] = 0

                            for dict_field in ["BEDROOMS","BATHROOMS","SQFT","RENT_COST"]:
                                if dict_field not in unit_dict.keys():
                                    unit_dict[dict_field] = 0

                            properties.append(unit_dict)

    print(f"(Page {pagenum} complete)")

    # Flip to the next page.
    pagenum += 1

# A final failsafe to ensure no unwanted side effects in circumstances where a property does not contain every desired field.
# If a field is not found in a property, it will appear empty on the resulting .CSV.
# This makes it easier to deduce which entries are clearly incomplete.
for property in properties:
    for field in FIELDS_NEEDED:
        if field not in property.keys():
            property[field] = None

print("Property data retrieval complete! Writing property data to CSV...")

# The resulting .CSV will be created within the same directory that this file is located in when it is initiated.
with open(os.path.join(os.path.dirname(__file__), "zillow-properties.csv"), mode='w') as zillow_csv:
    writer = csv.DictWriter(zillow_csv, fieldnames = FIELDS_NEEDED)
    writer.writeheader()
    for property in properties:
        writer.writerow(property)
