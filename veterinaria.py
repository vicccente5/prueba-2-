import pyodbc
from dotenv import load_dotenv
import os

class ConexionBD:
    def __init__(self):
        load_dotenv()
        self.servidor = os.getenv("DB_SERVER")
        self.base_datos = os.getenv("DB_NAME")
        self.usuario = os.getenv("DB_USER")
        self.contrasena = os.getenv("DB_PASSWORD")
        self.conexion = None

    def conectar(self):
        try:
            self.conexion = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={self.servidor};'
            f'DATABASE={self.base_datos};'
            f'UID={self.usuario};'
            f'PWD={self.contrasena}')
            print("Conexión exitosa a SQL Server.")
        except Exception as e:
            print("Error al conectar a la base de datos:", e)
            
    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada.")

    def ejecutar_consulta(self, consulta, parametros=()):
        try:
            cursor = self.conexion.cursor()
            cursor.execute(consulta, parametros)
            return cursor.fetchall()
        except Exception as e:
            print("Error al ejecutar la consulta:", e)
            return []

    def ejecutar_instruccion(self, consulta, parametros=()):
        try:
            cursor = self.conexion.cursor()
            cursor.execute(consulta, parametros)
            self.conexion.commit()
            print("Instrucción ejecutada correctamente.")
        except Exception as e:
            print("Error al ejecutar la instrucción:", e)
            self.conexion.rollback()


def mostrar_menu():
    print("\n--- SISTEMA DE GESTIÓN VETERINARIA ---")
    print("1. Registrar Nuevo Dueño")
    print("2. Registrar Nueva Mascota")
    print("3. Registrar Consulta Médica (Agendamiento)")
    print("4. Búsqueda por Nombre (Dueño o Mascota)")
    print("5. Reporte de Historial Clínico por Mascota")
    print("6. Salir")

def registrar_dueno(db):
    """Implementa el registro de un nuevo dueño."""
    print("\n--- REGISTRAR NUEVO DUEÑO ---")
    try:
        id_dueno = input("ID del Dueño (ej: 101): ").strip()
        if not id_dueno.isdigit():
            print("Error: El ID debe ser un número.")
            return

        nombre = input("Nombre completo del Dueño: ").strip()
        if len(nombre) < 3:
            print("Error: El nombre debe tener al menos 3 caracteres.")
            return

        direccion = input("Dirección: ").strip()
        telefono = input("Teléfono: ").strip()
        email = input("Email: ").strip()

        sql = "INSERT INTO Dueno (id_dueno, nombre, direccion, telefono, email) VALUES (?, ?, ?, ?, ?)"
        db.ejecutar_instruccion(sql, (int(id_dueno), nombre, direccion, telefono, email))
    except Exception as e:
        print(f"Ocurrió un error al registrar al dueño: {e}")


def registrar_mascota(db):
    """Implementa el registro de una nueva mascota vinculada a un dueño existente."""
    print("\n--- REGISTRAR NUEVA MASCOTA ---")
    try:
        id_mascota = input("ID de la Mascota (ej: 201): ").strip()
        if not id_mascota.isdigit():
            print("Error: El ID debe ser un número.")
            return

        nombre = input("Nombre de la Mascota: ").strip()
        if len(nombre) < 2:
            print("Error: El nombre debe tener al menos 2 caracteres.")
            return

        especie = input("Especie (Perro, Gato, etc.): ").strip()
        raza = input("Raza: ").strip()
        fecha_nacimiento = input("Fecha de Nacimiento (YYYY-MM-DD): ").strip()
        
        id_dueno = input("ID del Dueño (DEBE EXISTIR): ").strip()
        if not id_dueno.isdigit():
            print("Error: El ID del dueño debe ser un número.")
            return

        # Validación simple de existencia del dueño (opcional, pero recomendable)
        dueno = db.ejecutar_consulta("SELECT nombre FROM Dueno WHERE id_dueno = ?", (int(id_dueno),))
        if not dueno:
            print(f"Error: No se encontró un dueño con ID {id_dueno}. Registre al dueño primero.")
            return

        sql = "INSERT INTO Mascota (id_mascota, nombre, especie, raza, fecha_nacimiento, id_dueno) VALUES (?, ?, ?, ?, ?, ?)"
        db.ejecutar_instruccion(sql, (int(id_mascota), nombre, especie, raza, fecha_nacimiento, int(id_dueno)))
    except Exception as e:
        print(f"Ocurrió un error al registrar la mascota: {e}")


def registrar_consulta(db):
    """Implementa el agendamiento y registro de una consulta médica."""
    print("\n--- REGISTRAR CONSULTA MÉDICA ---")
    try:
        id_consulta = input("ID de la Consulta (ej: 301): ").strip()
        if not id_consulta.isdigit():
            print("Error: El ID debe ser un número.")
            return
            
        id_mascota = input("ID de la Mascota: ").strip()
        if not id_mascota.isdigit():
            print("Error: El ID de la mascota debe ser un número.")
            return

        # Verificar si la mascota existe
        mascota = db.ejecutar_consulta("SELECT nombre FROM Mascota WHERE id_mascota = ?", (int(id_mascota),))
        if not mascota:
            print(f"Error: No se encontró una mascota con ID {id_mascota}.")
            return

        id_veterinario = input("ID del Veterinario (DEBE EXISTIR o dejar vacío para NULL): ").strip()
        if id_veterinario and not id_veterinario.isdigit():
            print("Error: El ID del veterinario debe ser un número.")
            return
        
        # Si se deja vacío, se inserta NULL.
        id_veterinario_param = int(id_veterinario) if id_veterinario else None

        # La fecha de consulta usa DEFAULT GETDATE() en la BD, se puede dejar que la BD la ponga,
        # o pedirla si la consulta es para el futuro (agendamiento).
        # Por simplicidad, permitiremos que la BD use la fecha actual.

        motivo = input("Motivo de la consulta: ").strip()
        diagnostico = input("Diagnóstico: ").strip()
        tratamiento = input("Tratamiento: ").strip()
        observaciones = input("Observaciones: ").strip()

        sql = "INSERT INTO Consulta (id_consulta, id_mascota, id_veterinario, motivo, diagnostico, tratamiento, observaciones) VALUES (?, ?, ?, ?, ?, ?, ?)"
        db.ejecutar_instruccion(sql, (int(id_consulta), int(id_mascota), id_veterinario_param, motivo, diagnostico, tratamiento, observaciones))

    except Exception as e:
        print(f"Ocurrió un error al registrar la consulta: {e}")


