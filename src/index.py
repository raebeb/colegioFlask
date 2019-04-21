from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static\imgUpload'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///colegio.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

class noticia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    date = db.Column(db.DateTime)
    text = db.Column(db.Text)
    #imagen
    nameImage = db.Column(db.String(100))
    data = db.Column(db.LargeBinary)

@app.route('/')
def index():
    posts = noticia.query.order_by(noticia.date.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/Mision-y-Vision')
def MisionyVision():
    return render_template('Nosotros/indexNosotros.html')

@app.route('/Plan-de-emergencia')
def PlanEmergencia():
    return render_template('Nosotros/indexPlanEmergencia.html')

@app.route('/Historia')
def Historia():
    return render_template('Nosotros/indexHistoria.html')

@app.route('/Galeria')
def Galeria():
    return render_template('Galeria/Galeria.html')

@app.route('/Noticias-all')
def noticiasAll():
    posts = noticia.query.order_by(noticia.date.desc()).all()
    return render_template('Noticias/noticiasAll.html', post=posts)

@app.route('/Noticias/<int:post_id>')
def Noticias(post_id):
    post = noticia.query.filter_by(id=post_id).one()

    date = post.date.strftime('%B %d, %Y')

    return render_template('Noticias/Noticias.html', post=post, date=date)

@app.route('/add')
def add ():
    return render_template('add.html')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@app.route('/addpost', methods=['GET','POST'])
def addPost():

    file = request.files['foto']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    titulo = request.form['titulo']
    cuerpo = request.form['cuerpo']

    post = noticia(title=titulo, text=cuerpo, date=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/static/imgUpload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run(use_reloader = True, debug=True)