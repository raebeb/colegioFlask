from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
import os

UPLOAD_FOLDER = 'static/imgUpload'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uwu.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

app.secret_key = b'_5#y2L"F4Q8zln\xec]/'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10))
    password = db.Column(db.String(10))

class noticia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    date = db.Column(db.DateTime)
    text = db.Column(db.Text)
    #imagen
    nameImage = db.Column(db.String(100))
    data = db.Column(db.LargeBinary)

class loginform(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])

@app.route('/')
def index():
    posts = noticia.query.order_by(noticia.date.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginform() 
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                return redirect(url_for('add'))
        flash('Credenciales incorrectas', 'error')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


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

    image_names = os.listdir('static/imgUpload')

    return render_template('Noticias/Noticias.html', post=post, date=date)

@app.route('/Pt9QHFTUV6Vpq0vdu6Nn')
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

    post = noticia(title=titulo, text=cuerpo, date=datetime.now(), nameImage = filename)
    db.session.add(post)
    db.session.commit()

    return redirect('/')

@app.route('/static/imgUpload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run(use_reloader = True, debug=True)