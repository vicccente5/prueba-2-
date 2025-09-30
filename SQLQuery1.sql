CREATE DATABASE veterinario;
go


CREATE TABLE Dueno (
id_dueno INT PRIMARY KEY,nombre NVARCHAR(100) NOT NULL,
direccion NVARCHAR(100),telefono VARCHAR(50),email NVARCHAR(100)
);

CREATE TABLE Mascota (
id_mascota INT PRIMARY KEY, nombre NVARCHAR(100) NOT NULL,especie NVARCHAR(50),raza NVARCHAR(50),
fecha_nacimiento DATE,id_dueno INT NOT NULL,
CONSTRAINT fk_mascota_dueno FOREIGN KEY (id_dueno)
REFERENCES Dueno(id_dueno)
ON DELETE CASCADE
);

CREATE TABLE Veterinario (
id_veterinario INT PRIMARY KEY,nombre NVARCHAR(100) NOT NULL,
especialidad NVARCHAR(100),telefono VARCHAR(50),email NVARCHAR(100)
);

CREATE TABLE Consulta (
id_consulta INT PRIMARY KEY,fecha_consulta DATE DEFAULT GETDATE() NOT NULL,motivo NVARCHAR(200),
diagnostico NVARCHAR(200),tratamiento NVARCHAR(200),observaciones NVARCHAR(300),id_mascota INT NOT NULL,
id_veterinario INT,
CONSTRAINT fk_consulta_mascota FOREIGN KEY (id_mascota)
REFERENCES Mascota(id_mascota)
ON DELETE CASCADE,
CONSTRAINT fk_consulta_veterinario FOREIGN KEY (id_veterinario)
REFERENCES Veterinario(id_veterinario)
);



