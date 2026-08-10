
import pandas as pd
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

# --- Configuration ---
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")

if not MYSQL_USER or not MYSQL_PASSWORD or not MYSQL_DB:
    raise ValueError("Missing MySQL configuration in .env")

# --- Connect to MySQL ---
conn = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB
)

cursor = conn.cursor()

df_lw = pd.read_csv('livingwage.csv')
household_cols = [col for col in df_lw.columns if col.endswith('_living_wage')]
household_map = {}

for col in household_cols:
    description = col.replace('_living_wage', '').replace('_', ' ').title()
    cursor.execute("INSERT INTO HouseholdType (description) VALUES (%s)", (description,))
    household_map[col] = cursor.lastrowid

for _, row in df_lw.iterrows():
    cursor.execute(
        "INSERT INTO City (city_name, state_name, population_2020, population_2010, land_area_sqmi, density) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (row["city"], row["state"], row["population_2020"], row["population_2010"], row["land_area_sqmi"], row["density"])
    )
    city_id = cursor.lastrowid
    for col in household_cols:
        wage = row[col]
        household_id = household_map[col]
        cursor.execute(
            "INSERT INTO LivingWage (city_id, household_id, wage) VALUES (%s, %s, %s)",
            (city_id, household_id, wage)
        )

df_poverty = pd.read_csv('poverty_level_wages.csv')
group_cols = [col for col in df_poverty.columns if col != 'year']
group_map = {}

for group in group_cols:
    group_name = group.replace('_', ' ').title()
    cursor.execute("INSERT INTO PovertyGroup (group_name) VALUES (%s)", (group_name,))
    group_map[group] = cursor.lastrowid

for _, row in df_poverty.iterrows():
    year = int(row["year"])
    annual_wage = 20800
    hourly_wage = 10.00
    cursor.execute(
        "INSERT INTO YearlyPovertyThresholds (year, annual_poverty_wage, hourly_poverty_wage) VALUES (%s, %s, %s)",
        (year, annual_wage, hourly_wage)
    )
    for group in group_cols:
        try:
            perc = float(row[group])
            if perc < 0 or perc > 100:
                perc = 0.0
        except:
            perc = 0.0
        cursor.execute(
            "INSERT INTO PovertyWageDistribution (year, group_id, percentage) VALUES (%s, %s, %s)",
            (year, group_map[group], perc)
        )

conn.commit()
cursor.close()
conn.close()
print("Data successfully loaded into MySQL.")
