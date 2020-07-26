CREATE DATABASE peopleData;
use peopleData;

CREATE TABLE IF NOT EXISTS tblPeopleImport (

    `person_num` INT,
    `Height` NUMERIC(5, 2),
    `Weight` NUMERIC(5, 2),
    `result` NUMERIC(5, 2),

    PRIMARY KEY (`person_num`)
);
INSERT INTO tblPeopleImport (person_num, height, weight, result) VALUES
    (1, 65.78, 5, 112.99);
