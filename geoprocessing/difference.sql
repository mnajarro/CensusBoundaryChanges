-- This sql script tries to create the difference of two geometry tables within a postgres/postgis database
CREATE TABLE differencetwo (
 	gid int,
 	geoid varchar(255),
 	name varchar(255),
 	namelsad varchar(255),
 	geom geometry	
 );
 INSERT INTO differencetwo (geom)
 SELECT ST_Difference(public."2018uscousub".geom, public."2012_uscousub".geom)
 FROM public."2018uscousub" public."2012_uscousub" 
 