# Query Optimization & Indexing 
This section analyzes how we improved the performance of key MainePad-Finder queries

## Indexing Choices
We created a small set of indexes to support the most common access patterns
in the MainePad-Finder application. Each index was chosen because the corresponding column is
either:
- Frequently used in `WHERE` filters,
- Used to look up a single user or subset of users, or
- Used to sort data by recency (e.g., newest notifications/ messages)

**Chosen Indecies:**
- ``IDX_USERNAME ON USERS(USERNAME);``

We expect the application to frequently look up a user by their username (e.g., login, profile lookup). Without this index, queries such as profile searches would require scanning the entire USERS table.
- ``INDEX IDX_EMAIL ON USERS(EMAIL)``

Similar to usernames, emails are often used for login and password recovery and must be unique. Using this as an index avoids doing a full table scan and making existence checks and lookups much faster.
- ``INDEX IDX_DISPLAY_NAME ON USERS(DISPLAY_NAME);``

Display names are used for searching. For example you can search for users whos display name starts with "Jeff". An index on DISPLAY_NAME allows MySQL to efficiently seek into the range of matching names instead of scanning every row.
- ``INDEX IDX_BIRTHDATE ON USERS(BIRTH_DATE);`` Some queries may filter users by age or birthdate range if it is a roomate preference.

Indexing BIRTH_DATE lets MySQL use a range scan on the date column, which is much more efficient than scanning all users when we need to select only a subset by birthdate.
- ``INDEX IDX_RENT ON PROPERTY(RENT_COST);``

Our application supports queries that filter properties by a maximum or minimum rent amount. Without an index, MySQL would need to scan every property to check its rent. The 'IDX_RENT' index allows MySQL to perform a scan based on a range on RENT_COST, reading only the relevant portion of the index instead of the entire table.
- ``INDEX IDX_NOTIFICATION_TIMESTAMP ON NOTIFICATION(TIME_STAMP);``

Indexing TIME_STAMP helps MySQL efficiently find the most recent notifications for a user without scanning all older rows, which is important as the amount of notifications grow.
- ``INDEX IDX_MESSAGE_TIMESTAMP ON MESSAGE(TIME_STAMP);``

Such as the previous index, indexing TIME_STAMP allows MySQL to efficiently sort and limit the result set to the
newest messages, improving performance.
- ``INDEX IDX_CITY ON ADDRESS(CITY);``

Many MainePad-Finder queries filter properties by city, especially our optimized "Top-rated properties in a city" query we show as an example. By indexing ADDRESS(CITY), MySQL can quickly locate all addresses in a given city using the index instead of scanning the full ADDRESS table. This index is critical for efficiently supporting searches that are city based. 

## Optimized Queries 
### Query 1: Top Rated Properties In A City 
**Goal of query:** For a given city (e.g., Portland), find all properties in that city and sort them by their average review stars, highest first.

**Tables involved:**
```sql
- ADDRESS.sql
- PROPERTY.sql
- REVIEW.sql
```
#### Before Optimization 
```sql
SELECT 
    P.PROPERTY_ID,
    A.CITY,
    (
        SELECT AVG(R.STARS)
        FROM REVIEW AS R
        WHERE R.PROPERTY_ID = P.PROPERTY_ID
    ) AS AVG_RATING
FROM PROPERTY AS P
JOIN ADDRESS AS A
    ON P.ADDR_ID = A.ADDR_ID
WHERE A.CITY = 'Portland'
ORDER BY AVG_RATING DESC;
```
**What it does** 
- For each property row in Portland, it runs a separate SELECT on REVIEW to compute AVG(STARS)
- On a small dataset, this is fine. On a larger dataset, it can be slower because MySQL keeps re-running the inner query

**Why it is less optimial**
- The inner query is tied to the outer query through P.PROPERTY_ID = R.PROPERTY_ID
- MySQL may need to probe the REVIEW table once per property

#### After Optimization: Using JOIN and GROUP BY
```sql
SELECT 
    P.PROPERTY_ID,
    A.CITY,
    AVG(R.STARS) AS AVG_RATING
FROM PROPERTY AS P
JOIN ADDRESS AS A
    ON P.ADDR_ID = A.ADDR_ID
JOIN REVIEW AS R
    ON R.PROPERTY_ID = P.PROPERTY_ID
WHERE A.CITY = 'Portland'
GROUP BY 
    P.PROPERTY_ID,
    A.CITY
ORDER BY AVG_RATING DESC;
```
**What changed**
- We join REVIEW once and let MySQL compute AVG(R.STARS) using GROUP BY
- MySQL can plan this as a single grouped query instead of outer loop + many inner subqueries

#### Indexing 
```sql
CREATE INDEX IDX_CITY ON ADDRESS(CITY);
```
We use the IDX_CITY index on ADDRESS(CITY) because this query always filters by city. With this index, MySQL can quickly locate all addresses in a given city using an index range scan instead of scanning the entire ADDRESS table.

