#!/usr/bin/env python

import io
import uuid
import numpy as np
from PIL import Image
from flask import Flask, request, send_file

from celery_queue import workers
from utils import *

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route('/cartoon_transform/<style>', methods=['POST'])
def cartoon_transform(style):
    valid_ext = ['jpg', 'png']
    valid_style = ['hayao', 'hosoda', 'paprika', 'shinkai']

    if style.lower() not in valid_style:
        return send_error_response('Doesn\'t support style %s' % style)

    print(list(request.files.keys()))
    if 'file' not in request.files:
        return send_error_response('No file part')
    file = request.files['file']

    if file.filename == '':
        return send_error_response('No selected file')

    if not allowed_file(file.filename, valid_ext):
        return send_error_response('Only accept jpg and png files')

    try:
        image = Image.open(file.stream).convert("RGB")
        image = np.array(image)
        # file.stream
        task = workers.transform_photo.apply_async(
            args=[get_file_extension(file.filename), image.tolist(), style], 
        )
    except Exception as e:
        print('error', e)
        return 'failed', 500

    return task.id

@app.route('/cartoon_transform/check_status/<task_id>', methods=['GET'])
def check_cartoon_transform_status(task_id):
    res = workers.celery.AsyncResult(task_id)

    if res.failed():
        return send_error_response('task failed')

    if not res.ready():
        return  send_json_response({'finished': False})

    return  send_json_response({'finished': True})


@app.route('/cartoon_transform/download_image/<task_id>', methods=['GET'])
def download_cartoon_transformed_image(task_id):
    res = workers.celery.AsyncResult(task_id)

    if not res.ready():
        return  'task hasn\'t been finished', 500

    ext, image_list = res.get()
    output_image = Image.fromarray(np.uint8(image_list))

    image_bytes = io.BytesIO()
    output_image.save(image_bytes, format=image_format[ext])
    image_bytes = image_bytes.getvalue()

    return send_file(io.BytesIO(image_bytes), attachment_filename='result.' + ext, mimetype='image/%s' % ext)
