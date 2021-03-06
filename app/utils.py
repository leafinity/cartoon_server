#!/usr/bin/env python
from flask import jsonify

image_format = {
    'jpg': 'jpeg',
    'png': 'png',
}


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def send_json_response(custom_dict, error_code=200):
    respose_dict = {
        'success': True
    }
    respose_dict.update(custom_dict)
    return jsonify(respose_dict), error_code


def send_error_response(msg, error_code=500):
    print('fail', msg)
    return send_json_response({ 
        'success': False,
        'message': msg,
    }, error_code=error_code)


def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower()


def allowed_file(filename, allow_extensions):
    if '.' in filename:
        return get_file_extension(filename) in allow_extensions
    else:
        return False
