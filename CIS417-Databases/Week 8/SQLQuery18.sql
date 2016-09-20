--	18. Union the name of every starship in the ‘Admiral’ class with the name of every planet with a radius > 3000.

SELECT starshipName AS StarshipPlanetUnion
	FROM Starship s
	WHERE s.shipClass = 'Admiral'
	UNION 
	SELECT planetName 
	FROM Planet p
	WHERE p.radius > 3000; 
