-- Data Links
-- Artists  : https://github.com/MuseumofModernArt/collection/blob/master/Artists.csv
-- Artworks : https://github.com/MuseumofModernArt/collection/blob/master/Artworks.csv

####################################################################################
####################################################################################

-- UNIQUE NUMBER OF EXHIBITS PER DEPARTMENT 

SELECT DISTINCT Department, Count(*) as '# of Exhibits'
FROM MoMA_Artworks
GROUP BY Department
ORDER BY COUNT(Department) DESC

-- TOTAL NUMBER OF ARTWORKS EXHIBITED FOR EACH ARTIST

SELECT Artist, COUNT(*) as 'Total_Artworks'
FROM MoMA_Artworks
WHERE Artist is NOT NULL
GROUP BY Artist

-- TOP 5 MOST REPRESENTED ARTISTs 

SELECT Artist, COUNT(Artist) as 'Total_Artwork'
FROM MoMA_Artworks
WHERE Artist is NOT NULL
GROUP BY Artist
ORDER BY COUNT(Artist) DESC
LIMIT 5 

-- MOST REPRESENTED NATIONALITY

SELECT Nationality, COUNT(*) as 'Total'
FROM MoMA_Artists 
GROUP BY Nationality
ORDER BY COUNT(Nationality) DESC

-- MOST REPRESENTED GENDER 

SELECT Gender, COUNT(*) as 'Total' 
FROM MoMA_Artists
GROUP BY Gender

-- MOST EXHIBITED MEDIUMS  

SELECT Medium, COUNT(*) as 'Total'
FROM MoMA_Artworks
GROUP BY Medium
ORDER BY COUNT(Medium) DESC

-- MOST EXHIBITED CLASSIFICATIONS

SELECT Classification, COUNT(*) as 'Total'
FROM MoMA_Artworks
GROUP BY Classification
ORDER BY COUNT(Classification) DESC
