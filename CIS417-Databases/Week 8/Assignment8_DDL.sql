-- James Gray, CIS 417 Assignement #8
-- DDL statements to create and populate tables
-- SQL Server 2012

CREATE TABLE Starship
	-- Starship contains starship details
	(starshipID SMALLINT NOT NULL,
	 starshipName VARCHAR (20) NOT NULL,
	 crewSize SMALLINT NOT NULL,
	 shipClass VARCHAR (20) NOT NULL,
	 launchStarDate SMALLINT NOT NULL,
	 CONSTRAINT pk_starshipID PRIMARY KEY (starshipID)
	 );

CREATE TABLE Planet
	-- Planet contains planet details
	(planetID SMALLINT NOT NULL,
	 planetName VARCHAR (20) NOT NULL,
	 radius SMALLINT NOT NULL,
	 atmosphere VARCHAR (20) NOT NULL,
	 CONSTRAINT pk_planetID PRIMARY KEY (planetID)
	 );

CREATE TABLE PlanetVisit
	-- PlanetVisit contains the details of starships that visit planets
	(planetID SMALLINT NOT NULL,
	 starshipID SMALLINT NOT NULL,
	 arrivalStarDate SMALLINT NOT NULL,
	 departureStarDate SMALLINT NOT NULL,
	 CONSTRAINT pk_planetVisit PRIMARY KEY (planetID, starshipID, arrivalStarDate),
	 CONSTRAINT fk_planetVisit_planetID FOREIGN KEY (planetID) REFERENCES Planet (planetID),	 CONSTRAINT fk_planetVisit_starshipID FOREIGN KEY (starshipID) REFERENCES Starship (starshipID)
	);


-- populate starship table

INSERT INTO Starship (starshipID, starshipName, crewSize, shipClass, launchStarDate) VALUES ('351','Stingray','200','StellarIV', '21450');
INSERT INTO Starship (starshipID, starshipName, crewSize, shipClass, launchStarDate) VALUES ('352','Excelsior','200','StellarIV', '21470');
INSERT INTO Starship (starshipID, starshipName, crewSize, shipClass, launchStarDate) VALUES ('400','Odyssey','130', 'LightCruiser','21700');
INSERT INTO Starship (starshipID, starshipName, crewSize, shipClass, launchStarDate) VALUES ('402','Daredevil','128', 'LightCruiser','21550');
INSERT INTO Starship (starshipID, starshipName, crewSize, shipClass, launchStarDate) VALUES ('500','Adventure','85', 'Argon','21523');
INSERT INTO Starship (starshipID, starshipName, crewSize, shipClass, launchStarDate) VALUES ('501','Challenger','80', 'Argon','21553');
INSERT INTO Starship (starshipID, starshipName, crewSize, shipClass, launchStarDate) VALUES ('503','Invincible','75', 'Argon','21537');
INSERT INTO Starship (starshipID, starshipName, crewSize, shipClass, launchStarDate) VALUES ('601','Navigator','1850', 'Explorer','21855');
INSERT INTO Starship (starshipID, starshipName, crewSize, shipClass, launchStarDate) VALUES ('602','Far Journey','1900', 'Explorer','21890');
INSERT INTO Starship (starshipID, starshipName, crewSize, shipClass, launchStarDate) VALUES ('700','Davidson','500', 'Admiral','21600');
INSERT INTO Starship (starshipID, starshipName, crewSize, shipClass, launchStarDate) VALUES ('701','Cochran','500', 'Admiral','21650');

-- populate planet table

INSERT INTO Planet (planetID, planetName,radius, atmosphere) VALUES ('1','Vulcan','3500', 'Nitrogen/Oxygen');
INSERT INTO Planet (planetID, planetName,radius, atmosphere) VALUES ('2','Earth','4000', 'Nitrogen/Oxygen');
INSERT INTO Planet (planetID, planetName,radius, atmosphere) VALUES ('3','Galactus Prime IV','400', 'None');
INSERT INTO Planet (planetID, planetName,radius, atmosphere) VALUES ('4','Sigma Alpha Gamma','2500', 'Methane');
INSERT INTO Planet (planetID, planetName,radius, atmosphere) VALUES ('5','Romulus','4400', 'Nitrogen');
INSERT INTO Planet (planetID, planetName,radius, atmosphere) VALUES ('6','Borg','10000', 'Unknown');

-- populate planetvisit Table

INSERT INTO PlanetVisit (planetID, starshipID, arrivalStarDate, departureStarDate) VALUES ('1','351','22000','22008');
INSERT INTO PlanetVisit (planetID, starshipID, arrivalStarDate, departureStarDate) VALUES ('1','351','22022','22029');
INSERT INTO PlanetVisit (planetID, starshipID, arrivalStarDate, departureStarDate) VALUES ('1','701','22033','22044');
INSERT INTO PlanetVisit (planetID, starshipID, arrivalStarDate, departureStarDate) VALUES ('2','352','22040','22044');
INSERT INTO PlanetVisit (planetID, starshipID, arrivalStarDate, departureStarDate) VALUES ('2','402','22045','22047');
INSERT INTO PlanetVisit (planetID, starshipID, arrivalStarDate, departureStarDate) VALUES ('3','352','22016','22017');
INSERT INTO PlanetVisit (planetID, starshipID, arrivalStarDate, departureStarDate) VALUES ('3','701','22059','22063');
INSERT INTO PlanetVisit (planetID, starshipID, arrivalStarDate, departureStarDate) VALUES ('4','352','22050','22052');
INSERT INTO PlanetVisit (planetID, starshipID, arrivalStarDate, departureStarDate) VALUES ('4','402','22043','22044');
INSERT INTO PlanetVisit (planetID, starshipID, arrivalStarDate, departureStarDate) VALUES ('5','402','22049','22053');
INSERT INTO PlanetVisit (planetID, starshipID, arrivalStarDate, departureStarDate) VALUES ('5','701','22049','22052');
INSERT INTO PlanetVisit (planetID, starshipID, arrivalStarDate, departureStarDate) VALUES ('6','352','22055','22059');