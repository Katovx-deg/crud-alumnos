-- Ejecuta este script en MySQL Workbench o en la terminal de MySQL
-- antes de correr la app Flask.

CREATE DATABASE IF NOT EXISTS taller_alumnos
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE taller_alumnos;

CREATE TABLE IF NOT EXISTS alumnos (
    id       INT          AUTO_INCREMENT PRIMARY KEY,
    nombre   VARCHAR(80)  NOT NULL,
    apellido VARCHAR(80)  NOT NULL,
    edad     TINYINT      NOT NULL,
    correo   VARCHAR(120) NOT NULL UNIQUE
);


INSERT INTO alumnos (nombre, apellido, edad, correo) VALUES
    ('Ana',    'García',   20, 'ana.garcia@mail.com'),
    ('Luis',   'Pérez',    22, 'luis.perez@mail.com'),
    ('María',  'López',    19, 'maria.lopez@mail.com');