import requests
from usuarios import GestionUsuarios
from equipos import GestionEquipos
from datetime import datetime

class Prestamo:
    def __init__(self, id_usuario, id_equipo, fecha_prestamo):
        self.id_usuario = id_usuario
        self.id_equipo = id_equipo
        self.fecha_prestamo = fecha_prestamo

class GestionPrestamos:
    BASE_URL = "http://localhost:3000/prestamos"

    def __init__(self):
        self.prestamosDB = self.mostrar_prestamos() or []
        self.gestionEquipos = GestionEquipos()
        self.gestionUsuarios = GestionUsuarios()

    def anadir_prestamo(self, id_usuario, id_equipo, fecha):

        usuario = requests.get(f"{self.BASE_URL}/usuarios/{id_usuario}").json()
        equipo = requests.get(f"{self.BASE_URL}/equipos/{id_equipo}").json()

        if not usuario:
            return {"error": f"No se ha encontrado usuario con ID {id_usuario}"}

        if not equipo:
            return {"error": f"No se ha encontrado equipo con ID {id_equipo}"}

        try:
            fecha_prestamo = datetime.strptime(fecha, "%d/%m/%Y").date()
        except ValueError:
            return {"error": "Formato de fecha incorrecto, debe ser DD/MM/YYYY."}

        response = requests.post(self.BASE_URL, json={
            "id_usuario": id_usuario,
            "id_equipo": id_equipo,
            "fecha_prestamo": fecha_prestamo.isoformat()
        })

        if response.status_code == 201:
            return {"mensaje": "Préstamo añadido correctamente."}
        else:
            return {"error": "Error al añadir el préstamo."}

    def eliminar_prestamo(self, prestamo_id):
        response = requests.delete(f"{self.BASE_URL}/{prestamo_id}")

        if response.status_code == 200:
            return {"mensaje": f"Préstamo con ID {prestamo_id} borrado"}
        else:
            return {"error": "Préstamo no encontrado"}

    def buscar_prestamo(self, prestamo_id):
        response = requests.get(f"{self.BASE_URL}/{prestamo_id}")

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "No hay préstamo."}

    def mostrar_prestamos(self):
        response = requests.get(self.BASE_URL)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "No hay préstamos."}

# Example usage
if __name__ == "__main__":
    gestion_prestamos = GestionPrestamos()
    
    # Add(anadir_prestamo)
    add_response = gestion_prestamos.anadir_prestamo("12345678A", "978-3-16-148410-0", "2024-07-12")
    print(add_response)

    # Get(mostrar)
    prestamos = gestion_prestamos.mostrar_prestamos()
    print(prestamos)

    # Search(buscar)
    search_response = gestion_prestamos.buscar_prestamo(1)
    print(search_response)

    # Delete(eliminar)
    delete_response = gestion_prestamos.eliminar_prestamo(1)
    print(delete_response)
