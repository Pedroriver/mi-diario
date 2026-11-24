import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# --- Base de Datos ---
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///diario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Cloudinary ---
# Las credenciales se leen de las variables de entorno (para que sea seguro)
cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
    secure = True
)

# --- Modelo ---
class Entrada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(20), nullable=False)
    emoji = db.Column(db.String(10), default='🍂')
    titulo = db.Column(db.String(100), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    fotos = db.Column(db.Text, default='') # Guardaremos las URLs separadas por comas

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        emoji = request.form.get('animo')
        titulo = request.form.get('titulo')
        texto = request.form.get('texto')
        
        if fecha and titulo and texto:
            archivos = request.files.getlist('fotos')
            urls_guardadas = []
            
            for archivo in archivos:
                if archivo and archivo.filename != '':
                    try:
                        # Subimos a Cloudinary
                        resultado = cloudinary.uploader.upload(archivo)
                        urls_guardadas.append(resultado['secure_url'])
                    except Exception as e:
                        print(f"Error subiendo imagen: {e}")
            
            fotos_str = ",".join(urls_guardadas)
            
            nueva = Entrada(fecha=fecha, emoji=emoji, titulo=titulo, texto=texto, fotos=fotos_str)
            db.session.add(nueva)
            db.session.commit()
            
        return redirect(url_for('inicio'))

    entradas = Entrada.query.order_by(Entrada.fecha.desc()).all()
    return render_template('index.html', entradas=entradas)

if __name__ == '__main__':
    app.run(debug=True)
