## Query Optimization & Indexing 
This section analyzes how we improved the performance of key MainePad-Finder queries

### Indexing Choices


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

