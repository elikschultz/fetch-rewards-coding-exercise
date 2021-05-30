# [Fetch Rewards Coding Exercise](https://fetch-hiring.s3.amazonaws.com/analytics-engineer/ineeddata-data-modeling/data-modeling.html)

## 1. Relational data model
I created a relational data model that is diagramed in `relational_data_model.pdf.`

## 2. SQL query to answer business stakeholder question
This query is written to run in PostgreSQL, although the syntax is all pretty standard and I would expect it to work in most other dialects as well. This query answers the questions in both the third and fourth bullet points, since they can both be answered using just one aggregation.

I chose to answer those two rather than the other questions because I have some hesitations about the reliability of the receipt to brand relationship (via a bridge table) in the model I created. The first is that many receipts are missing `brandCode` values, and the second is that `brandCode` is not totally unique (there are two exceptions that need to be addresed prior to this relationship becoming operational). Any queries that use the bridge table would also require additional joins, which would make them less performant. 

## 3. Data quality
The `data_quality.py` script runs a number of data quality checks. The potential issues I discovered were the following:

- There are 628 records in the receipts data where the purchase data is prior to the creation date. This may or may not be an issue, but flagged it because I am not clear on what exactly the creation date represents.
- There are 172 records in the receipts data where the modify date is after the finish date. I can also imagine some business logic that would explain this, but thought it was worth flagging as well.
- There are 7 records where the purchase date is after the finish date, which does not seem like it should ever be the case.
- There are 13 records where the scan date is prior to the purchase date, which again seems like it should never be the case.
- There are 212 unique user_id values and 495 user records. It turns out that 283 of the records are duplicates.
- Barcodes in the brands data are not unique. Looking at a few of the duplications, it appears that there may be some test/dummy data causing this (e.g. barcode 511111704140 is used for the sauce brand Prego, but also used for "Diet Chris Cola")
- Many categories in the brands data are mising category codes.
- There are two brand codes that are associated with two different brand records (HUGGIES and GOODNITES), as well as 35 brand records with no brand code.

## 4. Communicate with Stakeholders
The `stakeholder_email.rtf` file contains a sample email. The questions asked in this section cover a lot of ground, and I've found that emails that are longer than a couple sentences do not tend to get read fully. Given the option I think I would have set up a call first to discuss these topics, and then follow up with emails later.
