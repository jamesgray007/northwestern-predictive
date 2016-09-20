-- 7. Show all PlanetVisits where the length of the visit >= 4 stardates. 

SELECT planetID, starshipID, departureStarDate - arrivalStarDate AS visitLength FROM PlanetVisit
	WHERE (departureStarDate - arrivalStarDate) >= 4;