def busqueda_por_nombre(db):
    """Busca y muestra información de dueños o mascotas por nombre."""
    print("\n--- BÚSQUEDA POR NOMBRE ---")
    nombre_buscar = input("Ingrese el nombre o parte del nombre (Dueño o Mascota) a buscar: ").strip()
    if not nombre_buscar:
        return

    patron = f"%{nombre_buscar}%"

    print("\n--- Resultados de Búsqueda de Dueños ---")
    sql_dueno = "SELECT id_dueno, nombre, telefono, email FROM Dueno WHERE nombre LIKE ?"
    duenos = db.ejecutar_consulta(sql_dueno, (patron,))
    if duenos:
        for d in duenos:
            print(f"Dueño: ID {d[0]}, Nombre: {d[1]}, Teléfono: {d[2]}, Email: {d[3]}")
    else:
        print("No se encontraron dueños.")

    print("\n--- Resultados de Búsqueda de Mascotas ---")
    # Consulta que incluye el nombre del dueño
    sql_mascota = """
    SELECT 
        M.id_mascota, M.nombre, M.especie, M.raza, D.nombre AS nombre_dueno 
    FROM Mascota M 
    JOIN Dueno D ON M.id_dueno = D.id_dueno
    WHERE M.nombre LIKE ?
    """
    mascotas = db.ejecutar_consulta(sql_mascota, (patron,))
    if mascotas:
        for m in mascotas:
            print(f"Mascota: ID {m[0]}, Nombre: {m[1]}, Especie: {m[2]}, Raza: {m[3]}, Dueño: {m[4]}")
    else:
        print("No se encontraron mascotas.")


def reporte_historial_clinico(db):
    """Genera y muestra el historial clínico de una mascota."""
    print("\n--- REPORTE DE HISTORIAL CLÍNICO ---")
    id_mascota = input("Ingrese el ID de la Mascota para ver su historial: ").strip()

    if not id_mascota.isdigit():
        print("Error: El ID debe ser un número válido.")
        return

    # 1. Información de la Mascota y Dueño
    sql_info = """
    SELECT 
        M.nombre, M.especie, M.raza, M.fecha_nacimiento, D.nombre AS nombre_dueno, D.telefono
    FROM Mascota M
    JOIN Dueno D ON M.id_dueno = D.id_dueno
    WHERE M.id_mascota = ?
    """
    info_mascota = db.ejecutar_consulta(sql_info, (int(id_mascota),))

    if not info_mascota:
        print(f"Error: No se encontró una mascota con ID {id_mascota}.")
        return

    info = info_mascota[0]
    print("\n--- DETALLE DE MASCOTA Y DUEÑO ---")
    print(f"Mascota: {info[0]} (ID: {id_mascota})")
    print(f"Especie/Raza: {info[1]} / {info[2]}")
    print(f"F. Nacimiento: {info[3]}")
    print(f"Dueño: {info[4]} | Teléfono: {info[5]}")

    # 2. Historial de Consultas
    sql_historial = """
    SELECT
        C.fecha_consulta, C.motivo, C.diagnostico, C.tratamiento, C.observaciones, V.nombre AS nombre_veterinario
    FROM Consulta C
    LEFT JOIN Veterinario V ON C.id_veterinario = V.id_veterinario
    WHERE C.id_mascota = ?
    ORDER BY C.fecha_consulta DESC
    """
    historial = db.ejecutar_consulta(sql_historial, (int(id_mascota),))

    print("\n--- HISTORIAL DE CONSULTAS ---")
    if historial:
        for h in historial:
            vet_nombre = h[5] if h[5] else "N/A"
            print("-" * 30)
            print(f"Fecha: {h[0]}")
            print(f"Veterinario: {vet_nombre}")
            print(f"Motivo: {h[1]}")
            print(f"Diagnóstico: {h[2]}")
            print(f"Tratamiento: {h[3]}")
            print(f"Observaciones: {h[4]}")
    else:
        print("No hay consultas registradas para esta mascota.")

# --- Función Principal ---
def main():
    db = ConexionBD()
    db.conectar()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_dueno(db)
        elif opcion == "2":
            registrar_mascota(db)
        elif opcion == "3":
            registrar_consulta(db)
        elif opcion == "4":
            busqueda_por_nombre(db)
        elif opcion == "5":
            reporte_historial_clinico(db)
        elif opcion == "6":
            print("Saliendo del sistema de gestión veterinaria...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")
            
    db.cerrar_conexion()

if __name__ == "__main__":
    main()