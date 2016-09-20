-- 	13. List the details of each planet visit along with the crewsize of the starship making the visit.

SELECT p.planetID, p.planetName, s.starshipID, s.starshipName, v.arrivalStarDate, v.departureStarDate, s.crewSize
	FROM planetVisit v INNER JOIN Starship s
	ON v.starshipID = s.starshipID
	INNER JOIN Planet p
	ON v.planetID = p.planetID;