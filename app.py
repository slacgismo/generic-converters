import os
import urllib.request
import json
import sys
import getopt
import shutil
import glob
from flask import Flask, flash, request, redirect, render_template, url_for, send_from_directory
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['json'])

app = Flask(__name__)
app.config.from_object("settings.config.DevelopmentConfig")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/convert')
def upload_form():
    # content = log()
    return render_template('convert.html')

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        convertFrom = request.form["convertFrom"]
        convertTo = request.form["convertTo"]
        uploadFiles = glob.glob('./uploads/*')
        for f in uploadFiles:
            os.remove(f)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(filename + ' successfully uploaded')
            inputExt = filename.split(".")[1]
            os.system('python ./' + convertFrom + '2' + convertTo + '.py')
            # --entrypoint=/bin/bash <imagename>
            outputFile = glob.glob('./uploads/*.' + convertTo)
            outputFile = outputFile[0].split("/")[-1:][0]
            return redirect(url_for('download', filename = outputFile))
        else:
            flash('Allowed file types are json')
            return redirect('/convert')

@app.route('/convert/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)


if __name__ == '__main__':
    app.run(debug=True)
