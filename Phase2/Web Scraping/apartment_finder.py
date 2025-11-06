import time
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

os.environ['MOZ_HEADLESS'] = '1'

driver = webdriver.Firefox()
search = input("Enter url to search listings from: ")
driver.get(search)

urls = []
addresses = []
next = None



while True:
    time.sleep(3)
    elems = driver.find_elements(By.CSS_SELECTOR, "a.property-link[href]")

    for listing in elems:
        url = listing.get_attribute("href")
        if url and url not in urls:
            urls.append(url)
            print("Found", url)
            # Testing
            break
    try:
        next = driver.find_element(By.CLASS_NAME, "next")
    except Exception:
        break

    next.click()


print("Found", len(urls), "listings")
driver.quit()


for link in urls:
    listingDriver = webdriver.Firefox()
    listingDriver.get(link)

    # Address
    address = listingDriver.find_element(By.CLASS_NAME, "propertyAddressContainer").text

    parts = address.split("\n")
    addressParts = [p.strip() for p in parts if p.strip() != "Property Website"]
    cleanAddress = ' '.join(addressParts)


    


    # Units 

    # Apartment Number

    print(cleanAddress)

    # Rent Cost

    # Bathrooms

    # Bedrooms

    # Available to Rent



    # Individual Houses

    # Rent Cost

    # Bathrooms

    # Bedrooms

    # Available to Rent


    listingDriver.quit()


    
print(addresses)