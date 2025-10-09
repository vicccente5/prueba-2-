# prueba-2 Caso 5 – Clínica Veterinaria

# ----------------------------------------------------------------
Se comenzo por la base de datos debido a que se tuvieron complicaciones con la aplicacion de base de datos al vincularla con el visual asi que decidimos empezar a avanza con la base de datos por que empezar por el codigo pensamos que iba a ser algo enrredado debido a que no pudimos conectarlo a la base de datos.

se agrego el archivo conexion_estudiante.py el cual se utilizara como base para empezar la conexion con la base de datos de la veterinaria.

# ----------------------------------------------------------------

se modifico el archivo conexion_estudiante.py paso a ser el archivo veterinaria.py se hizo un renombramiento y Adaptación de Funciones para que sean acordes al tema y a la base de datos se creo una nueva interfaz de usuario y Menú para que sea acorde de el tema que se solicito, las consutas sql fueron modificadas para que se ingresen los datos acorde de la base de datos creada.
se comento dentro del codigo el que hace cada cosa

# ----------------------------------------------------------------

se logro entablar una buena conexion con una base de datos pero se tubo que cambiar de aplicacion de base de datos se paso a utilizar la aplicacion oracle sql se tiene que mejorar mucho el codigo por que devido a que se cambio de base de datos se tiene que modificar vastante el codigo y poner verificaciones pero se va por buen camino


## Librerías necesarias

```bash
pip install pyodbc python-dotenv
```

## Archivos del proyecto

- `.env`: Variables de entorno con credenciales de conexión.
- `veterinaria.py`: Script interactivo en consola para listar y agregar estudiantes.
- `SQLQUERY1.sql`: Script SQL para crear la base de datos `veterinario` y las tablas.
