import pandas as pd
import psycopg

import os
from dotenv import load_dotenv

load_dotenv()

# -------------------------------
# Step 1: Load cleaned datasets
# -------------------------------

df_obesity = pd.read_csv("final_obesity_data.csv")
df_malnutrition = pd.read_csv("final_malnutrition_data.csv")

# -------------------------------
# Step 2: Connect to PostgreSQL
# -------------------------------

conn = psycopg.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()

print("✅ Connected to PostgreSQL")

# -------------------------------
# Step 3: Create Tables
# -------------------------------

create_obesity_table = """
CREATE TABLE IF NOT EXISTS obesity (
    Year INT,
    Gender VARCHAR(10),
    Mean_Estimate FLOAT,
    LowerBound FLOAT,
    UpperBound FLOAT,
    age_group VARCHAR(20),
    Country VARCHAR(100),
    Region VARCHAR(100),
    CI_Width FLOAT,
    Obesity_level VARCHAR(20)
);
"""

create_malnutrition_table = """
CREATE TABLE IF NOT EXISTS malnutrition (
    Year INT,
    Gender VARCHAR(10),
    Mean_Estimate FLOAT,
    LowerBound FLOAT,
    UpperBound FLOAT,
    age_group VARCHAR(20),
    Country VARCHAR(100),
    Region VARCHAR(100),
    CI_Width FLOAT,
    Malnutrition_level VARCHAR(20)
);
"""

cursor.execute(create_obesity_table)
cursor.execute(create_malnutrition_table)

conn.commit()

print("✅ Tables created")

# -------------------------------
# Step 4: Insert Data (Obesity)
# -------------------------------

insert_obesity = """
INSERT INTO obesity (
    Year, Gender, Mean_Estimate, LowerBound, UpperBound,
    age_group, Country, Region, CI_Width, Obesity_level
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

for _, row in df_obesity.iterrows():
    cursor.execute(insert_obesity, (
        int(row['Year']),
        row['Gender'],
        float(row['Mean_Estimate']),
        float(row['LowerBound']),
        float(row['UpperBound']),
        row['age_group'],
        row['Country'],
        row['Region'],
        float(row['CI_Width']),
        row['Obesity_level']
    ))

conn.commit()
print("✅ Obesity data inserted")

# -------------------------------
# Step 5: Insert Data (Malnutrition)
# -------------------------------

insert_malnutrition = """
INSERT INTO malnutrition (
    Year, Gender, Mean_Estimate, LowerBound, UpperBound,
    age_group, Country, Region, CI_Width, Malnutrition_level
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

for _, row in df_malnutrition.iterrows():
    cursor.execute(insert_malnutrition, (
        int(row['Year']),
        row['Gender'],
        float(row['Mean_Estimate']),
        float(row['LowerBound']),
        float(row['UpperBound']),
        row['age_group'],
        row['Country'],
        row['Region'],
        float(row['CI_Width']),
        row['Malnutrition_level']
    ))

conn.commit()
print("✅ Malnutrition data inserted")

# -------------------------------
# Step 6: Close connection
# -------------------------------

cursor.close()
conn.close()

print("🎉 Data successfully inserted into PostgreSQL!")
