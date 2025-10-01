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
                f'PWD={self.contrasena}'
            )
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
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Listar estudiantes")
    print("2. Agregar estudiante")
    print("3. Buscar estudiante por nombre")
    print("4. Eliminar estudiante por ID")
    print("5. Actualizar edad de estudiante por ID")
    print("6. Mostrar estudiantes con edad ≥ 18")
    print("7. Salir")

def main():
    db = ConexionBD()
    db.conectar()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            estudiantes = db.ejecutar_consulta("SELECT * FROM estudiantes")
            print("\n--- Lista de Estudiantes ---")
            for est in estudiantes:
                print(f"ID: {est[0]}, Nombre: {est[1]}, Edad: {est[2]}")
        elif opcion == "2":
            nombre = input("Nombre del estudiante: ").strip()
            edad = input("Edad del estudiante: ").strip()

            #validaciones
            if len(nombre) < 3:
                print("Error: El nombre debe tener al menos 3 caracteres.")
                continue
            if not edad.isdigit() or int(edad) < 15 or int(edad) > 99:
                print("Error: La edad debe ser un número entre 15 y 99.")
                continue

            db.ejecutar_instruccion("INSERT INTO estudiantes (nombre, edad) VALUES (?, ?)", (nombre, int(edad))
            )
        elif opcion == "3":
            nombre_buscar = input("Ingrese el nombre o parte del nombre a buscar: ").strip()
            estudiantes = db.ejecutar_consulta("SELECT * FROM estudiantes WHERE nombre LIKE ?", (f"%{nombre_buscar}%",)
            )
            print("\n--- Resultados de la búsqueda ---")
            if estudiantes:
                for est in estudiantes:
                    print(f"ID: {est[0]}, Nombre: {est[1]}, Edad: {est[2]}")
            else:
                print("No se encontraron estudiantes con ese nombre.")
        elif opcion == "4":
            id_eliminar = input("Ingrese el ID del estudiante a eliminar: ").strip()

            #validación del ID
            if not id_eliminar.isdigit():
                print("Error: El ID debe ser un número válido.")
                continue

            confirmacion = input(f"¿Está seguro de que desea eliminar al estudiante con ID {id_eliminar}? (s/n): ").strip().lower()
            if confirmacion == "s":
                db.ejecutar_instruccion("DELETE FROM estudiantes WHERE id = ?", (int(id_eliminar),))
                print(f"Estudiante con ID {id_eliminar} eliminado correctamente.")
            else:
                print("Operación cancelada.")

        elif opcion == "5":
            id_actualizar = input("Ingrese el ID del estudiante cuya edad desea actualizar: ").strip()

            #validación del ID
            if not id_actualizar.isdigit():
                print("Error: El ID debe ser un número válido.")
                continue

            nueva_edad = input("Ingrese la nueva edad: ").strip()

            #validación de la nueva edad
            if not nueva_edad.isdigit() or int(nueva_edad) < 15 or int(nueva_edad) > 99:
                print("Error: La edad debe ser un número entre 15 y 99.")
                continue

            db.ejecutar_instruccion(
                "UPDATE estudiantes SET edad = ? WHERE id = ?", (int(nueva_edad), int(id_actualizar))
            )
            print(f"Edad del estudiante con ID {id_actualizar} actualizada correctamente.")
        elif opcion == "6":
            estudiantes = db.ejecutar_consulta("SELECT * FROM estudiantes WHERE edad >= 18")
            print("\n--- Estudiantes con edad ≥ 18 ---")
            if estudiantes:
                for est in estudiantes:
                    print(f"ID: {est[0]}, Nombre: {est[1]}, Edad: {est[2]}")
            else:
                print("No se encontraron estudiantes con edad ≥ 18.")
        elif opcion == "7":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")
    db.cerrar_conexion()

if __name__ == "__main__":
    main()
