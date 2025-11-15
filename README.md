# MainePad-Finder

MainePad-Finder is a housing search application designed for Maine University students.  
This repo contains the MySQL schema, stored procedures, functions, example queries used to power the backend database and web scraping.

## Table of Contents
### [Phase 2](https://github.com/TheHylianLegend/MainePad-Finder/tree/31b1e6cc412722f1852190fb40a6aed6102b8990/Phase2)
- [Database Operations](https://github.com/TheHylianLegend/MainePadFinder/tree/31b1e6cc412722f1852190fb40a6aed6102b8990/Phase2/Database%20Operations) 
- [Functions](https://github.com/TheHylianLegend/MainePad-Finder/tree/262c45c812d33b4845b1f611651738d45e087525/Phase2/Functions)
- [Procedures](https://github.com/TheHylianLegend/MainePad-Finder/tree/262c45c812d33b4845b1f611651738d45e087525/Phase2/Procedures)
- [Queries](https://github.com/TheHylianLegend/MainePad-Finder/tree/983ab3f3532497a4c049ce1b2e8e112aa9aff0fc/Phase2/Queries)
- [Schema](https://github.com/TheHylianLegend/MainePad-Finder/tree/d2591ae08ed2a89a19d25773ed49a6cad05f5191/Phase2/Schema)
- [Web Scrapping](https://github.com/TheHylianLegend/MainePad-Finder/tree/48905f4f5baf0d539872c8325e53fd940f5e15be/Phase2/Web%20Scraping)
### [Running MySQL Files](#running-mysql-files)
### [Web Scraping Scripts](https://github.com/TheHylianLegend/MainePad-Finder/blob/main/README.md#web-scraping-scripts-1)
### [Query Optimization & Indexing](https://github.com/TheHylianLegend/MainePad-Finder/blob/main/README.md#query-optimization--indexing-1)
## Running MySQL Files

### Overview
Create database using designated MySQL files from "Database Operations", "Procedures" and "Functions" folders. Verify your database is functioning accordingly by using an example query from the "Queries" folder. 

### Installation and Requirements 
- [MySQL Community Server](https://dev.mysql.com/downloads/mysql/8.0.html) installed 
- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/)
- A MySQL account that allows you to create databases and tables 

### How To Run MySQL Workbench
1. Open **MySQL Workbench** and connect to your local server 
2. For every schema in the schema folder, go to **File -> Open SQL Script**
3. Select each file in the **Files Order** and upload 
4. Click the lightning bolt to execute and follow **Files Order**
5. Repeat this process for procedures and functions
6. To verify the database is running correctly, upload and run queries from the "queries" file

### Files Order
1. **Database Operations**
```sql
- Create_DATABASE.SQL
- ALL_TABLE.sql
- ADD_INDEXES.sql
```
2. **Procedure and Function Files**
```sql
- ADD_PROPERTY.sql
- INSERT_MATCH.sql
- INSERT_USER.sql
- SEND_MESSAGE.sql
- SEND_NOTIFICATION.sql
- SUBMIT_REVIEW.sql
- GET_AVG_RATING.sql
```
3. **Query Files**
```sql
- FIND_PROPS_BELOW_RENT_AMT.sql
- FIND_TOP_RATED_PROPS_IN_CITY.sql
```

## Web Scraping Scripts

### Overview

Several Python-based web scraping scripts have been designed in order to populate the _MainePad Finder_ application with pertinent real-world address and property data. `apartment_finder.py` (designed by Sophia Priola and Ashley Pike) retrieves property information from Apartments.com, while `Fosgate_ZillowScraper.py` (designed by Jeffrey Fosgate and Yunlong Li) retrieves property information from Zillow. Property and address information shall be returned in a comma-separated variable (CSV) format. See _Web Scraper Documentation_ files (mentioned below) for additional details on each individual web scraper design.

### Files

All files pertaining to _MainePad Finder_ web scraping functionalities can be found within the directory `MainePad-Finder/Phase2/Web Scraping`. The files contained within this directory are further differentiated below.

#### Web Scraping Scripts

There are two Python scripts included which provide the primary web scraping functionality needed for retrieving real-world sample address and property data. These scripts include:

```
- apartment_finder.py
- Fosgate_ZillowScraper.py
```

#### Sample Data

Several CSV files have already been provided, showcasing some sample data retrieved during tests of the web scraper conducted by the _MainePad Finder_ development team. This sample data is provided by:

```
- apartments-properties.csv
- zillow-properties.csv
```

`apartments-properties.csv` provides the output received from `apartment_finder.py` (Apartments.com), while `zillow-properties.csv` provides the output received from `Fosgate_ZillowScraper.py` (Zillow).

#### Web Scraper Documentation

Documentation has been provided to further elaborate upon the design of each web scraper and the steps taken to sanitize the data retrieved. This documentation is provided by:

```
- Data_Scraping_Documentation__Zillow.pdf
- Web_Scraping_Documentation_Apartments.com.pdf
- Data_Cleaning_Documentation_Apartments.com.pdf
```

### Running Web Scraping Scripts

#### Installations and Requirements

**[An installation of Python](https://www.python.org/downloads/)** is required for running both web scraping scripts. **A release of Python at or above release version 3.5 is highly recommended** for supporting all libraries used within the scripts.

Once Python has been installed on your system, the following Python utility and library downloads will be required. Commands for installation provided here are assumed to be executed within your Python version's current directory.

- **`pip`**: `python get-pip.py`
- **`BeautifulSoup4`**: `python -m pip install bs4`
- **`Selenium`**: `python -m pip install selenium`

#### Script Execution

Both web scraping files can be executed identically to any other basic Python file. Assuming that your Python version and your web scraper of choice are located within the same directory, this can be done with the commands

```python
python Fosgate_ZillowScraper.py
python apartment_finder.py
```

See the respective documentation provided for both web scrapers for additional information on the precise directory and format in which the resulting property output will be provided.

## Query Optimization & Indexing 
This section analyzes how we improved the performance of key MainePad-Finder queries by:

### Query 1: Top Rated Properties In A City 
**Goal of query:** For a given city (e.g., Portland), find all properties in that city and sort them by their average review stars, highest first.

**Tables involved:**
```sql
- ADDRESS.sql
- PROPERTY.sql
-REVIEW.sql
```


