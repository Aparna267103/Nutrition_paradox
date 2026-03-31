import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# Load cleaned datasets
# -------------------------------

df_obesity = pd.read_csv("final_obesity_data.csv")
df_malnutrition = pd.read_csv("final_malnutrition_data.csv")

# -------------------------------
# Basic Info
# -------------------------------

print("🔹 OBESITY DATA")
print(df_obesity.info())
print(df_obesity.describe())

print("\n🔹 MALNUTRITION DATA")
print(df_malnutrition.info())
print(df_malnutrition.describe())

# -------------------------------
# Missing Values
# -------------------------------

print("\nMissing Values (Obesity):")
print(df_obesity.isnull().sum())

print("\nMissing Values (Malnutrition):")
print(df_malnutrition.isnull().sum())

# -------------------------------
# Distribution
# -------------------------------

plt.figure()
sns.histplot(df_obesity['Mean_Estimate'], kde=True)
plt.title("Obesity Distribution")
plt.show()

plt.figure()
sns.histplot(df_malnutrition['Mean_Estimate'], kde=True)
plt.title("Malnutrition Distribution")
plt.show()

# -------------------------------
# Trends Over Time
# -------------------------------

plt.figure()
df_obesity.groupby('Year')['Mean_Estimate'].mean().plot()
plt.title("Obesity Trend Over Time")
plt.show()

plt.figure()
df_malnutrition.groupby('Year')['Mean_Estimate'].mean().plot()
plt.title("Malnutrition Trend Over Time")
plt.show()

# -------------------------------
# Region Comparison
# -------------------------------

plt.figure()
df_obesity.groupby('Region')['Mean_Estimate'].mean().sort_values().plot(kind='bar')
plt.title("Obesity by Region")
plt.xticks(rotation=45)
plt.show()

plt.figure()
df_malnutrition.groupby('Region')['Mean_Estimate'].mean().sort_values().plot(kind='bar')
plt.title("Malnutrition by Region")
plt.xticks(rotation=45)
plt.show()

# -------------------------------
# Gender Comparison
# -------------------------------

plt.figure()
sns.boxplot(x='Gender', y='Mean_Estimate', data=df_obesity)
plt.title("Obesity by Gender")
plt.show()

plt.figure()
sns.boxplot(x='Gender', y='Mean_Estimate', data=df_malnutrition)
plt.title("Malnutrition by Gender")
plt.show()

# -------------------------------
# Scatter Plot
# -------------------------------

plt.figure()
sns.scatterplot(x='CI_Width', y='Mean_Estimate', data=df_obesity)
plt.title("Obesity CI vs Mean")
plt.show()

plt.figure()
sns.scatterplot(x='CI_Width', y='Mean_Estimate', data=df_malnutrition)
plt.title("Malnutrition CI vs Mean")
plt.show()

print("\n✅ EDA Completed Successfully!")