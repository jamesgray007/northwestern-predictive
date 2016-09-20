-- 	12. Show all Starships whose name has an 'a' as the 2nd character (For example, 'Navigator'). 

SELECT starshipName FROM Starship
	WHERE starshipName LIKE '_a%';