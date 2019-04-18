from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C/Users/fran/Documents/Desarrollo/colegio/respaldo/colegio.db'
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
    return render_template('index.html')

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

@app.route('/Noticias')
def Noticias():
    return render_template('Noticias/Noticias.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    newFile = noticia(nameImage=file.filename, data=file.read)
    db.session.add(newFile)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)