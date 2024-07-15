from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from database import Database

class ApiRestBase(BaseHTTPRequestHandler):
    def set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        db = Database()
        if self.path == "/usuarios":
            resultado = db.query("SELECT * FROM usuarios")
        elif self.path == "/prestamos":
            resultado = db.query("SELECT * FROM prestamos")
        elif self.path == "/equipos":
            resultado = db.query("SELECT * FROM equipos")
        else:
            self.set_headers(404)
            self.wfile.write(json.dumps({"error": "Ruta no encontrada"}).encode("utf-8"))
            return

        resultadoFormat = [
            {column[0]: value for column, value in zip(self.cursor.description, row)} for row in resultado
        ]
        self.set_headers()
        self.wfile.write(json.dumps(resultadoFormat).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        db = Database()
        if self.path == "/usuarios":
            db.execute("INSERT INTO usuarios (dni, email, nombre, apellido, password) VALUES (%s, %s, %s, %s, %s)", 
                       (data["dni"], data["email"], data["nombre"], data["apellido"], data["password"]))
        elif self.path == "/prestamos":
            db.execute("INSERT INTO prestamos (id_usuario, id_equipo, fecha_prestamo) VALUES (%s, %s, %s)", 
                   (data["id_usuario"], data["id_equipo"], data["fecha_prestamo"]))
        elif self.path == "/equipos":
            db.execute("INSERT INTO equipos (isbn, titulo, color) VALUES (%s, %s, %s)", 
                       (data["isbn"], data["titulo"], data["color"]))
        else:
            self.set_headers(404)
            self.wfile.write(json.dumps({"error": "Ruta no encontrada"}).encode("utf-8"))
            db.close()
            return

        db.close()
        self.set_headers(201)
        self.wfile.write(json.dumps({"mensaje": "Dato almacenado en MySQL ok!"}).encode("utf-8"))

    def do_PUT(self):
        parts = self.path.split("/")
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        updated_data = json.loads(post_data)

        db = Database()

        if len(parts) == 3 and parts[1] == "equipos":
            equipo_id = parts[2]
            rows = db.execute(
                "UPDATE equipos SET titulo = %s, isbn = %s, color = %s WHERE id = %s",
            (updated_data["titulo"], updated_data["isbn"], updated_data["color"], equipo_id)
            )

            if rows > 0:
                self.set_headers(200)
                self.wfile.write(json.dumps({"mensaje": "Equipo actualizado correctamente."}).encode("utf-8"))
            else:
                self.set_headers(404)
                self.wfile.write(json.dumps({"error": "Equipo no encontrado"}).encode("utf-8"))

        elif len(parts) == 3 and parts[1] == "usuarios":
            user_id = parts[2]
            rows = db.execute(
                "UPDATE usuarios SET dni = %s, email = %s, nombre = %s, apellido = %s, password = %s WHERE id = %s",
            (updated_data["dni"], updated_data["email"], updated_data["nombre"], updated_data["apellido"], updated_data["password"], user_id)
            )

            if rows > 0:
                self.set_headers(200)
                self.wfile.write(json.dumps({"mensaje": "Usuario actualizado correctamente."}).encode("utf-8"))
            else:
                self.set_headers(404)
                self.wfile.write(json.dumps({"error": "Usuario no encontrado"}).encode("utf-8"))

        elif len(parts) == 3 and parts[1] == "prestamos":
            prestamo_id = parts[2]
            rows = db.execute(
                "UPDATE prestamos SET id_usuario = %s, id_equipo = %s, fecha_prestamo = %s WHERE id = %s",
            (updated_data["id_usuario"], updated_data["id_equipo"], updated_data["fecha_prestamo"], prestamo_id)
            )

            if rows > 0:
                self.set_headers(200)
                self.wfile.write(json.dumps({"mensaje": "Préstamo actualizado correctamente."}).encode("utf-8"))
            else:
                self.set_headers(404)
                self.wfile.write(json.dumps({"error": "Préstamo no encontrado"}).encode("utf-8"))

        else:
            self.set_headers(404)
            self.wfile.write(json.dumps({"error": "Ruta no encontrada"}).encode("utf-8"))

        db.close()


    def do_DELETE(self):
        parts = self.path.split("/")
        db = Database() 

        if len(parts) == 3 and parts[1] == "usuarios":
            user_id = parts[2]
            rows = db.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))

            if rows > 0:
                self.set_headers(200)
                self.wfile.write(json.dumps({"mensaje": "Usuario borrado ok!"}).encode("utf-8"))
            else:
                self.set_headers(404)
                self.wfile.write(json.dumps({"error": "Usuario no encontrado"}).encode("utf-8"))

        elif len(parts) == 3 and parts[1] == "equipos":
            equipo_id = parts[2]
            rows = db.execute("DELETE FROM equipos WHERE id = %s", (equipo_id,))

            if rows > 0:
                self.set_headers(200)
                self.wfile.write(json.dumps({"mensaje": "Equipo borrado ok!"}).encode("utf-8"))
            else:
                self.set_headers(404)
                self.wfile.write(json.dumps({"error": "Equipo no encontrado"}).encode("utf-8"))

        elif len(parts) == 3 and parts[1] == "prestamos":
            prestamo_id = parts[2]
            rows = db.execute("DELETE FROM prestamos WHERE id = %s", (prestamo_id,))

            if rows > 0:
                self.set_headers(200)
                self.wfile.write(json.dumps({"mensaje": "Préstamo borrado ok!"}).encode("utf-8"))
            else:
                self.set_headers(404)
                self.wfile.write(json.dumps({"error": "Préstamo no encontrado"}).encode("utf-8"))

        else:
            self.set_headers(404)
            self.wfile.write(json.dumps({"error": "Ruta no encontrada"}).encode("utf-8"))

        db.close() 

def run(server_class=HTTPServer, handler_class=ApiRestBase, port=3000):
    server_address = ("localhost", port)
    httpd = server_class(server_address, handler_class)
    print(f"ApiRest escuchando por el puerto {port}")
    httpd.serve_forever()

run()
