import time
import os
import csv
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

os.environ['MOZ_HEADLESS'] = '1'

driver = webdriver.Firefox()
search = input("Enter url to search listings from: ")
driver.get(search)

urls = []
next = None

listingData = []
listingData.append(["Street", "City", "State", "Zipcode", "Unit", "Rent", "SqFt", "Bedrooms", "Bathrooms", "Available"])



while True:
    time.sleep(3)
    elems = driver.find_elements(By.CSS_SELECTOR, "a.property-link[href]")

    for listing in elems:
        url = listing.get_attribute("href")
        if url and url not in urls:
            urls.append(url)
            print("Found", url)

    try:
        next = driver.find_element(By.CLASS_NAME, "next")
    except Exception:
        break

    next.click()


print("Found", len(urls), "listings")
driver.quit()

listingDriver = webdriver.Firefox()


for link in urls:
    print(link)
    listingDriver.get(link)

    try:
        showUnavailable = listingDriver.find_element(By.CSS_SELECTOR, "button.js-showUnavailableFloorPlansButton")
        showUnavailable.click()
    except Exception:
        pass

    # Address
    address = listingDriver.find_element(By.CLASS_NAME, "propertyAddressContainer").text

    parts = address.split("\n")
    addressParts = [p.strip() for p in parts if p.strip() != "Property Website"]
    address = ' '.join(addressParts)

    addressParts = address.strip().split(",")

    if len(addressParts) > 3:
        continue

    streetParts = addressParts[0].strip().split("Unit")
    street = streetParts[0].strip()

    city = addressParts[1].strip()

    stateZip = addressParts[2].strip().split(" ")

    state = stateZip[0].strip()
    zipcode = stateZip[1].strip()



    # Check if several units or single property
    isSeveralListings = None
    unitBar = None

    try: 
        unitBar = listingDriver.find_element(By.CSS_SELECTOR, "div#pricingView")
    except Exception:
        pass

    if unitBar:
        isSeveralListings = 1
    else:
        isSeveralListings = 0


    # Units 
    if isSeveralListings == 1:
        
        section = listingDriver.find_element(By.CSS_SELECTOR, "div.tab-section.active")
        categoryContainers = section.find_elements(By.CSS_SELECTOR, "div.pricingGridItem.multiFamily.hasUnitGrid.v3.UnitLevel_var2")
        

        for container in categoryContainers:
            unitContainer = container.find_elements(By.CSS_SELECTOR, "li.unitContainer.js-unitContainerV3")

            details = container.find_element(By.CSS_SELECTOR, "span.detailsTextWrapper").text
            detailParts = details.split("\n")

            for unit in unitContainer:

                # Unit Number
                unitNum = unit.find_element(By.CSS_SELECTOR, "div.unitColumn.column span:not(.screenReaderOnly)").text.strip()

                # Rent Cost
                rent = unit.find_element(By.CSS_SELECTOR, "div.pricingColumn.column span:not(.screenReaderOnly)").text.strip()
                rent = rent.replace("$", "")
                rent = rent.replace(",", "")
                try:
                    rent = int(rent)
                except ValueError:
                    rent = None
                
                # SqFt
                sqft = unit.find_element(By.CSS_SELECTOR, "div.sqftColumn.column span:not(.screenReaderOnly)").text.strip()
                sqft = sqft.replace(",", "")
                try:
                    sqft = int(sqft)
                except ValueError:
                    sqft = None

                # Bedrooms
                bedrooms = detailParts[0].strip()
                if bedrooms == "Studio":
                    bedrooms = 0
                else:
                    bedroomSplit = bedrooms.split(" ")
                    try:
                        bedrooms = float(bedroomSplit[0])
                    except ValueError:
                        bedrooms = None

                # Bathroom
                bathrooms = detailParts[1].strip()
                bathroomSplit = bathrooms.split(" ")
                try:
                    bathrooms = float(bathroomSplit[0])
                except ValueError:
                    bathrooms = None
                
                
                # Available to Rent
                available = unit.find_element(By.CSS_SELECTOR, "div.availableColumn.column span:not(.screenReaderOnly)").text.strip()
                if available.lower == "now" or available.lower == "available now":
                    available = 1
                else:
                    available = 0

                # Append to data array
                singleListing = [street, city, state, zipcode, unitNum, rent, sqft, bedrooms, bathrooms, available]
                if not singleListing[4] and not singleListing[5] and not singleListing[6]:
                    continue
                if singleListing not in listingData:
                    listingData.append(singleListing)



    # Individual Houses
    elif isSeveralListings == 0:

        # Check if contains unit number
        try:
            unitNum = streetParts[1].strip()
        except Exception:
            pass

        # Rent Cost
        rentContainer  = listingDriver.find_element(By.CSS_SELECTOR, "div#propertyNameRow.propertyNameRow")
        rentText = rentContainer.text

        unwantedText = rentContainer.find_element(By.CSS_SELECTOR, "span.display-name-caption").text
        rentText = rentText.replace(unwantedText, "").strip()

        rentText = rentText.replace("$", "")
        rentText = rentText.replace(",", "")
        try:
            rent = int(rentText)
        except ValueError:
            rent = None

        details = listingDriver.find_element(By.CSS_SELECTOR, "div.priceBedRangeInfoContainer")

        detailParts = details.find_elements(By.CSS_SELECTOR, "li.column")

        for section in detailParts:
            if section.find_element(By.CSS_SELECTOR, "p.rentInfoLabel").text == "Square Feet":
                sqftText = section.find_element(By.CSS_SELECTOR, "p.rentInfoDetail").text.strip()
            if section.find_element(By.CSS_SELECTOR, "p.rentInfoLabel").text == "Bedrooms":
                bedrooms = section.find_element(By.CSS_SELECTOR, "p.rentInfoDetail").text.strip()
            if section.find_element(By.CSS_SELECTOR, "p.rentInfoLabel").text == "Bathrooms":
                bathrooms = section.find_element(By.CSS_SELECTOR, "p.rentInfoDetail").text.strip()
            if section.find_element(By.CSS_SELECTOR, "p.rentInfoLabel").text == "Available":
                available = section.find_element(By.CSS_SELECTOR, "p.rentInfoDetail").text.strip()


        # SqFt
        sqftText = sqftText.replace(",", "")
        sqftParts = sqftText.split(" ")
        try:
            sqft = int(sqftParts[0])
        except ValueError:
            sqft = None

        # Bedrooms
        try:
            bedrooms = float(bedrooms)
        except ValueError:
            bedrooms = None

        # Bathrooms
        try:
            bathrooms = float(bathrooms)
        except ValueError:
            bathrooms = None

        # Available to Rent
        if available.lower == "now" or available.lower == "available now":
            available = 1
        else:
            available = 0

        #Append to data array 
        singleListing = [street, city, state, zipcode, unitNum, rent, sqft, bedrooms, bathrooms, available]
        if not singleListing[4] and not singleListing[5] and not singleListing[6]:
            continue
        if singleListing not in listingData:
            listingData.append(singleListing)


listingDriver.quit()

print("Finished with scraping")

while True:
    pathText = input("Enter the path of the destination file: ")

    if pathText.endswith(".csv"):
        break
    else:
        print("File destination does not end with .csv \n Retrying...")


fileName = Path(pathText)
fileName.parent.mkdir(parents=True, exist_ok=True)

with fileName.open("w", newline="", encoding="utf-8") as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(listingData)

print("Finished writing to CSV file")