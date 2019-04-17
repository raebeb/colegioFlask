from flask import Flask, render_template

app = Flask(__name__)
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

if __name__ == '__main__':
    app.run(debug=True)