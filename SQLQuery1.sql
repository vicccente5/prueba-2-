CREATE DATABASE veterinario;
GO

USE veterinario;
GO

CREATE TABLE Dueño (
    id_dueño int PRIMARY KEY,
    nombre NVARCHAR(100),
    direccion NVARCHAR(100), telefono varchar(50),email nvarchar(100)
);

CREATE TABLE Mascota (
    id_mascota INT PRIMARY KEY,
    nombre NVARCHAR(100),
    especie NVARCHAR(50),
    raza NVARCHAR(50),
    fecha_nacimiento date,
    id_dueño INT NOT NULL,
    CONSTRAINT fk_mascota_dueño FOREIGN KEY (id_dueño) -- ¡Corrección aquí!
    REFERENCES Dueño(id_dueño)
    ON DELETE CASCADE
);

CREATE TABLE consulta (
    id_consulta INT PRIMARY KEY,
    fecha_consulta DATE DEFAULT GETDATE() NOT NULL, 
    motivo NVARCHAR(200),
    diagnostico NVARCHAR(200),
    tratamiento NVARCHAR(200),
    id_mascota INT NOT NULL,
    CONSTRAINT fk_consulta_mascota FOREIGN KEY (id_mascota)
    REFERENCES Mascota(id_mascota)
    ON DELETE CASCADE
);
