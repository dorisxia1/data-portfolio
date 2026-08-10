
import pandas as pd
from pymongo import MongoClient
import pprint
import re

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB_NAME = "chatdb_nosql"
CSV_FILE = "wages_by_education.csv"

COLL_OVERALL = "wages_overall"
COLL_GENDER = "wages_gender"
COLL_RACE = "wages_race"

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

print(f"Dropping existing collections: {COLL_OVERALL}, {COLL_GENDER}, {COLL_RACE}...")
db[COLL_OVERALL].drop()
db[COLL_GENDER].drop()
db[COLL_RACE].drop()
if "wages_by_education" in db.list_collection_names():
    print("Dropping old collection: wages_by_education...")
    db["wages_by_education"].drop()

coll_overall = db[COLL_OVERALL]
coll_gender = db[COLL_GENDER]
coll_race = db[COLL_RACE]

try:
    df_wages = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    print(f"Error: {CSV_FILE} not found.")
    exit(1)

all_cols = df_wages.columns.tolist()
if 'year' not in all_cols:
    print("Error: 'year' column not found in CSV.")
    exit(1)

overall_core_cols = ['less_than_hs', 'high_school', 'some_college', 'bachelors_degree', 'advanced_degree']
overall_cols = ['year'] + [col for col in overall_core_cols if col in all_cols]

gender_cols = ['year'] + [
    col for col in all_cols if
    ('men' in col or 'women' in col) and
    not any(race in col for race in ['white', 'black', 'hispanic', 'asian']) and
    col != 'year'
]

race_cols = ['year'] + [
    col for col in all_cols if
    any(race in col for race in ['white', 'black', 'hispanic', 'asian']) and
    col != 'year'
]
print(f"Identified Overall columns: {overall_cols}")
print(f"Identified Gender columns: {gender_cols}")
print(f"Identified Race columns: {race_cols}")

print("Processing and inserting data into MongoDB...")
inserted_counts = {COLL_OVERALL: 0, COLL_GENDER: 0, COLL_RACE: 0}

for index, row in df_wages.iterrows():
    year = int(row['year'])

    doc_overall = {col: row[col] for col in overall_cols if col in row}
    doc_overall['year'] = year 
    coll_overall.insert_one(doc_overall)
    inserted_counts[COLL_OVERALL] += 1

    doc_gender = {col: row[col] for col in gender_cols if col in row}
    doc_gender['year'] = year
    coll_gender.insert_one(doc_gender)
    inserted_counts[COLL_GENDER] += 1

    doc_race = {col: row[col] for col in race_cols if col in row}
    doc_race['year'] = year
    coll_race.insert_one(doc_race)
    inserted_counts[COLL_RACE] += 1

print("\nMongoDB Insert Complete.")
print(f"Total documents inserted:")
print(f" - {COLL_OVERALL}: {inserted_counts[COLL_OVERALL]}")
print(f" - {COLL_GENDER}: {inserted_counts[COLL_GENDER]}")
print(f" - {COLL_RACE}: {inserted_counts[COLL_RACE]}")

print("\nSample document from wages_overall (year 2022):")
pprint.pprint(coll_overall.find_one({"year": 2022}))
print("\nSample document from wages_gender (year 2022):")
pprint.pprint(coll_gender.find_one({"year": 2022}))
print("\nSample document from wages_race (year 2022):")
pprint.pprint(coll_race.find_one({"year": 2022}))

client.close()
print("\nMongoDB connection closed.")
