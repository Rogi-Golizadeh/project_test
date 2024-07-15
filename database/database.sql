DROP DATABASE IF EXISTS `Surf_club`;
CREATE DATABASE IF NOT EXISTS `Surf_club`;
USE `Surf_club`;

CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    dni VARCHAR(9) NOT NULL UNIQUE,
    email VARCHAR(50) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    password CHAR(40) NOT NULL
);

CREATE TABLE equipos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    isbn VARCHAR(20) NOT NULL UNIQUE,
    titulo VARCHAR(50) NOT NULL,
    color VARCHAR(50) NOT NULL
);

CREATE TABLE prestamos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_equipo INT NOT NULL,
    fecha_prestamo DATE NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_equipo) REFERENCES equipos(id)
);

SELECT NOW();
