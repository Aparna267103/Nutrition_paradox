-- ==============================
-- 🔢 OBESITY QUERIES (10)
-- ==============================

-- 1. Top 5 regions with highest avg obesity in 2022
SELECT Region, AVG(Mean_Estimate) AS avg_obesity
FROM obesity
WHERE Year = 2022
GROUP BY Region
ORDER BY avg_obesity DESC
LIMIT 5;

-- 2. Top 5 countries with highest obesity
SELECT Country, AVG(Mean_Estimate) AS avg_obesity
FROM obesity
GROUP BY Country
ORDER BY avg_obesity DESC
LIMIT 5;

-- 3. Obesity trend in India
SELECT Year, AVG(Mean_Estimate) AS obesity_trend
FROM obesity
WHERE Country = 'India'
GROUP BY Year
ORDER BY Year;

-- 4. Average obesity by gender
SELECT Gender, AVG(Mean_Estimate) AS avg_obesity
FROM obesity
GROUP BY Gender;

-- 5. Country count by obesity level & age group
SELECT Obesity_level, age_group, COUNT(DISTINCT Country) AS country_count
FROM obesity
GROUP BY Obesity_level, age_group;

-- 6. Least reliable (high CI) & most consistent (low CI)
-- Top 5 highest CI
SELECT Country, AVG(CI_Width) AS avg_ci
FROM obesity
GROUP BY Country
ORDER BY avg_ci DESC
LIMIT 5;

-- Top 5 lowest CI
SELECT Country, AVG(CI_Width) AS avg_ci
FROM obesity
GROUP BY Country
ORDER BY avg_ci ASC
LIMIT 5;

-- 7. Average obesity by age group
SELECT age_group, AVG(Mean_Estimate) AS avg_obesity
FROM obesity
GROUP BY age_group;

-- 8. Top 10 consistent low obesity countries
SELECT Country,
       AVG(Mean_Estimate) AS avg_obesity,
       AVG(CI_Width) AS avg_ci
FROM obesity
GROUP BY Country
HAVING AVG(Mean_Estimate) < 25 AND AVG(CI_Width) < 3
ORDER BY avg_obesity ASC
LIMIT 10;

-- 9. Female obesity higher than male (same year)
SELECT o1.Country, o1.Year,
       o1.Mean_Estimate AS female,
       o2.Mean_Estimate AS male,
       (o1.Mean_Estimate - o2.Mean_Estimate) AS difference
FROM obesity o1
JOIN obesity o2
ON o1.Country = o2.Country AND o1.Year = o2.Year
WHERE o1.Gender = 'Female' AND o2.Gender = 'Male'
AND o1.Mean_Estimate > o2.Mean_Estimate
ORDER BY difference DESC;

-- 10. Global average obesity per year
SELECT Year, AVG(Mean_Estimate) AS global_avg
FROM obesity
GROUP BY Year
ORDER BY Year;

-- ==============================
-- 👾 MALNUTRITION QUERIES (10)
-- ==============================

-- 1. Avg malnutrition by age group
SELECT age_group, AVG(Mean_Estimate) AS avg_malnutrition
FROM malnutrition
GROUP BY age_group;

-- 2. Top 5 countries highest malnutrition
SELECT Country, AVG(Mean_Estimate) AS avg_malnutrition
FROM malnutrition
GROUP BY Country
ORDER BY avg_malnutrition DESC
LIMIT 5;

-- 3. Trend in African region
SELECT Year, AVG(Mean_Estimate) AS trend
FROM malnutrition
WHERE Region = 'Africa'
GROUP BY Year
ORDER BY Year;

-- 4. Gender-based malnutrition
SELECT Gender, AVG(Mean_Estimate) AS avg_malnutrition
FROM malnutrition
GROUP BY Gender;

-- 5. Avg CI width by level & age group
SELECT Malnutrition_level, age_group,
       AVG(CI_Width) AS avg_ci
FROM malnutrition
GROUP BY Malnutrition_level, age_group;

-- 6. Yearly change (India, Nigeria, Brazil)
SELECT Country, Year, AVG(Mean_Estimate) AS trend
FROM malnutrition
WHERE Country IN ('India', 'Nigeria', 'Brazil')
GROUP BY Country, Year
ORDER BY Country, Year;

-- 7. Regions with lowest malnutrition
SELECT Region, AVG(Mean_Estimate) AS avg_malnutrition
FROM malnutrition
GROUP BY Region
ORDER BY avg_malnutrition ASC
LIMIT 5;

-- 8. Countries with increasing malnutrition
SELECT Country,
       MIN(Mean_Estimate) AS early_value,
       MAX(Mean_Estimate) AS recent_value
FROM malnutrition
GROUP BY Country
HAVING MAX(Mean_Estimate) - MIN(Mean_Estimate) > 0;

-- 9. Min/Max year-wise comparison
SELECT Year,
       MIN(Mean_Estimate) AS min_value,
       MAX(Mean_Estimate) AS max_value
FROM malnutrition
GROUP BY Year
ORDER BY Year;

-- 10. High CI Width flags
SELECT *
FROM malnutrition
WHERE CI_Width > 5;

-- ==============================
-- 🔗 COMBINED QUERIES (5)
-- ==============================

-- 1. Obesity vs malnutrition (5 countries)
SELECT o.Country,
       AVG(o.Mean_Estimate) AS obesity,
       AVG(m.Mean_Estimate) AS malnutrition
FROM obesity o
JOIN malnutrition m
ON o.Country = m.Country AND o.Year = m.Year
WHERE o.Country IN ('India', 'United States', 'Brazil', 'China', 'Nigeria')
GROUP BY o.Country;

-- 2. Gender disparity
SELECT o.Gender,
       AVG(o.Mean_Estimate) AS obesity,
       AVG(m.Mean_Estimate) AS malnutrition
FROM obesity o
JOIN malnutrition m
ON o.Country = m.Country AND o.Year = m.Year AND o.Gender = m.Gender
GROUP BY o.Gender;

-- 3. Region-wise (Africa vs Americas)
SELECT o.Region,
       AVG(o.Mean_Estimate) AS obesity,
       AVG(m.Mean_Estimate) AS malnutrition
FROM obesity o
JOIN malnutrition m
ON o.Country = m.Country AND o.Year = m.Year
WHERE o.Region IN ('Africa', 'Americas Region')
GROUP BY o.Region;

-- 4. Countries obesity up & malnutrition down
SELECT o.Country
FROM
(SELECT Country, MIN(Mean_Estimate) AS min_o, MAX(Mean_Estimate) AS max_o
 FROM obesity GROUP BY Country) o
JOIN
(SELECT Country, MIN(Mean_Estimate) AS min_m, MAX(Mean_Estimate) AS max_m
 FROM malnutrition GROUP BY Country) m
ON o.Country = m.Country
WHERE (o.max_o - o.min_o) > 0
AND (m.max_m - m.min_m) < 0;

-- 5. Age-wise trend
SELECT o.age_group,
       AVG(o.Mean_Estimate) AS obesity,
       AVG(m.Mean_Estimate) AS malnutrition
FROM obesity o
JOIN malnutrition m
ON o.Country = m.Country AND o.Year = m.Year AND o.age_group = m.age_group
GROUP BY o.age_group;