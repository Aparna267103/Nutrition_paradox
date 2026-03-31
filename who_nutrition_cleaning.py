import pandas as pd
import pycountry

# -------------------------------
# Step 0: API URLs
# -------------------------------

url_adult_obesity = "https://ghoapi.azureedge.net/api/NCD_BMI_30C"
url_child_obesity = "https://ghoapi.azureedge.net/api/NCD_BMI_PLUS2C"
url_adult_underweight = "https://ghoapi.azureedge.net/api/NCD_BMI_18C"
url_child_thinness = "https://ghoapi.azureedge.net/api/NCD_BMI_MINUS2C"

# -------------------------------
# Step 1: Load datasets
# -------------------------------

def load_data(url):
    df = pd.read_json(url)
    return pd.json_normalize(df['value'])

df_adult_obesity = load_data(url_adult_obesity)
df_child_obesity = load_data(url_child_obesity)
df_adult_underweight = load_data(url_adult_underweight)
df_child_thinness = load_data(url_child_thinness)

# -------------------------------
# Step 2: Add age_group
# -------------------------------

df_adult_obesity['age_group'] = 'Adult'
df_child_obesity['age_group'] = 'Child/Adolescent'

df_adult_underweight['age_group'] = 'Adult'
df_child_thinness['age_group'] = 'Child/Adolescent'

# -------------------------------
# Step 3: Combine datasets
# -------------------------------

df_obesity = pd.concat([df_adult_obesity, df_child_obesity], ignore_index=True)
df_malnutrition = pd.concat([df_adult_underweight, df_child_thinness], ignore_index=True)

# -------------------------------
# Step 4: Filter years (2012–2022)
# -------------------------------

df_obesity = df_obesity[(df_obesity['TimeDim'] >= 2012) & (df_obesity['TimeDim'] <= 2022)]
df_malnutrition = df_malnutrition[(df_malnutrition['TimeDim'] >= 2012) & (df_malnutrition['TimeDim'] <= 2022)]

# -------------------------------
# Step 5: Keep required columns
# -------------------------------

columns_to_keep = [
    'ParentLocation',
    'Dim1',
    'TimeDim',
    'Low',
    'High',
    'NumericValue',
    'SpatialDim',
    'age_group'
]

df_obesity = df_obesity[columns_to_keep]
df_malnutrition = df_malnutrition[columns_to_keep]

# -------------------------------
# Step 6: Rename columns
# -------------------------------

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

# -------------------------------
# Step 7: Standardize Gender
# -------------------------------

def standardize_gender(g):
    g = str(g).lower()
    if 'male' in g:
        return 'Male'
    elif 'female' in g:
        return 'Female'
    else:
        return 'Both'

df_obesity['Gender'] = df_obesity['Gender'].apply(standardize_gender)
df_malnutrition['Gender'] = df_malnutrition['Gender'].apply(standardize_gender)

# -------------------------------
# Step 8: Convert Country Codes
# -------------------------------

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
    'AMR': 'Americas Region',
    'WB_UMI': 'Upper Middle Income'
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

# -------------------------------
# Step 9: Create CI_Width
# -------------------------------

df_obesity['CI_Width'] = df_obesity['UpperBound'] - df_obesity['LowerBound']
df_malnutrition['CI_Width'] = df_malnutrition['UpperBound'] - df_malnutrition['LowerBound']

# -------------------------------
# Step 10: Obesity Level
# -------------------------------

def obesity_level(val):
    if val >= 30:
        return 'High'
    elif val >= 25:
        return 'Moderate'
    else:
        return 'Low'

df_obesity['Obesity_level'] = df_obesity['Mean_Estimate'].apply(obesity_level)

# -------------------------------
# Step 11: Malnutrition Level
# -------------------------------

def malnutrition_level(val):
    if val >= 20:
        return 'High'
    elif val >= 10:
        return 'Moderate'
    else:
        return 'Low'

df_malnutrition['Malnutrition_level'] = df_malnutrition['Mean_Estimate'].apply(malnutrition_level)

# -------------------------------
# Step 12: Save final datasets
# -------------------------------

df_obesity.to_csv("final_obesity_data.csv", index=False)
df_malnutrition.to_csv("final_malnutrition_data.csv", index=False)

print("✅ Data cleaning & feature engineering completed!")
print("Files saved:")
print("- final_obesity_data.csv")
print("- final_malnutrition_data.csv")

# -------------------------------
# Preview
# -------------------------------

print("\nObesity Data Sample:")
print(df_obesity.head())

print("\nMalnutrition Data Sample:")
print(df_malnutrition.head())