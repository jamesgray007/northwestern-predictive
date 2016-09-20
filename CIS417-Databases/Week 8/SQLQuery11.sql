-- 11. For each Planet, show the number of visits made by all starships. Your result table should have two columns: 'planetID' and 'Num Visits'. 

SELECT planetID, COUNT (planetID) AS 'Num Visits'
	FROM PlanetVisit
	GROUP BY planetID;