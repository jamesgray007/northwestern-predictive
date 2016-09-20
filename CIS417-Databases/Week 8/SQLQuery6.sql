-- 	6. Show all planets with a radius ranging from 2000 to 4000 kilometers, sorted from largest to smallest. 

SELECT * from Planet
	WHERE radius >= 2000 AND radius <= 4000
	ORDER BY radius DESC;