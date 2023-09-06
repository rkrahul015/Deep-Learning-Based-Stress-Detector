CREATE DATABASE IF NOT EXISTS py_charmer_hackfest;

USE py_charmer_hackfest;

CREATE TABLE IF NOT EXISTS employee (  
	ID int AUTO_INCREMENT NOT NULL, 
	user_name varchar(255) UNIQUE,
    first_name varchar(200)NOT NULL,
	last_name varchar(200),
	email varchar(150) UNIQUE NOT NULL,     
	pass_word varchar(100),     
	acc_token text NOT NULL,
    contact varchar(15) NOT NULL,
    reportingTime int NOT NULL,
	PRIMARY KEY(ID) 
);


CREATE TABLE IF NOT EXISTS student (  
	ID int AUTO_INCREMENT NOT NULL, 
	user_name varchar(255) UNIQUE,
    first_name varchar(200)NOT NULL,
	last_name varchar(200),
	email varchar(150) UNIQUE NOT NULL,     
	pass_word varchar(100),     
	acc_token text NOT NULL,
    contact varchar(15) NOT NULL,
    reportingTime int NOT NULL,
	PRIMARY KEY(ID) 
);

-- Select * From py_charmer_hackfest.student
