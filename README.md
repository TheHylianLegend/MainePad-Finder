# MainePad-Finder

## Table of Contents
### [Phase 2](https://github.com/TheHylianLegend/MainePad-Finder/tree/31b1e6cc412722f1852190fb40a6aed6102b8990/Phase2)
- [Database Operations](https://github.com/TheHylianLegend/MainePad-Finder/tree/31b1e6cc412722f1852190fb40a6aed6102b8990/Phase2/Database%20Operations) 
- [Functions](https://github.com/TheHylianLegend/MainePad-Finder/tree/262c45c812d33b4845b1f611651738d45e087525/Phase2/Functions)
- [Procedures](https://github.com/TheHylianLegend/MainePad-Finder/tree/262c45c812d33b4845b1f611651738d45e087525/Phase2/Procedures)
- [Queries](https://github.com/TheHylianLegend/MainePad-Finder/tree/983ab3f3532497a4c049ce1b2e8e112aa9aff0fc/Phase2/Queries)
- [Schema](https://github.com/TheHylianLegend/MainePad-Finder/tree/d2591ae08ed2a89a19d25773ed49a6cad05f5191/Phase2/Schema)
- [Web Scrapping](https://github.com/TheHylianLegend/MainePad-Finder/tree/48905f4f5baf0d539872c8325e53fd940f5e15be/Phase2/Web%20Scraping)

## Running MySQL Files

### Overview
Create database using designated MySQL files from "Functions", "Procedures" and "Schema" folders. 

### Installation and Requirements 
- [MySQL Community Server](https://dev.mysql.com/downloads/mysql/8.0.html) installed 
- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/)
- A MySQL account that allows you to create databases and tables 

### Schema Files
```sql
- ADDRESS.sql
- HAS_PREFERENCE.sql
- LANDLORD.sql
- MESSAGE.sql
- NOTIFICATION.sql
- NOTIFIES.sql
- PROPERTY.sql
- RENTER.sql
- RENTER_MATCH.sql
- RENTER_PREFERENCES.sql
- RENTER_SETTINGS.sql
- REVIEW.sql
- USERS.sql
```
### Procedure and Function Files 
```sql
- ADD_PROPERTY.sql
- INSERT_MATCH.sql
- INSERT_USER.sql
- SEND_MESSAGE.sql
- SEND_NOTIFICATION.sql
- SUBMIT_REVIEW.sql
- GET_AVG_RATING.sql
```
### Query Files 

### How To Run MySQL Workbench
1. Open **MySQL Workbench** and connect to your local server 
2. Create a database:
   ```sql
   CREATE DATABASE maine_pad_finder:
   USE maine_pad_finder;
   ```
3. For every schema in the schema folder, go to **File -> Open SQL Script**
4. Select each file and upload
5. 
