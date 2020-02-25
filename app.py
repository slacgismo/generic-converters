import os
import urllib.request
import json
import sys
import getopt
import shutil
import glob
from flask import Flask, flash, request, redirect, render_template, url_for, send_from_directory
from werkzeug.utils import secure_filename
from converters.json2glm import json2glm
from converters.json2png import json2png

app = Flask(__name__)
app.config.from_object("settings.config.DevelopmentConfig")

supported_from_to_conversions = {
    "json": {
        "png": "json2png(file_in)",
        "glm": "json2glm(file_in)",
    },
}

def allowed_file(filename):
    name, extension = os.path.splitext(filename)
    extension = extension[1:].lower()
    return extension in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/convert')
def upload_form():
    return render_template('convert.html')


@app.route('/', methods=['POST'])
def upload_file():
    convert_from = request.form["convertFrom"]
    convert_to = request.form["convertTo"]
    upload_files = glob.glob('./uploads/*')
    for f in upload_files:
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
        file_in = glob.glob('./uploads/*.json')
        try:
            exec(supported_from_to_conversions[convert_from][convert_to])
        except KeyError:
            print(f"{convert_from} to {convert_to} is not implemented")

        output_file = glob.glob('./uploads/*.' + convert_to)
        output_file = output_file[0].split("/")[-1:][0]

        return redirect(url_for('download', filename=output_file))
    else:
        flash('Allowed file types are json')
        return redirect('/convert')


@app.route('/convert/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)


if __name__ == '__main__':
    app.run(debug=True)
