-- 	19. Find the name, crewsize, and shipclass of every starship whose crewsize is larger then the crewsize of every starship of shipclass ‘LightCruiser’.

SELECT starshipName, crewSize, shipClass
	FROM Starship
	WHERE crewSize > (SELECT MAX (crewSize) max_crewSize FROM Starship WHERE shipClass = 'LightCruiser'); 