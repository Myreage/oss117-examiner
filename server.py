import os
from IdChecker import checkMRZ
from flask import Flask, request, render_template

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    result = {}
    if request.method == 'POST':

        # check if file exists and has right format
        if 'file' not in request.files:            
            return render_template('home.html', result=result, error="Il va me falloir un fichier déjà Larmina...")
        if not request.files['file']:       
            return render_template('home.html', result=result, error="Il va me falloir un fichier déjà Larmina...")
        if not allowed_file(request.files['file'].filename):       
            return render_template('home.html', result=result, error="Ecoutez mon p'tit, les formats autorisés sont: .png, .jpg, .pdf, .gif")      
        file = request.files['file']

        # call YouSign API
        try:
            result = checkMRZ(file.read())
        except Exception as e:

            return render_template('home.html', result=result, error=str(e.toString()))
        
        
    return render_template('home.html', result=result)

