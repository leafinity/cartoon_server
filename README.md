# Style Transfer Server on Jupyter hub

## usage

* server: flask, ngrok
* model: [CartoonGAN-Test-Pytorch-Torch](https://github.com/Yijunmaverick/CartoonGAN-Test-Pytorch-Torch))

## execute

start flask server

    export FLASK_APP=./app/main.py
    export PYTHONPATH=./app
    python -m flask run

start ngrok

    ./ngrok http 5000


## test

    python test.py --testfile test.jpg --hostname xxxxx.ngrok.io

