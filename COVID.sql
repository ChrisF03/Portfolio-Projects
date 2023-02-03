Data Source : https://github.com/owid/covid-19-data/tree/master/public/data

Data used in this analysis is recent as of 1/31/2023
-------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------
SELECT * 
FROM CovidDeaths

SELECT * 
FROM CovidVaccinations

-- SELECTING DATA TO BE USED 

SELECT location, date, total_cases, new_cases, total_deaths, population
FROM CovidDeaths 

-- TOTAL CASES vs TOTAL DEATHS (DEATH PERCENTAGE)
-- SHOWS LIKELIHOOD OF DEATH IN EACH COUNTRY IF COVID IS/WAS CONTRACTED 

SELECT location, date, total_cases, total_deaths, (((total_deaths*1.0)/total_cases)*100) as DeathPercentage 
FROM CovidDeaths 
--WHERE location LIKE '%%'
--UNCOMMENT THE LINE ABOVE^ AND ENTER A LOCATION OF YOUR CHOICE BETWEEN THE PERCENT SIGNS TO FILTER TO IT

-- LOOKING AT TOTAL CASES vs POPULATION (INFECTION RATE)
-- SHOWS WHAT PERCENTAGE OF POPULATION CONTRACTED COVID

SELECT location, date, population, total_cases,(((total_cases*1.0)/population)*100) as InfectionRate 
FROM CovidDeaths 
-- WHERE location LIKE '%%'

-- HIGHEST INFECTION RATE COMPARED TO POPULATION
SELECT location, population, MAX(total_cases) as HighestInfectionCount, MAX(((total_cases*1.0)/population))*100 as InfectionRate 
FROM CovidDeaths 
-- WHERE location LIKE '%%'
GROUP BY location, population 
ORDER BY InfectionRate desc 

-- COUNTRIES WITH HIGHEST DEATH COUNT PER POPULATION
SELECT location, MAX(CAST(total_deaths as int)) as TotalDeathCount
FROM CovidDeaths 
-- WHERE location LIKE '%%'
WHERE continent is NOT NULL
GROUP BY location
ORDER BY TotalDeathCount desc 

-- DEATH COUNT PER CONTINENT
SELECT location, MAX(CAST(total_deaths as int)) as TotalDeathCount
FROM CovidDeaths 
-- WHERE location LIKE '%%'
WHERE continent is NULL
GROUP BY location
ORDER BY TotalDeathCount desc 

-- GLOBAL CHANGE IN DEATH PERCENTAGE BY THE DAY
SELECT date, SUM(total_cases) as Total_Cases, SUM(new_cases)as New_Cases, SUM(CAST(new_deaths as int)) as New_Deaths, SUM(total_deaths) as Total_Deaths, SUM(CAST(new_deaths as int)*1.0)/SUM(new_cases)*100 as DChange_In_Death_Percentage
FROM CovidDeaths
--WHERE location LIKE '%%'
WHERE continent is NOT NULL 
GROUP BY date

-- LOOKING AT TOTAL POPULATION vs VACCINATIONS
SELECT continent, location, date, population, new_vaccinations, SUM(CAST(new_vaccinations as int)) OVER (PARTITION BY location ORDER BY location, date) as rolling_total_vaccinations
FROM CovidDeaths
WHERE continent is NOT NULL 

-- LOOKING AT TOTAL POPULATION vs FULL VACCINATIONS AND BOOSTERS
SELECT dea.continent, dea.location, dea.date, dea.population, vac.people_fully_vaccinated, vac.total_boosters, ((vac.people_fully_vaccinated)*1.0/dea.population)*100 as percent_of_population_fully_vaccinated,((vac.total_boosters*1.0)/dea.population)*100 as percent_of_population_boosted
FROM CovidDeaths as dea
JOIN CovidVaccinations as vac 
on dea.location = vac.location
and dea.date = vac.date
WHERE dea.continent is NOT NULL 

-- USE CTE
WITH POPvsVAC(continent,location, date, population, new_vaccinations, rolling_total_vaccinations)
as
(
SELECT dea.continent, dea.location, dea.date, dea.population, dea.new_vaccinations, SUM(CAST(dea.new_vaccinations as int)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) as rolling_total_vaccinations
FROM CovidDeaths as dea
JOIN CovidVaccinations as vac 
on dea.location = vac.location
and dea.date = vac.date
WHERE dea.continent is NOT NULL 
)
SELECT *,((rolling_total_vaccinations*1.0)/population)*100 as percent_of_population_vaccinated
FROM POPvsVAC
--WHERE location LIKE '%%'

-- TEMP TABLE
CREATE TABLE IF NOT EXISTS PercentOfPopulationVaccinated(
Continent TEXT(255),
Location TEXT(255),
Date TEXT(255),
Population NUMERIC,
New_Vaccinations NUMERIC, 
Rolling_Total_Vaccinations NUMERIC)

INSERT INTO PercentOfPopulationVaccinated
SELECT continent, location, date, population, new_vaccinations, SUM(CAST(new_vaccinations as int)) OVER (PARTITION BY location ORDER BY location, date) as rolling_total_vaccinations
FROM CovidDeaths as dea
--WHERE continent is NOT NULL AND
--WHERE location LIKE '%%'

SELECT *,((Rolling_Total_Vaccinations*1.0)/Population)*100 as percent_of_population_vaccinated
FROM PercentOfPopulationVaccinated

-- CREATING VIEW TO STORE DATA FOR LATER VISUALIZATIONS

CREATE VIEW PercentageOfPopulationVaccinated AS
SELECT continent, location, date, population, new_vaccinations, SUM(CAST(new_vaccinations as int)) OVER (PARTITION BY location ORDER BY location, date) as rolling_total_vaccinations
FROM CovidDeaths as dea
