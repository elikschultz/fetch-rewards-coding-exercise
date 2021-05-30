# Fetch Rewards Coding Exercise

## 1. Relational data model
I created a relational data model that is diagramed in relational_data_model.pdf. There were a few tricky decisions to make when designing that, which are discussed further in the document itself.

## 2. SQL query to answer business stakeholder question
This query is written to run in PostgreSQL, although the syntax is all pretty standard and I would expect it to work in most other dialects as well. This query answers the questions in both the third and fourth bullet points, since they can both be answered using just one aggregation.

I did not feel like I had enough information to create a model that answers the questions asked in the remaining bullet points because I determined that it was not feasible to define a relationshiop between receipts and brands given the information in hand (ass per the discussion in `relational_data_model.pdf`, and because I did not have access to the parter product file mentioned in the description for the brandCode field the brand data schema). 

## 3. Data quality
The `data_quality.py` script runs a number of data quality checks. The potential issues I discovered were the following:

- There are 628 records in the receipts data where the purchase data is prior to the creation date. This may or may not be an issue, but flagged it because I am not clear on what exactly the creation date represents.
- There are 172 records in the receipts data where the modify date is after the finish date. I can also imagine some business logic that would explain this, but thought it was worth flagging as well.
- There are 7 records where the purchase date is after the finish date, which does not seem like it should ever be the case.
- There are 13 records where the scan date is prior to the purchase date, which again seems like it should never be the case.
- There are 212 unique user_id values and 495 user records. It turns out that 283 of the records are duplicates.
- Barcodes in the brands data are not unique. Looking at a few of the duplications, it appears that there may be some test/dummy data causing this (e.g. barcode 511111704140 is used for the sauce brand Prego, but also for "Diet Chris Cola")
- Many categories in the brands data are mising category codes.

## 4. Communicate with Stakeholders
