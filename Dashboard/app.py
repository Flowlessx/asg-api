from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, jsonify, request, make_response, render_template, send_file
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import auto_field

import requests

from sqlalchemy.sql.sqltypes import String
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from flask_qrcode import QRcode as QRcode_generator
import uuid
import json
import socket
import os

# instantiate flask object
app = Flask(__name__)

# add QRcode generator
qrcode_generator = QRcode_generator(app)

@app.route("/")
def index():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        return render_template('index.html', hostname=host_name, ip=host_ip)
    except:
        return render_template('error.html')


# add a qrcode
@app.route("/qrcode", methods=["GET"])
def add_qrcode():
    '''
    Request a QR code from asg api. 
    If succesfull return template with rendered qr image
    if unsuccesfull return error msg

    Input : NONE
    Output : HTML TEMPLATE WITH QR_CODE JSON Object 
    '''
    try:
        
        # request a new qr code
        response = requests.get('http://asg-api:8080/qrcode')

        # serialize incoming response
        serialized_qrcode = json.loads(response.text)

        # return template
        return render_template(
            'qr_code.html',
            title=serialized_qrcode['uuid'],
            description="Generate QR code with unique uuid",
            json_qrcode=serialized_qrcode
        )

    except Exception as e:
        return jsonify({"Error": "Invalid Request, please try again." + str(e)})


# get all qrcodes
@app.route("/qrcodes", methods=["GET"])
def get_qrcodes():
    '''
    get all qr code objects from QR_Code model class
    and return jinja template with a table rendering 
    a new row for each dumped qr code object that exists. 

    Input : None
    Output : All QR_CODE JSON Objects
    '''
    try:
        
        # request a new qr code
        response = requests.get('http://asg-api:8080/qrcodes')

        # serialize incoming response
        serialized_qr_codes = json.loads(response.text)

        # return template
        return render_template(
            'qr_codes_overview.html',
            title="QR codes",
            description="Show all existing qr codes",
            qr_codes=serialized_qr_codes
        )

    except Exception as e:
        return jsonify({"Error": "Invalid Request, please try again." + str(e)})

   

# get a specific qrcode
@app.route("/qrcode/<qr_uuid>", methods=["GET"])
def get_qrcode(qr_uuid):
    '''
    Show QR code info with QR code uuid

    Input : QR code uuid
    Ouput : QR code JSON object with corresponding uuid
    '''
    try:
       # request a new qr code
        response = requests.get('http://asg-api:8080/qrcode/' + qr_uuid)

        # serialize incoming response
        serialized_qr_code = json.loads(response.text)

        # return template
        return render_template(
            'qr_code.html',
            title="QR code: " + str(serialized_qr_code.uuid),
            description="Generate QR code with unique uuid",
            json_qrcode=serialized_qr_code
        )

    except Exception as e:
        return jsonify({"Error": "Invalid Request, please try again." + str(e)})



# update a qrcode
@app.route("/qrcode/scanned/<qr_uuid>", methods=["PUT"])
def scanned_qrcode(qr_uuid):
    '''
    Update qr code info from html template form

    Input : QR Code uuid
    Output : QR Code uuid   
    '''
    if request.method == 'PUT':
       
        # update a qr code
        response = requests.put('http://asg-api:8080/qrcode/' + str(qr_uuid))

        # serialize incoming response
        serialized_new_qrcode = json.loads(response.text)

        # return template
        return render_template(
            'qr_code.html',
            title=serialized_new_qrcode['uuid'],
            description="Generate QR code with unique uuid",
            json_qrcode=serialized_new_qrcode
        )

# delete qrcode
@app.route("/qrcode/delete/<qr_uuid>", methods=["DELETE"])
def delete_qrcode(qr_uuid):
    '''
    select qrcode by uuid from QR_Code model class
    deletes qrcode object from database 
    commit if succesfull
    '''
    if request.method == 'DELETE':
       
        #delete a qr code
        response = requests.delete('http://asg-api:8080/qrcode/' + str(qr_uuid))

        # serialize incoming response
        serialized_new_qrcode = json.loads(response.text)

        # return template
        return render_template(
            'qr_code.html',
            title=serialized_new_qrcode['uuid'],
            description="Generate QR code with unique uuid",
            json_qrcode=serialized_new_qrcode
        )

# error handeling
@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@app.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found lolzs'}), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)
   
   
