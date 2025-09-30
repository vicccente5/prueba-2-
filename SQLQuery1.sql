CREATE DATABASE veterinario;
GO

USE veterinario;
GO

CREATE TABLE Due�o (
    id_due�o int PRIMARY KEY,
    nombre NVARCHAR(100),
    direccion NVARCHAR(100), telefono varchar(50),email nvarchar(100)
);

CREATE TABLE Mascota (
    id_mascota INT PRIMARY KEY,
    nombre NVARCHAR(100),
    especie NVARCHAR(50),
    raza NVARCHAR(50),
    fecha_nacimiento date,
    id_due�o INT NOT NULL,
    CONSTRAINT fk_mascota_due�o FOREIGN KEY (id_due�o) -- �Correcci�n aqu�!
    REFERENCES Due�o(id_due�o)
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
