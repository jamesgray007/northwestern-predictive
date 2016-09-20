-- 	4. Show all Starships launched after stardate 21500, sorted by shipClass and name.

SELECT starshipName, crewSize, shipClass, launchStarDate FROM Starship
	WHERE launchStarDate > 21500 
	ORDER BY shipClass, starshipName;