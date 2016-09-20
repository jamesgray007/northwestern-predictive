--	14. Create a table ‘Moon’ with the following attributes:  MoonID, name, PlanetID, radius.

CREATE TABLE Moon 
	(MoonID SMALLINT NOT NULL,
	 name VARCHAR (30) NOT NULL,
	 PlanetID SMALLINT NOT NULL,
	 radius SMALLINT NOT NULL
	 CONSTRAINT pk_MoonID PRIMARY KEY (MoonID)
	 );
