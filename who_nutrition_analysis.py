import pandas as pd

# -----------------------------------
# WHO API URLs
# -----------------------------------

URLS = {
    "adult_obesity": "https://ghoapi.azureedge.net/api/NCD_BMI_30C",
    "child_obesity": "https://ghoapi.azureedge.net/api/NCD_BMI_PLUS2C",
    "adult_underweight": "https://ghoapi.azureedge.net/api/NCD_BMI_18C",
    "child_thinness": "https://ghoapi.azureedge.net/api/NCD_BMI_MINUS2C"
}

# -----------------------------------
# Load API Data
# -----------------------------------

def load_dataset(url):
    df = pd.read_json(url)
    return pd.json_normalize(df['value'])

print("Loading WHO datasets...")

df_adult_obesity = load_dataset(URLS["adult_obesity"])
df_child_obesity = load_dataset(URLS["child_obesity"])

df_adult_underweight = load_dataset(URLS["adult_underweight"])
df_child_thinness = load_dataset(URLS["child_thinness"])

print("Datasets loaded successfully!")

# -----------------------------------
# Add Age Group
# -----------------------------------

df_adult_obesity['age_group'] = 'Adult'
df_child_obesity['age_group'] = 'Child'

df_adult_underweight['age_group'] = 'Adult'
df_child_thinness['age_group'] = 'Child'

# -----------------------------------
# Combine Datasets
# -----------------------------------

df_obesity = pd.concat(
    [df_adult_obesity, df_child_obesity],
    ignore_index=True
)

df_malnutrition = pd.concat(
    [df_adult_underweight, df_child_thinness],
    ignore_index=True
)

# -----------------------------------
# Filter Years
# -----------------------------------

df_obesity = df_obesity[
    (df_obesity['TimeDim'] >= 2012) &
    (df_obesity['TimeDim'] <= 2022)
]

df_malnutrition = df_malnutrition[
    (df_malnutrition['TimeDim'] >= 2012) &
    (df_malnutrition['TimeDim'] <= 2022)
]

# -----------------------------------
# Keep Required Columns
# -----------------------------------

required_columns = [
    'SpatialDim',
    'ParentLocation',
    'TimeDim',
    'Dim1',
    'NumericValue',
    'Low',
    'High',
    'age_group'
]

df_obesity = df_obesity[required_columns]
df_malnutrition = df_malnutrition[required_columns]

# -----------------------------------
# Save Intermediate Files
# -----------------------------------

df_obesity.to_csv("obesity_raw.csv", index=False)
df_malnutrition.to_csv("malnutrition_raw.csv", index=False)

print("\nFiles Saved:")
print("1. obesity_raw.csv")
print("2. malnutrition_raw.csv")

# -----------------------------------
# Preview
# -----------------------------------

print("\nObesity Sample:")
print(df_obesity.head())

print("\nMalnutrition Sample:")
print(df_malnutrition.head())
