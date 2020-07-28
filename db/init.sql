CREATE DATABASE numberData;
use numberData;

CREATE TABLE IF NOT EXISTS numberImport (

    `id` INT,
    `num1` NUMERIC(5, 2),
    `num2` NUMERIC(5, 2),
    `result` NUMERIC(5, 2)
   );
INSERT INTO numberImport (id, num1, num2, result) VALUES
    (1, 65.78, 5, 112.99);
