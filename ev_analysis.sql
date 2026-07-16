
CREATE DATABASE ev_project ;
USE ev_project ;

SELECT COUNT(*) AS total_row FROM ev_adoption ;

SELECT * FROM ev_adoption LIMIT 5;

# QUERY 1 --"Which city type (Urban, Suburban, Rural) has the highest EV adoption rate?"
SELECT 
    city_type, 
    ev_adoption_likelihood, 
    COUNT(*) as total
FROM ev_adoption
GROUP BY city_type, ev_adoption_likelihood
ORDER BY total DESC;

# QUERY 2 --"What is the average annual income of people grouped by their EV adoption likelihood (High, Medium, Low)?
SELECT 
    ev_adoption_likelihood,
    ROUND(AVG(annual_income), 2) AS avg_income
FROM ev_adoption
GROUP BY ev_adoption_likelihood
ORDER BY avg_income DESC;

# QUERY 3 - How many people own each type of vehicle (Hatchback, Sedan, SUV etc.)
SELECT 
     current_vehicle_type,
     COUNT(*) AS total_people
FROM ev_adoption 
GROUP BY current_vehicle_type ;

# QUERY 4 --"Which education level has the highest average EV knowledge score?"
SELECT education_level , AVG( ev_knowledge_score) 
FROM ev_adoption 
WHERE education_level IS NOT NULL
GROUP BY education_level  
ORDER BY AVG(ev_knowledge_score) DESC 
LIMIT 1 ;

# QUERY 5 --"What is the average fuel expense per month for each city type?"
SELECT AVG(fuel_expense_per_month ), city_type 
FROM ev_adoption 
GROUP BY city_type;


# QUERY 6 --"Which vehicle type has the highest average monthly charging cost?"
SELECT current_vehicle_type , AVG(monthly_charging_cost) AS avg_monthly_charging_cost 
FROM ev_adoption 
GROUP BY current_vehicle_type 
ORDER BY avg_monthly_charging_cost DESC
LIMIT 1 ;
 

# QUERY 7 --"Find the top 5 combinations of city type and education level that have the highest number of people with High EV adoption likelihood"
SELECT city_type , education_level , COUNT(*) AS ev_user 
FROM ev_adoption 
WHERE ev_adoption_likelihood = 'High' 
GROUP BY city_type , education_level 
ORDER BY ev_user DESC
LIMIT 5 ;

# QUERY 8 --"Find all people whose annual income is above the average annual income of the entire dataset"
SELECT age , city_type , education_level ,current_vehicle_type 
FROM ev_adoption 
WHERE annual_income > (
       SELECT AVG(annual_income)
       FROM ev_adoption ) 
ORDER BY annual_income DESC 
	 ;

# QUERY 9 --"Find the city type that has above average charging station accessibility"
SELECT DISTINCT city_type 
FROM ev_adoption 
WHERE charging_station_accessibility > (
        SELECT AVG(charging_station_accessibility)
        FROM ev_adoption );


# QUERY 10 --"Find people who have a higher EV knowledge score than the average EV knowledge score of their own city type"
SELECT e1.city_type , e1.ev_knowledge_score 
FROM ev_adoption e1 
WHERE e1.ev_knowledge_score > (
          SELECT AVG(e2.ev_knowledge_score)
          FROM ev_adoption e2
          WHERE e2.city_type = e1.city_type )
          ;

# QUERY 11 --"Rank each city type based on average annual income, with rank 1 being the highest income"
SELECT 
    city_type,
    ROUND(AVG(annual_income), 2) AS avg_annual_income,
    RANK() OVER (ORDER BY AVG(annual_income) DESC) AS income_rank
FROM ev_adoption
GROUP BY city_type;

# QUERY 12 --"Rank customers within each city type based on their fuel expense per month, highest first. Show city type, fuel expense and their rank"
SELECT city_type , fuel_expense_per_month ,
  RANK() OVER (PARTITION BY city_type ORDER BY fuel_expense_per_month  DESC)
FROM ev_adoption ;


# QUERY 13 --"For each vehicle type, assign a row number to each person ordered by their EV knowledge score highest first"
SELECT current_vehicle_type , ev_knowledge_score ,
  ROW_NUMBER() OVER (PARTITION BY current_vehicle_type ORDER BY ev_knowledge_score DESC) 
FROM ev_adoption ;

# QUERY 14 --"Find the top 3 people with highest annual income within each education level using DENSE_RANK"
SELECT * FROM (
    SELECT 
        education_level, 
        annual_income,
        DENSE_RANK() OVER (PARTITION BY education_level ORDER BY annual_income DESC) AS income_rank
    FROM ev_adoption
    WHERE education_level IS NOT NULL
) AS ranked
WHERE income_rank <= 3;


# QUERY 15 --"Find the top 2 people with highest fuel expense within each city type using ROW_NUMBER"
SELECT * FROM (
    SELECT 
        fuel_expense_per_month, 
        city_type,
        ROW_NUMBER() OVER (PARTITION BY city_type ORDER BY fuel_expense_per_month DESC) AS indivisuial_fuel_expense
    FROM ev_adoption
    WHERE fuel_expense_per_month IS NOT NULL
) AS ranked
WHERE indivisuial_fuel_expense <= 2;


# QUERY 16 --"Show each person's annual income and the average annual income of their city type side by side, along with the difference between the two"
SELECT city_type, annual_income,
  ROUND(AVG(annual_income) OVER (PARTITION BY city_type), 2) AS avg_city_income,
  ROUND(annual_income - AVG(annual_income) OVER (PARTITION BY city_type), 2) AS income_difference
FROM ev_adoption;


CREATE TABLE city_detail (
    city_type VARCHAR(50),
    ev_infrastructure_score INT,
    govt_ev_support VARCHAR(20),
    avg_electricity_cost DECIMAL(5,2),
    charging_stations_count INT,
    ev_policy_rating VARCHAR(20)
);

INSERT INTO city_detail VALUES
('Urban', 9, 'High', 0.12, 500, 'Excellent'),
('Suburban', 6, 'Medium', 0.14, 200, 'Good'),
('Rural', 3, 'Low', 0.18, 50, 'Poor');


SELECT * FROM city_detail ;

# Query 17 --"Join ev_adoption and city_detail tables to show each person's city type, annual income, government EV support level and EV infrastructure score for their city"
SELECT e.city_type, e.annual_income, c.govt_ev_support, c.ev_infrastructure_score
FROM ev_adoption e
INNER JOIN city_detail c
ON e.city_type = c.city_type;

# QUERY 18 --"Show each city type, its average annual income, charging stations count and EV infrastructure score — joining both tables"
SELECT e.city_type , AVG(e.annual_income) , c.charging_stations_count, c.ev_infrastructure_score 
FROM ev_adoption e
INNER JOIN city_detail c 
ON e.city_type = c.city_type
GROUP BY e.city_type , c.charging_stations_count , c.ev_infrastructure_score   ;
