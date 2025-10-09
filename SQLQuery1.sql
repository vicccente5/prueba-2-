
-- Tabla Dueno (debe existir antes si no la tienes ya)
CREATE TABLE Dueno (
  id_dueno INT PRIMARY KEY,nombre NVARCHAR2(100) NOT NULL,
  direccion NVARCHAR2(100),telefono VARCHAR2(50),email NVARCHAR2(100)
);

-- Tabla Mascota
CREATE TABLE Mascota (
  id_mascota INT PRIMARY KEY,nombre NVARCHAR2(100) NOT NULL,especie NVARCHAR2(50),
  raza NVARCHAR2(50),fecha_nacimiento DATE,id_dueno INT NOT NULL,
  CONSTRAINT fk_mascota_dueno FOREIGN KEY (id_dueno)REFERENCES Dueno(id_dueno) ON DELETE CASCADE
);

-- Tabla Veterinario
CREATE TABLE Veterinario (
  id_veterinario INT PRIMARY KEY,nombre NVARCHAR2(100) NOT NULL,
  especialidad NVARCHAR2(100),telefono VARCHAR2(50),email NVARCHAR2(100)
);

-- Tabla Consulta
CREATE TABLE Consulta (
  id_consulta INT PRIMARY KEY,fecha_consulta DATE DEFAULT SYSDATE NOT NULL,motivo NVARCHAR2(200),
  diagnostico NVARCHAR2(200),tratamiento NVARCHAR2(200),observaciones NVARCHAR2(300),
  id_mascota INT NOT NULL,id_veterinario INT,
  CONSTRAINT fk_consulta_mascota FOREIGN KEY (id_mascota) REFERENCES Mascota(id_mascota) ON DELETE CASCADE,
  CONSTRAINT fk_consulta_veterinario FOREIGN KEY (id_veterinario) REFERENCES Veterinario(id_veterinario)
);

