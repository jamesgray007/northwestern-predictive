-- 	15. Add a constraint to the ‘Moon’ table making planetId a foreign key to the Planet table.

ALTER TABLE Moon
	ADD CONSTRAINT fk_Moon_planetID FOREIGN KEY (planetID) REFERENCES Planet (planetID);