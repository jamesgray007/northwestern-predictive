-- 	5. Show all Starships except those in the 'Argon' class, sorted by launchStardate.

SELECT * FROM Starship
	WHERE NOT (shipClass = 'Argon')
	ORDER BY launchStardate; 