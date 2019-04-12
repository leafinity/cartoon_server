#!/usr/bin/env python

from flask import Flask, request, send_file

from utils import *
from models.cartoon import CartoonTransformer, Style


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/sync_cartoon_transform/<style>', methods=['POST'])
def sync_cartoon_transform(style):
    valid_ext = ['jpg', 'png']
    valid_style = ['hayao', 'hosoda', 'paprika', 'shinkai']

    if style.lower() not in valid_style:
        return send_error_response('Doesn\'t support style %s' % style)

    if 'file' not in request.files:
        return send_error_response('No file part')
    file = request.files['file']

    if file.filename == '':
        return send_error_response('No selected file')

    if not allowed_file(file.filename, valid_ext):
        return send_error_response('Only accept jpg and png files')

    image =  CartoonTransformer().transform(file2image(file.stream), Style[style.upper()])
    ext = get_file_extension(file.filename)
    image_bytes = image2file(ext, image)

    return send_file(image_bytes, attachment_filename='result.' + ext, mimetype='image/%s' % ext)