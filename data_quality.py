### Imports and data reading/loading ###

# Import libraries
import pandas as pd
import json

# Function for reading files
def read_json(file_name):
    result = ''
    # Add commas to end of each line for compatibility with Python JSON format
    with open(file_name) as f:
        for line in f:
            result += line.strip('\n') + ',\n'

    # Format JSON as list
    result = '[' + result[:-2] + ']'
    result = json.loads(result)
    
    return result

receipts = read_json('receipts.json')
users = read_json('users.json')
brands = read_json('brands.json')

# Modify default dictionary get method to return empty dictionary if value is None
def safe_get(dict_name, key, value_if_missing):
    if dict_name.get(key, None) == None:
        return dict()
    else:
        return dict_name[key]

# Convert JSON file to dataframe
receipts_df = pd.DataFrame()

for receipt in receipts:
    receipt_dict = dict()
    receipt_dict['_id'] = [safe_get(receipt, '_id', dict()).get('$oid', None)]
    receipt_dict['bonusPointsEarned'] = [receipt.get('bonusPointsEarned', None)]
    receipt_dict['bonusPointsEarnedReason'] = [receipt.get('bonusPointsEarnedReason', None)]
    receipt_dict['createDate'] = [safe_get(receipt, 'createDate', dict()).get('$date', None)]
    receipt_dict['dateScanned'] = [safe_get(receipt, 'dateScanned', dict()).get('$date', None)]
    receipt_dict['finishedDate'] = [safe_get(receipt, 'finishedDate', dict()).get('$date', None)]
    receipt_dict['modifyDate'] = [safe_get(receipt, 'modifyDate', dict()).get('$date', None)]
    receipt_dict['pointsAwardedDate'] = [safe_get(receipt, 'pointsAwardedDate', dict()).get('$date', None)]
    receipt_dict['pointsEarned'] = [receipt.get('pointsEarned', None)]
    receipt_dict['purchaseDate'] = [safe_get(receipt, 'purchaseDate', None).get('$date', None)]
    receipt_dict['purchasedItemCount'] = [receipt.get('purchasedItemCount', None)]
    receipt_dict['rewardsReceiptItemList'] = [receipt.get('rewardsReceiptItemList', None)]
    receipt_dict['rewardsReceiptStatus'] = [receipt.get('rewardsReceiptStatus', None)]
    receipt_dict['totalSpent'] = [receipt.get('totalSpent', None)]
    receipt_dict['userId'] = [receipt.get('userId', None)]
    receipts_df = receipts_df.append(pd.DataFrame(data = receipt_dict))
    
brands_df = pd.DataFrame()
for brand in brands:
    brand_dict = dict()
    brand_dict['_id'] = [safe_get(brand, '_id', dict()).get('$oid', None)]
    brand_dict['barcode'] = [brand.get('barcode', None)]
    brand_dict['brandCode'] = [brand.get('brandCode', None)] 
    brand_dict['category'] = [brand.get('category', None)]
    brand_dict['categoryCode'] = [brand.get('categoryCode', None)]
    brand_dict['cpg'] = [brand.get('cpg', None)]
    brand_dict['topBrand'] = [brand.get('topBrand', None)]
    brand_dict['name'] = [brand.get('name', None)]
    brands_df = brands_df.append(pd.DataFrame(data = brand_dict))
    
users_df = pd.DataFrame()
for user in users:
    user_dict = dict()
    user_dict['_id'] = [safe_get(user, '_id', dict()).get('$oid', None)]
    user_dict['state'] = [user.get('state', None)]
    user_dict['createdDate'] = [safe_get(user, 'createdDate', dict()).get('$date', None)]
    user_dict['lastLogin'] = [safe_get(user, 'lastLogin', dict()).get('$date', None)]
    user_dict['role'] = [user.get('role', None)]
    user_dict['active'] = [user.get('active', None)]
    users_df = users_df.append(pd.DataFrame(data = user_dict))

### Perform checks on recipts ###

# Ensure that all numeric columns are correctly identified as such
numeric_columns = ['bonusPointsEarned', 'pointsEarned', 'purchasedItemCount', 'totalSpent']
for column in numeric_columns:
    receipts_df[column] = pd.to_numeric(receipts_df[column])


# Check that _id field is unique and not null
print("Total receipt rows:", len(receipts_df['_id']))
print("Unique receipt _id values:", receipts_df['_id'].nunique())
print("Null receipt _id values:", sum(receipts_df['_id'].isna()))

# Check whether userID field is not null
print("Total rows with null userID:", sum(receipts_df['userId'].isna()))

# Examine numeric values for potential anomolies
receipts_df[numeric_columns].describe()

# Check that order of dates is as expected (purchase prior to scan, create prior to any other date, 
# finished date after any other date, scan prior to points awarded)
date_fields = ['createDate', 'dateScanned', 'modifyDate', 'pointsAwardedDate',
               'purchaseDate', 'finishedDate']

for date_field in date_fields[1:]:
    print(f"Number of records where {date_field} is prior to createDate: ",
          sum((receipts_df[date_field] - receipts_df['createDate']).apply(lambda x: True if x < 0 else False)))

for date_field in date_fields[:-1]:
    print(f"Number of records where {date_field} is after to finishedDate: ",
          sum((receipts_df[date_field] - receipts_df['finishedDate']).apply(lambda x: True if x > 0 else False)))

print("Number of records where dateScanned is prior to purchaseDate: ",
      sum((receipts_df['dateScanned'] - receipts_df['purchaseDate']).apply(lambda x: True if x < 0 else False)))

print("Number of records where pointsAwardedDate is prior to dateScanned: ",
      sum((receipts_df['pointsAwardedDate'] - receipts_df['dateScanned']).apply(lambda x: True if x < 0 else False)))


# Compute average totalSpent and sum of purchasedItemCount by rewardsReceiptStatus
receipts_df.groupby('rewardsReceiptStatus').agg({'totalSpent': ['mean'], 'purchasedItemCount': ['sum']})

### Perform checks on brands ###

# Check that _id field is unique and not null
print("Total brand rows:", len(brands_df['_id']))
print("Unique brand _id values:", brands_df['_id'].nunique())
print("Null brand _id values:", sum(brands_df['_id'].isna()))

# Ensure that category code and category have one-to-one relationship
brands_df[['category', 'categoryCode']].groupby('category').nunique()

# Check whether barcodes and brand codes are unique for a given brand
brands_df[['barcode', '_id']].groupby('barcode').size().sort_values()
brands_df[['brandCode', '_id']].groupby('brandCode').size().sort_values()

### Perform checks on users ###

# Check that _id field is unique and not null
print("Total user rows:", len(users_df['_id']))
print("Unique user _id values:", users_df['_id'].nunique())
print("Null user _id values:", sum(users_df['_id'].isna()))
print("Number of duplicated user records: ", sum(users_df.duplicated()))

# Ensure that last login is more recent than created date
print("Number of records where lastLogin is prior to createdDate: ",
      sum((users_df['lastLogin'] - users_df['createdDate']).apply(lambda x: True if x < 0 else False)))

