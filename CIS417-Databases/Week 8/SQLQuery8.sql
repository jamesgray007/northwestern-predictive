--	8. List the planet, starship, and length of stay for each planet visit.

SELECT planetName, starshipName, departureStarDate - arrivalStarDate AS lengthOfStay
	FROM PlanetVisit v INNER JOIN Planet p
	ON v.planetID = p.planetID 
	INNER JOIN Starship s
	ON s.starshipID = v.starshipID;