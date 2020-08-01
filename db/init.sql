CREATE DATABASE numberData;
use numberData;

CREATE TABLE IF NOT EXISTS numberImport (

    `id` INT AUTO_INCREMENT,
    `num1` NUMERIC(5, 2),
    `num2` NUMERIC(5, 2),
    `operation` VARCHAR (20),
    `result` NUMERIC(5, 2),
    PRIMARY KEY (`id`)
   );
INSERT INTO numberImport (id, num1, num2, operation, result) VALUES
    (1, 65.78, 5, "add",  70.78);

