from flask import Flask, render_template, request, redirect, url_for
import json, csv, os
from conexion.conexion import db, init_app

app = Flask(__name__)
init_app(app)  # Inicializa la base de datos

# -------------------- Modelo MySQL --------------------
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    mail = db.Column(db.String(100))

# Crear tablas automáticamente
with app.app_context():
    db.create_all()

# -------------------- Rutas --------------------
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/formulario')
def formulario():
    return render_template("formulario.html")

# -------------------- Persistencia TXT --------------------
@app.route('/guardar_txt', methods=['POST'])
def guardar_txt():
    nombre = request.form['nombre']
    os.makedirs("datos", exist_ok=True)
    with open("datos/datos.txt", "a", encoding="utf-8") as f:
        f.write(nombre + "\n")
    return redirect(url_for('index'))

@app.route('/leer_txt')
def leer_txt():
    contenido = []
    if os.path.exists("datos/datos.txt"):
        with open("datos/datos.txt", "r", encoding="utf-8") as f:
            contenido = f.readlines()
    return render_template("resultado.html", datos=contenido, titulo="Clientes (TXT)")

# -------------------- Persistencia JSON --------------------
@app.route('/guardar_json', methods=['POST'])
def guardar_json():
    nombre = request.form['nombre']
    os.makedirs("datos", exist_ok=True)
    data = []
    if os.path.exists("datos/datos.json"):
        with open("datos/datos.json", "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    data.append({"nombre": nombre})
    with open("datos/datos.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return redirect(url_for('index'))

@app.route('/leer_json')
def leer_json():
    data = []
    if os.path.exists("datos/datos.json"):
        with open("datos/datos.json", "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    return render_template("resultado.html", datos=data, titulo="Clientes (JSON)")

# -------------------- Persistencia CSV --------------------
@app.route('/guardar_csv', methods=['POST'])
def guardar_csv():
    nombre = request.form['nombre']
    os.makedirs("datos", exist_ok=True)
    with open("datos/datos.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([nombre])
    return redirect(url_for('index'))

@app.route('/leer_csv')
def leer_csv():
    data = []
    if os.path.exists("datos/datos.csv"):
        with open("datos/datos.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            data = list(reader)
    return render_template("resultado.html", datos=data, titulo="Clientes (CSV)")

# -------------------- Persistencia MySQL --------------------
@app.route('/guardar_mysql', methods=['POST'])
def guardar_mysql():
    nombre = request.form['nombre']
    mail = request.form.get('mail', '')
    if nombre.strip() != "":
        nuevo = Usuario(nombre=nombre, mail=mail)
        db.session.add(nuevo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/leer_mysql')
def leer_mysql():
    usuarios = Usuario.query.all()
    return render_template("resultado.html", datos=usuarios, titulo="Clientes (MySQL)")

# -------------------- Ruta de prueba --------------------
@app.route('/test_mysql')
def test_mysql():
    try:
        total = Usuario.query.count()
        return f"Conectado a MySQL en la nube. Total usuarios: {total}"
    except Exception as e:
        return f"Error: {e}"

# -------------------- Arranque del servidor --------------------
if __name__ == '__main__':
    app.run(debug=True)
