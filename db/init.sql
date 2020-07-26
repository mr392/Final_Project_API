CREATE DATABASE numberData;
use numberData;

CREATE TABLE IF NOT EXISTS tblPeopleImport (


    `num1` NUMERIC(5, 2),
    `num2` NUMERIC(5, 2),
    `result` NUMERIC(5, 2)
    );
INSERT INTO tblPeopleImport (num1, num2, result) VALUES
    (65.78, 5, 112.99);
