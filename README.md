# 🥗 Nutrition Paradox: Obesity vs Malnutrition Analysis

## 📌 Project Overview

The **Nutrition Paradox Project** analyzes the coexistence of **obesity and malnutrition** across different countries, regions, genders, and age groups using WHO data.

This project demonstrates a complete **data pipeline**:

* Data extraction from API
* Data cleaning & transformation
* Database storage (PostgreSQL)
* SQL-based analysis
* Interactive visualization using Power BI

---

## 🎯 Objectives

* Analyze global trends in obesity and malnutrition
* Compare regions, countries, and demographics
* Identify patterns, disparities, and anomalies
* Build an interactive dashboard for insights

---

## 🛠️ Tech Stack

* **Python** (Pandas, NumPy)
* **PostgreSQL** (Database)
* **SQL** (Analysis queries)
* **Power BI** (Visualization)

---

## 📂 Project Structure

```
Nutrition_Paradox_Project/
│
├── db_connection.py
├── who_nutrition_analysis.py
├── who_nutrition_cleaning.py
├── who_nutrition_eda.py
├── who_sql_insert.py
├── who_analysis_queries.sql
│
├── obesity_cleaned.csv
├── malnutrition_cleaned.csv
├── final_obesity_data.csv
├── final_malnutrition_data.csv
│
└── README.md
```

---

## 🔄 Workflow

### 1️⃣ Data Collection

* Data is fetched from WHO API endpoints:

  * Adult & Child Obesity
  * Adult & Child Malnutrition

---

### 2️⃣ Data Cleaning & Transformation

* Filter years (2012–2022)
* Standardize gender values
* Convert country codes
* Create new features:

  * `CI_Width`
  * `Obesity_level`
  * `Malnutrition_level`

---

### 3️⃣ Exploratory Data Analysis (EDA)

* Distribution plots
* Trend analysis
* Region & gender comparisons
* Scatter plots for uncertainty

---

### 4️⃣ Database Integration

* PostgreSQL used for storing structured data
* Tables created:

  * `obesity`
  * `malnutrition`

---

### 5️⃣ SQL Analysis

* 20+ analytical queries including:

  * Top countries & regions
  * Trends over time
  * Gender-based comparison
  * Obesity vs Malnutrition correlation

---

### 6️⃣ Power BI Dashboard

* 15+ visualizations created:

  * Line charts (trend analysis)
  * Bar charts (comparisons)
  * Maps (geographical insights)
  * Scatter plots (relationship analysis)
  * Pie charts (distribution)

---

## 📊 Key Insights

* Obesity is steadily increasing globally 📈
* Malnutrition remains high in developing regions 🌍
* Some countries face **both obesity & malnutrition simultaneously**
* Gender differences observed in both conditions
* Regional disparities highlight economic and lifestyle factors

---

## 🚀 How to Run

### Step 1: Install dependencies

```
pip install pandas psycopg sqlalchemy matplotlib seaborn pycountry
```

### Step 2: Run pipeline

```
python who_nutrition_analysis.py
python who_nutrition_cleaning.py
python who_sql_insert.py
```

### Step 3: Run SQL queries

* Use pgAdmin / VS Code / psql

### Step 4: Open Power BI

* Connect to PostgreSQL
* Load tables
* Build dashboard

---

## 📈 Output

* Clean datasets
* SQL insights
* Interactive Power BI dashboard

---

## 💡 Future Improvements

* Add machine learning predictions
* Automate pipeline using Airflow
* Deploy dashboard online

---

## 👨‍💻 Author

Aparna V

---

## 📜 License

This project is for educational purposes.
