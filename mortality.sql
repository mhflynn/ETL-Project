drop database mortality;

create database mortality;


use mortality;

-- ---------------- This is the ouput form python ------------------------------------

CREATE TABLE  IF NOT EXISTS age_recode_52( 
ckey VARCHAR(255) NOT NULL PRIMARY KEY, 
cvalue VARCHAR(1024) ); 

 CREATE TABLE  IF NOT EXISTS age_recode_27( 
 ckey VARCHAR(255) NOT NULL PRIMARY KEY, 
 cvalue VARCHAR(1024) );  
 
 CREATE TABLE  IF NOT EXISTS age_recode_12( 
 ckey VARCHAR(255) NOT NULL PRIMARY KEY, 
 cvalue VARCHAR(1024) );  
 
 CREATE TABLE  IF NOT EXISTS infant_age_recode_22( 
 ckey VARCHAR(255) NOT NULL PRIMARY KEY, 
 cvalue VARCHAR(1024) );


CREATE TABLE  IF NOT EXISTS person( 
id INT PRIMARY KEY NOT NULL, 
fk_age_recode_52 VARCHAR(255) DEFAULT '',  
	CONSTRAINT fk_age_recode_52 FOREIGN KEY (fk_age_recode_52) REFERENCES age_recode_52(ckey) ON DELETE NO ACTION ON UPDATE CASCADE,
fk_age_recode_27 VARCHAR(255) DEFAULT '',  
	CONSTRAINT cfk_age_recode_27 FOREIGN KEY (fk_age_recode_27) REFERENCES age_recode_27(ckey) ON DELETE NO ACTION ON UPDATE CASCADE,
fk_age_recode_12 VARCHAR(255) DEFAULT '',  
	CONSTRAINT cfk_age_recode_12 FOREIGN KEY (fk_age_recode_12) REFERENCES age_recode_12(ckey) ON DELETE NO ACTION ON UPDATE CASCADE,
fk_infant_age_recode_22 VARCHAR(255) DEFAULT '',  
	CONSTRAINT cfk_infant_age_recode_22 FOREIGN KEY (fk_infant_age_recode_22) REFERENCES infant_age_recode_22(ckey) ON DELETE NO ACTION ON UPDATE CASCADE);

-- ----- ------------------------------------ ------------------------------------ ------------------------------------ ------------------------------------ ------------------------------------
-- This query for exrernal MySQL USER with no acces to data files

-- ----- ------------------------------------ ------------------------------------ ------------------------------------ ------------------------------------ ------------------------------------

-- QUERY TO RETURN MAPPED COLUMNS:
SELECT p.id, ar52.cvalue AS 'RECODE 52', ar27.cvalue AS 'RECODE 27', ar12.cvalue AS 'RECODE 12', iar22.cvalue AS 'INFANT RECODE 22'
	FROM person AS p 
		LEFT JOIN age_recode_52 AS ar52 ON p.fk_age_recode_52 = ar52.ckey
	   JOIN age_recode_27 AS ar27 ON p.fk_age_recode_27 = ar27.ckey
		JOIN age_recode_12 AS ar12 ON p.fk_age_recode_12 = ar12.ckey
	   LEFT JOIN infant_age_recode_22 AS iar22 ON p.fk_infant_age_recode_22= iar22.ckey;







-- ----- ------------------------------------ ------------------------------------ ------------------------------------ ------------------------------------ ------------------------------------
-- This table would be tyhe structure for already mapped  data for refrence
-- ----- ------------------------------------ ------------------------------------ ------------------------------------ ------------------------------------ ------------------------------------

CREATE TABLE  IF NOT EXISTS mapped_person( 
id INT PRIMARY KEY NOT NULL, resident_status VARCHAR(1024) , 
education_1989_revision VARCHAR(1024), 
education_2003_revision VARCHAR(1024), 
education_reporting_flag VARCHAR(1024), 
month_of_death VARCHAR(1024), 
sex VARCHAR(1024), 
detail_age_type VARCHAR(1024), 
detail_age VARCHAR(1024), 
age_recode_52 VARCHAR(1024), 
age_recode_27 VARCHAR(1024), 
age_recode_12 VARCHAR(1024), 
infant_age_recode_22 VARCHAR(1024),
place_of_death_and_decedents_status VARCHAR(1024), 
marital_status VARCHAR(1024), 
day_of_week_of_death VARCHAR(1024), 
current_data_year VARCHAR(1024), 
injury_at_work VARCHAR(1024), 
manner_of_death VARCHAR(1024), 
method_of_disposition VARCHAR(1024), 
autopsy VARCHAR(1024), 
activity_code VARCHAR(1024), 
place_of_injury_for_causes_w00_y34_except_y06_and_y07_ VARCHAR(1024), 
icd_code_10th_revision VARCHAR(1024), 
358_cause_recode VARCHAR(1024), 
113_cause_recode VARCHAR(1024), 
130_infant_cause_recode VARCHAR(1024),
 39_cause_recode VARCHAR(1024), 
 number_of_entity_axis_conditions VARCHAR(1024), 
 entity_condition_1 VARCHAR(1024), 
 entity_condition_2 VARCHAR(1024), 
 number_of_record_axis_conditions VARCHAR(1024), 
 record_condition_1 VARCHAR(1024), 
 record_condition_2 VARCHAR(1024), 
 race VARCHAR(1024), 
 bridged_race_flag VARCHAR(1024), 
 race_imputation_flag VARCHAR(1024), 
 race_recode_3 VARCHAR(1024), 
 race_recode_5 VARCHAR(1024),
 hispanic_origin VARCHAR(1024), 
 hispanic_originrace_recode VARCHAR(1024));


