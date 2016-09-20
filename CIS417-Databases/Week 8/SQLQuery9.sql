-- 	9. Show all PlanetVisits to planets with planetIDs 1, 2, and 5, sorted by planetID and starshipID. 

SELECT * FROM PlanetVisit
	WHERE planetID IN ('1', '2', '5')
	ORDER BY planetID, starshipID;