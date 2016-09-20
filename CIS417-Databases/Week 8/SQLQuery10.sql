-- 	10. Show the average crew size for all starships in each shipClass. The result table should have two columns: 'shipClass' and 'Average Crew'. 

SELECT shipClass, AVG (crewSize) as Average_Crew
	FROM Starship
	GROUP BY shipClass;