import requests
from utils import validar_dni_format, validar_dni_unique, validar_email_format, validar_email_unique

class Usuario:
    def __init__(self, dni, nombre, apellido, email, password):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.password = password

class GestionUsuarios:
    BASE_URL = "http://localhost:3000/usuarios"

    def __init__(self):
        self.usuariosDB = self.mostrar_usuarios() or []

    def anadir_usuario(self, dni, nombre, apellido, email, password):
        if not validar_dni_format(dni):
            return {"error": "Formato de DNI incorrecto."}

        if not validar_dni_unique(dni, self.usuariosDB):
            return {"error": "DNI ya existente."}

        if not validar_email_format(email):
            return {"error": "Formato de email incorrecto."}

        if not validar_email_unique(email, self.usuariosDB):
            return {"error": "Email ya existente."}

        # Ensure password is a string
        if not isinstance(password, str):
            return {"error": "La contraseña debe ser una cadena."}

        usuario = Usuario(dni, nombre, apellido, email, password)
        response = requests.post(self.BASE_URL, json={
            "dni": usuario.dni,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "email": usuario.email,
            "password": usuario.password
        })

        if response.status_code == 201:
            return {"mensaje": "Usuario añadido correctamente."}
        else:
            return {"error": "Error al añadir el usuario."}


    def borrar_usuario(self, dni):
        response = requests.delete(f"{self.BASE_URL}/{dni}")

        if response.status_code == 200:
            return {"mensaje": f"Usuario con DNI {dni} borrado."}
        else:
            return {"error": f"Usuario con DNI {dni} no registrado."}

    def buscar_usuario(self, dni):
        response = requests.get(f"{self.BASE_URL}/{dni}")

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "No hay usuario."}

    def mostrar_usuarios(self):
        response = requests.get(self.BASE_URL)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "No hay usuarios."}

# Example usage 
if __name__ == "__main__":
    gestion_usuarios = GestionUsuarios()
    
    # Ad(añadir)
    add_response = gestion_usuarios.anadir_usuario("12345678A", "John", "Doe", "john.doe@example.com", "password123")
    print(add_response)

    # Get(mostrar)
    usuarios = gestion_usuarios.mostrar_usuarios()
    print(usuarios)

    # Search(buscar)
    search_response = gestion_usuarios.buscar_usuario("12345678A")
    print(search_response)

    # Delete(borrar)
    delete_response = gestion_usuarios.borrar_usuario("12345678A")
    print(delete_response)
