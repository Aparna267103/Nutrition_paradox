import pandas as pd

# -------------------------------
# Step 1: Load datasets from WHO API
# -------------------------------

url_adult_obesity = "https://ghoapi.azureedge.net/api/NCD_BMI_30C"
url_child_obesity = "https://ghoapi.azureedge.net/api/NCD_BMI_PLUS2C"
url_adult_underweight = "https://ghoapi.azureedge.net/api/NCD_BMI_18C"
url_child_thinness = "https://ghoapi.azureedge.net/api/NCD_BMI_MINUS2C"

print("Loading datasets...")

df_adult_obesity = pd.read_json(url_adult_obesity)
df_child_obesity = pd.read_json(url_child_obesity)
df_adult_underweight = pd.read_json(url_adult_underweight)
df_child_thinness = pd.read_json(url_child_thinness)

# The actual data is inside the 'value' key
df_adult_obesity = pd.json_normalize(df_adult_obesity['value'])
df_child_obesity = pd.json_normalize(df_child_obesity['value'])
df_adult_underweight = pd.json_normalize(df_adult_underweight['value'])
df_child_thinness = pd.json_normalize(df_child_thinness['value'])

print("Datasets loaded successfully.\n")

# -------------------------------
# Step 2: Add age_group column
# -------------------------------

df_adult_obesity['age_group'] = 'Adults'
df_child_obesity['age_group'] = 'Children'

df_adult_underweight['age_group'] = 'Adults'
df_child_thinness['age_group'] = 'Children'

# -------------------------------
# Step 3: Combine obesity datasets
# -------------------------------

df_obesity = pd.concat([df_adult_obesity, df_child_obesity], ignore_index=True)

# -------------------------------
# Step 4: Combine malnutrition datasets
# -------------------------------

df_malnutrition = pd.concat([df_adult_underweight, df_child_thinness], ignore_index=True)

# -------------------------------
# Step 5: Filter years (2012–2022)
# -------------------------------

df_obesity_filtered = df_obesity[
    (df_obesity['TimeDim'] >= 2012) & (df_obesity['TimeDim'] <= 2022)
]

df_malnutrition_filtered = df_malnutrition[
    (df_malnutrition['TimeDim'] >= 2012) & (df_malnutrition['TimeDim'] <= 2022)
]

# -------------------------------
# Optional: Select useful columns
# -------------------------------

columns_to_keep = [
    'SpatialDim',       # Country code
    'ParentLocation',         # Country name
    'TimeDim',          # Year
    'Dim1',             # Sex
    'NumericValue',     # Value
    'Low',              # Lower CI
    'High',             # Upper CI
    'age_group'
]

df_obesity_filtered = df_obesity_filtered[columns_to_keep]
df_malnutrition_filtered = df_malnutrition_filtered[columns_to_keep]

# -------------------------------
# Save cleaned datasets
# -------------------------------

df_obesity_filtered.to_csv("obesity_cleaned.csv", index=False)
df_malnutrition_filtered.to_csv("malnutrition_cleaned.csv", index=False)

print("Processing completed!")
print("Saved files:")
print("- obesity_cleaned.csv")
print("- malnutrition_cleaned.csv")

# -------------------------------
# Preview data
# -------------------------------

print("\nObesity Data Sample:")
print(df_obesity_filtered.head())

print("\nMalnutrition Data Sample:")
print(df_malnutrition_filtered.head())