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
        "glm": {
            "function_handler": json2glm,
            "defaults": {},
        },
        "png": {
            "function_handler": json2png,
            "defaults": {'output_type': 'summary', 'with_nodes': False, 'resolution': '300', 'size': '300x200', 'limit': None},
        },
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
    dict_args = request.form.to_dict()
    convert_from = dict_args["convertFrom"]
    convert_to = dict_args["convertTo"]
    # default values for any converter
    try:
        defaults = dict(supported_from_to_conversions[convert_from][convert_to]["defaults"])
    except KeyError:
        flash(f'{convert_from} to {convert_to} converter is not available.')
        print(f'{convert_from} to {convert_to} converter is not available.')
        return redirect('/convert')

    for k, v in dict_args.items():
        if (v == ""):
            dict_args[k] = defaults.get(k)

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
        dict_args['file_in'] = file_in
        try:
            supported_from_to_conversions[convert_from][convert_to]["function_handler"](dict_args)
        except KeyError:
            flash(f'{convert_from} to {convert_to} converter is not available.')
            print(f'{convert_from} to {convert_to} converter is not available.')
            return redirect('/convert')
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
