-- Definición de la tabla "usuarios"
CREATE TABLE Tabla_usuarios (
    id SERIAL PRIMARY KEY,  -- Crea una columna que se crea automáticamente incrementándose en 1 cada vez que se añade un componente a la base de datos.
    nombreUsuario VARCHAR(100),
    correoUsuario VARCHAR(100)
);

-- Cada usuario registrado tiene asociado un ID en la tabla "usuarios". Este ID será el utilizado para registrar
-- los mensajes de los distintos usuarios en la tabla mensajes

-- Definición de la tabla "mensajes"
CREATE TABLE Tabla_mensajes (
    id SERIAL PRIMARY KEY,
    IDusuario INT,
    mensaje TEXT,
    fecha TEXT
);