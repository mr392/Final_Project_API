CREATE DATABASE peopleData;
use peopleData;

CREATE TABLE IF NOT EXISTS tblPeopleImport (
    `index` INT,
    `num1` NUMERIC(5,2),
    `num2` NUMERIC(5, 2),
    `result` NUMERIC(5, 2),

    PRIMARY KEY (`index`)
);
INSERT INTO tblPeopleImport (index, num1, num2, result) VALUES
    (1, 1, 65.78, 112.99),
    (2, 71.52, 136.49),
    (3, 69.40, 153.03),
    (4, 67.76, 114.56),
    (4, 68.02, 123.49),
    (6, 67.66, 123.05);
