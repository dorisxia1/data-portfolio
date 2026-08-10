CREATE DATABASE chatdb_relational;
USE chatdb_relational;

-- Example table definitions (simplified):
CREATE TABLE City (
    city_id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100),
    state_name VARCHAR(100),
    population_2020 INT,
    population_2010 INT,
    land_area_sqmi FLOAT,
    density FLOAT
);
CREATE TABLE HouseholdType (
    household_id INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(100)
);
CREATE TABLE LivingWage (
    livingwage_id INT AUTO_INCREMENT PRIMARY KEY,
    city_id INT,
    household_id INT,
    wage DECIMAL(5,2),
    FOREIGN KEY (city_id) REFERENCES City(city_id),
    FOREIGN KEY (household_id) REFERENCES HouseholdType(household_id)
);
CREATE TABLE PovertyGroup (
    group_id INT AUTO_INCREMENT PRIMARY KEY,
    group_name VARCHAR(100)
);
CREATE TABLE YearlyPovertyThresholds (
    year INT PRIMARY KEY,
    annual_poverty_wage INT,
    hourly_poverty_wage DECIMAL(5,2)
);
CREATE TABLE PovertyWageDistribution (
    pwd_id INT AUTO_INCREMENT PRIMARY KEY,
    year INT,
    group_id INT,
    percentage DECIMAL(4,1),
    FOREIGN KEY (year) REFERENCES YearlyPovertyThresholds(year),
    FOREIGN KEY (group_id) REFERENCES PovertyGroup(group_id)
);
