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
    (1, 65.78, 5, "add",  70.78),
    (2, 25, 4, "multiply", 100),
    (3, 10, 9, "subtract", 1),
    (4, 100, 10, "divide", 10),
    (5, 5, 0, "sqaure", 25),
    (6, 100, 0, "sqrt", 10);


CREATE TABLE IF NOT EXISTS statsImport (

    `id` INT AUTO_INCREMENT,
    `num1` NUMERIC(10, 4),
    `num2` NUMERIC(10, 4),
    `num3` NUMERIC(10, 4),
    `num4` NUMERIC(10, 4),
    `num5` NUMERIC(10, 4),
    `num6` NUMERIC(10, 4),
    `operation` VARCHAR (20),
    `result` NUMERIC(5, 2),
    PRIMARY KEY (`id`)
   );
INSERT INTO statsImport (id, num1, num2,num3,num4,num5,num6, operation, result) VALUES
    (1, 1, 65.78, 5, 2.2, 9.0, 6.7, "mean",  70.78),
    (2, 2, 3, 4, 5, 6, 7, "mean", 4);