import pandas as pd
import pycountry

# -----------------------------------
# Load Raw Files
# -----------------------------------

df_obesity = pd.read_csv("obesity_raw.csv")
df_malnutrition = pd.read_csv("malnutrition_raw.csv")

print("Raw datasets loaded!")

# -----------------------------------
# Rename Columns
# -----------------------------------

rename_dict = {
    'TimeDim': 'Year',
    'Dim1': 'Gender',
    'NumericValue': 'Mean_Estimate',
    'Low': 'LowerBound',
    'High': 'UpperBound',
    'ParentLocation': 'Region',
    'SpatialDim': 'Country'
}

df_obesity.rename(columns=rename_dict, inplace=True)
df_malnutrition.rename(columns=rename_dict, inplace=True)

# -----------------------------------
# Standardize Gender
# -----------------------------------

def standardize_gender(g):

    g = str(g).lower()

    if 'male' in g:
        return 'Male'

    elif 'female' in g:
        return 'Female'

    return 'Both'

df_obesity['Gender'] = df_obesity['Gender'].apply(standardize_gender)
df_malnutrition['Gender'] = df_malnutrition['Gender'].apply(standardize_gender)

# -----------------------------------
# Convert Country Codes
# -----------------------------------

special_cases = {
    'GLOBAL': 'Global',
    'WB_LMI': 'Low & Middle Income',
    'WB_HI': 'High Income',
    'WB_LI': 'Low Income',
    'EMR': 'Eastern Mediterranean Region',
    'EUR': 'Europe',
    'AFR': 'Africa',
    'SEAR': 'South-East Asia Region',
    'WPR': 'Western Pacific Region',
    'AMR': 'Americas Region'
}

def convert_country(code):

    try:
        country = pycountry.countries.get(alpha_3=code)

        if country:
            return country.name

    except:
        pass

    return special_cases.get(code, code)

df_obesity['Country'] = df_obesity['Country'].apply(convert_country)
df_malnutrition['Country'] = df_malnutrition['Country'].apply(convert_country)

# -----------------------------------
# Create Confidence Interval Width
# -----------------------------------

df_obesity['CI_Width'] = (
    df_obesity['UpperBound'] -
    df_obesity['LowerBound']
)

df_malnutrition['CI_Width'] = (
    df_malnutrition['UpperBound'] -
    df_malnutrition['LowerBound']
)

# -----------------------------------
# Obesity Classification
# -----------------------------------

def obesity_level(value):

    if value >= 30:
        return 'High'

    elif value >= 25:
        return 'Moderate'

    return 'Low'

df_obesity['Obesity_Level'] = (
    df_obesity['Mean_Estimate']
    .apply(obesity_level)
)

# -----------------------------------
# Malnutrition Classification
# -----------------------------------

def malnutrition_level(value):

    if value >= 20:
        return 'High'

    elif value >= 10:
        return 'Moderate'

    return 'Low'

df_malnutrition['Malnutrition_Level'] = (
    df_malnutrition['Mean_Estimate']
    .apply(malnutrition_level)
)

# -----------------------------------
# Save Final Cleaned Files
# -----------------------------------

df_obesity.to_csv(
    "final_obesity_data.csv",
    index=False
)

df_malnutrition.to_csv(
    "final_malnutrition_data.csv",
    index=False
)

print("\n✅ Cleaning Completed!")

print("\nFiles Saved:")
print("1. final_obesity_data.csv")
print("2. final_malnutrition_data.csv")

# -----------------------------------
# Preview
# -----------------------------------

print("\nObesity Data:")
print(df_obesity.head())

print("\nMalnutrition Data:")
print(df_malnutrition.head())
