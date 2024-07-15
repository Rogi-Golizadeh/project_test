import requests
from utils import validar_isbn_format, validar_isbn_unique

class Equipo:
    def __init__(self, titulo, isbn, color):
        self.titulo = titulo
        self.isbn = isbn
        self.color = color

class GestionEquipos:
    BASE_URL = "http://localhost:3000/equipos"

    def __init__(self):
        self.equiposDB = self.mostrar_equipos() or []

    def anadir_equipo(self, titulo, isbn, color):
        if not validar_isbn_format(isbn):
            return {"error": "ISBN con formato incorrecto"}

        if not validar_isbn_unique(isbn, self.equiposDB):
            return {"error": "ISBN ya existente"}

        equipo = Equipo(titulo, isbn, color)
        response = requests.post(self.BASE_URL, json={
            "titulo": equipo.titulo,
            "isbn": equipo.isbn,
            "color": equipo.color
        })

        if response.status_code == 201:
            return {"mensaje": "Equipo añadido correctamente."}
        else:
            return {"error": "Error al añadir el equipo."}

    def eliminar_equipo(self, isbn):
        response = requests.delete(f"{self.BASE_URL}/{isbn}")

        if response.status_code == 200:
            return {"mensaje": f"Equipo con ISBN {isbn} borrado"}
        else:
            return {"error": "Equipo no encontrado"}

    def buscar_equipo(self, busqueda):
        resultados = [equipo for equipo in self.equiposDB if busqueda.lower() in (equipo['titulo'].lower(), equipo['color'].lower(), equipo['isbn'])]
        
        if resultados:
            return resultados
        else:
            return {"error": "No se encontraron resultados"}

    def mostrar_equipos(self):
        response = requests.get(self.BASE_URL)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "No hay equipos disponibles"}

# Example usage
if __name__ == "__main__":
    gestion_equipos = GestionEquipos()
    
    # Add(añadir)
    add_response = gestion_equipos.anadir_equipo("Surfboard", "978-3-16-148410-0", "Blue")
    print(add_response)

    # Get(mostrar)
    equipos = gestion_equipos.mostrar_equipos()
    print(equipos)

    # Search(buscar)
    search_response = gestion_equipos.buscar_equipo("978-3-16-148410-0")
    print(search_response)

    # Delete(borrar)
    delete_response = gestion_equipos.eliminar_equipo("978-3-16-148410-0")
    print(delete_response)
