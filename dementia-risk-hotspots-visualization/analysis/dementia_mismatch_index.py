import pandas as pd
from sklearn.linear_model import LinearRegression

# Load dementia data
dementia = pd.read_csv("NORC_Dementia_DataHub_County_2020.csv", dtype={'FIPS': str})
dementia = dementia[dementia['DEMENTIACAT'] == 'Total']  # Use total dementia prevalence

# Load PLACES dataset
places = pd.read_csv("PLACES__Local_Data_for_Better_Health__County_Data_2024_release_20250307.csv", dtype={'LocationName': str})

# Filter for relevant measures
measures = {
    "Stroke among adults aged >=18 years": "stroke_rate",
    "Diagnosed diabetes among adults aged >=18 years": "diabetes_rate",
    "Cognitive disability among adults aged >=18 years": "cognitive_disability_rate"
}
places = places[places["Measure"].isin(measures.keys()) & (places["Data_Value_Type"] == "Crude prevalence")]

# Pivot PLACES to wide format
places_pivot = places.pivot_table(
    index=["LocationID", "StateAbbr", "LocationName"],
    columns="Measure",
    values="Data_Value"
).reset_index()

# Rename columns
places_pivot.rename(columns={
    "LocationID": "FIPS",
    "Stroke among adults aged >=18 years": "stroke_rate",
    "Diagnosed diabetes among adults aged >=18 years": "diabetes_rate",
    "Cognitive disability among adults aged >=18 years": "cognitive_disability_rate"
}, inplace=True)

# Prepare dementia prevalence
dementia = dementia[['FIPS', 'StateAbbr', 'LocationName', 'prevalence_rate']]

# Merge
merged = pd.merge(dementia, places_pivot, on='FIPS', how='left')

# Drop rows with missing values
merged = merged.dropna(subset=['stroke_rate', 'diabetes_rate', 'cognitive_disability_rate', 'prevalence_rate'])

# Build linear regression model
X = merged[['stroke_rate', 'diabetes_rate', 'cognitive_disability_rate']]
y = merged['prevalence_rate']
model = LinearRegression().fit(X, y)

# Predict expected prevalence
merged['expected_prevalence'] = model.predict(X)

# Compute mismatch index
merged['mismatch_index'] = merged['prevalence_rate'] - merged['expected_prevalence']

# Save relevant columns
output = merged[['FIPS', 'StateAbbr', 'LocationName', 'stroke_rate', 'diabetes_rate',
                 'cognitive_disability_rate', 'prevalence_rate',
                 'expected_prevalence', 'mismatch_index']]

# Save to CSV
output.to_csv("dementia_mismatch_index.csv", index=False)
