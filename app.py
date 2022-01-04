from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, jsonify, request, make_response, render_template, send_file
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import auto_field

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

# set app configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'root'),
    os.getenv('DB_PASSWORD', 'rootpass'),
    os.getenv('DB_HOST', 'database'),
    os.getenv('DB_NAME', 'asg')
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# create db instance
db = SQLAlchemy(app)

# add QRcode generator
qrcode_generator = QRcode_generator(app)

# flask swagger configs
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "AirStar API"
    }
)

class QR_Code(db.Model):
    # table name
    __tablename__ = 'qr_code'  

    # table columns
    uuid = db.Column(db.String(500), nullable=False, primary_key=True)
    scanned = db.Column(db.Boolean, nullable=False, default=False)
    creation_datetime = db.Column(db.DateTime, default=datetime.utcnow)

    # foreign keys
    entry_id = Column(String(500), ForeignKey('entry_info.uuid'))
    user_id = Column(String(500), ForeignKey('user.uuid'))

    # relations
    entry_info = relationship("Entry_Info", foreign_keys=[entry_id])
    user = relationship("User", foreign_keys=[user_id])

class Entry_Info(db.Model):
    # table name
    __tablename__ = 'entry_info'

    # table columns
    uuid = db.Column(db.String(500), nullable=False, primary_key=True)
    location = db.Column(db.String(300), nullable = False)    
    entry_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)   
  

class User(db.Model):
    # table name
    __tablename__ = 'user'

    # columns
    uuid = db.Column(db.String(500), nullable=False, primary_key=True)
    creation_datetime = db.Column(db.DateTime, default=datetime.utcnow)

    # foreign keys
    user_info_uuid = Column(String(500), ForeignKey('user_info.uuid'))
    user_scanned_qr_code_uuid = Column(String(500), ForeignKey('user_scanned_qr_code.uuid'))

    # relations
    user_info = relationship("User_Info", foreign_keys=[user_info_uuid] )
    user_scanned_qr_code = relationship("User_Scanned_QR_Code", foreign_keys=[user_scanned_qr_code_uuid])

class User_Info(db.Model):
    # table name
    __tablename__ = 'user_info'

    # table columns
    uuid = db.Column(db.String(500), nullable=False, primary_key=True)
    ldap_uuid = db.Column(db.String(200))
    name = db.Column(db.String(200))

class User_Scanned_QR_Code(db.Model):
    # table name
    __tablename__ = 'user_scanned_qr_code'   

    # table columns
    uuid = db.Column(db.String(500), nullable=False, primary_key=True) 

    # foreign keys
    user_id = Column(String(500), ForeignKey('user.uuid'))
    qr_code_id = Column(String(500), ForeignKey('qr_code.uuid'))

# instanctiate marshmallow
ma = Marshmallow(app)

# create qr code schema class from SQLAlchemyAutoSchema  
# json object data also gets verified with using schema
class QR_Code_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # set model to QR code in models
        model = QR_Code
        include_relationships = True
        load_instance = True

    # generate fields from models
    uuid = auto_field()
    creation_datetime = auto_field()
    scanned = auto_field()

# instantiate schema objects for qrcodelist and qrcodelists
# qr code list (1 list)
qrcode_schema = QR_Code_Schema(many=False)

# qr codes lists (multiple list)
qrcodes_schema = QR_Code_Schema(many=True)

# regist swagger blueprint and set
# url to /SWAGGER_URL which is set to /swagger
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

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
    Generate QR code with uuid4 this will generate 
    a string with 128 random characters. this uuid will
    be used to identify the qr code and acces its class object 
    to retreive or update any information if neccesary. 
    Input : NONE
    Output : QR_CODE JSON Object 
    '''
    try:
        # create to do list object with a name and description
        qrcode = QR_Code()
        # qr code uuid
        qrcode.uuid = str(uuid.uuid4())
        # qr code scanned boolean
        qrcode.scanned = False
        # add to new value to db session
        db.session.add(qrcode)
        # commit current session to db
        db.session.commit()
        # serialize qr code object
        serialized_qrcode = qrcode_schema.dump(qrcode)
        # return qrcode list schema in json
        return serialized_qrcode

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
    Output : All QR_CODE JSON objects
    '''
    try:
        # query and set complete list
        qrcodes = QR_Code.query.all()

        # serialize object into qrcodes schema
        serialized_qr_codes = qrcodes_schema.dump(qrcodes)

        # return new result set as an json object
        return serialized_qr_codes

    except Exception as e:
            return jsonify({"Error": "Invalid Request, please try again." + str(e)})

# get a specific qrcode
@app.route("/qrcode/<qr_uuid>", methods=["GET"])
def get_qrcode(qr_uuid):
    '''
    QR Code get qrcode object from QR_Code model class
    with its uuid (Universally Unique Identifier )
    and return jinja template with qrcode generator that
    will hold the value's according this QR_Code model class
    Input : QR code uuid
    Ouput : QR code JSON object with corresponding uuid
    '''
    try:
        # query and set specific QR code row with id
        qrcode = QR_Code.query.filter_by(uuid=qr_uuid).first()
        # serialize qr_code
        serialized_qrcode = qrcode_schema.dump(qrcode)
        # return template
        return serialized_qrcode

    except Exception as e:
            return jsonify({"Error": "Invalid Request, please try again." + e})

# update a qrcode
@app.route("/qrcode/scanned/<qr_uuid>", methods=["PUT"])
def scanned_qrcode(qr_uuid):
    '''
    This function updates to do value's, using
    json to request our value we can query our db data  
    Input : QR Code uuid
    Output : QR Code uuid   
    '''
    if request.method == 'PUT':
       
        try:
            # query and set specific QR code row with id
            qrcode = QR_Code.query.filter_by(uuid=qr_uuid).first()
            # set object values using the new data that we requested
            # from the json object above.
            qrcode.uuid = qr_uuid
            qrcode.scanned = True
            # with updating our object values we can
            # commit the current db session
            db.session.commit()

        # on exception export error as e
        except Exception as e:
            return jsonify({"Error": str(e)})

        # request a new qr code
        response = request.get('http://localhost:8080/qrcode')

        # serialize incoming response
        serialized_new_qrcode = json.loads(response.text)

        # return template
        return serialized_new_qrcode

# delete qrcode
@app.route("/qrcode/delete/<qr_uuid>", methods=["GET"])
def delete_qrcode(qr_uuid):
    '''
    select qrcode by uuid from QR_Code model class
    deletes qrcode object from database 
    commit if succesfull
    '''
    # query and set specific QR code row with id
    qrcode = QR_Code.query.filter_by(uuid=qr_uuid).first()
    db.session.delete(qrcode)
    db.session.commit()
    return jsonify({"Success": "qrcode deleted."})


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
   
   
