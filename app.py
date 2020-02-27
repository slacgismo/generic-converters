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
        "png": "json2png(file_in, size, output_type, resolution, limit, with_nodes)",
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
    requests = request.form.to_dict()
    convert_from = requests["convertFrom"]
    convert_to = requests["convertTo"]

    # # json2png parameters
    # output_type = requests.get('outputType', 'summary')
    # with_nodes = requests.get('withNodes', False)
    # resolution = requests.get('resolution', '300')
    # size = requests.get('size', '300x200')
    # limit = requests.get('limit', None)

    # json2png default parameters
    output_type = 'summary'
    with_nodes = False
    resolution = "300"
    size = "300x200"
    limit = None
    if (convert_from == "json" and convert_to == "png"):
        # json2png custom options
        if (requests["size"] != ""):
            size = requests["size"]
        if (requests["outputType"] != ""):
            output_type = requests["outputType"]
        if (requests["resolution"] != ""):
            resolution = requests["resolution"]
        if (requests["limit"] != ""):
            limit = requests["limit"]
        if (requests["withNodes"] != ""):
            with_nodes = requests["withNodes"]

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
        except:
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
