# encoding: utf-8
from __future__ import absolute_import, print_function, division, unicode_literals

from flask import Blueprint, request, abort, session, send_from_directory
from datetime import *
import flask
from werkzeug.utils import secure_filename
from sqlalchemy.orm import joinedload

from .questionnaire_api import init_reply
from .models import *
from . import app
#from .seed import jsonify


api = Blueprint("api", __name__)


def jsonify(*args, **kwargs):
    if len(args) == 1 and not kwargs and type(args[0]) == list:
        return flask.Response(flask.json.dumps(args[0], indent=2), mimetype='application/json')
    else:
        return flask.jsonify(*args, **kwargs)

"""
Authentication API

The Authentication API implements the RESTful methods for login/logout an user
and also initiating/destroying sessions.
"""



@api.route("/session")
def get_session_obj():
    if not "user_id" in session:
        abort(403)
    user = User.query.with_polymorphic("*")\
                .filter_by(id=session["user_id"]).first_or_404()
    today = date.today().__str__()
    print(today)
    bar_charge = BarCalendar.query.options(joinedload("barCharge")).get(today) # BarCharge.query.options(joinedload(BarCharge.date)).first_or_404()
    session_data = {
        "user": user,
        "bar_charge": bar_charge
    }
    return jsonify(session_data)


@api.route("/session", methods=["POST"])
def check_auth():
    """
    Receives a JSON object that contains the login type
    Examples:
        {username: "kreft", password: 123456}
    """
    auth_request = request.get_json()

    if "username" in auth_request:
        user = User.query.filter_by(username=auth_request["username"]).first_or_404()
        if user.check_password(auth_request["password"]):
            session['user_id'] = user.id
            return get_session_obj()
        else:
            abort(403)
    else:
        abort(403)


@api.route("/session/new", methods=["POST"])
def sing_up_patient():
    """
    Receives a JSON object that contains the login type
    Examples:
        {facebook: {... facebook auth data ...}}
        {username: "Max Muster"}
    """
    new_patient_request = request.json
    new_patient_request["pw_hash"] = generate_password_hash(new_patient_request["pw_hash"])
    resident = Resident(**new_patient_request)
    db.session.add(resident)
    db.session.commit()

    user = User.query.filter_by(username=new_patient_request["username"]).first_or_404()

    session['user_id'] = user.id
    return get_session_obj()


@api.route("/session", methods=["DELETE"])
def logout():
    session.pop('user_id', None)  # Delete user cookie
    return ""


user_modifiable_attrs = ["name"]


@api.route("/users/<string:username>")
def get_user(username):
    """
    GET to patient resource: return single patient.
    Use .first_or_404() to automatically raise a 404 error if the resource isn't found.
    """
    return jsonify(User.query.filter_by(username=username).first_or_404())



"""
File API

The File API implements all RESTful methods for demonstration purposes.
As you may note, access control is _not_ implemented yet.
For the moment, that's a feature, so just ignore it.
"""


def _random_string():
    return binascii.b2a_hex(os.urandom(15))


def upload_file(file):
    access_token = _random_string()
    os.mkdir(os.path.join(app.config["UPLOAD_FOLDER"], access_token))

    filename = access_token + "/" + secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    return filename


@api.route('/files', methods=['POST'])
def post_file_upload():
    if "user_id" not in session:
        abort(403)

    file = request.files.listvalues()[0][0]
    filename = upload_file(file)

    return jsonify({
        "filename": filename
    })


@api.route("/files/<token>/<filename>")
def get_file_blob(token, filename):
    """
    return file if access token is correct
    """
    token = filter(str.isalnum, str(token))
    return send_from_directory(os.path.join(app.config["UPLOAD_FOLDER"], token),
                               filename,
                               as_attachment=True,
                               attachment_filename=filename)



@api.route("/picture/<name>")
def get_picture(name):
    return jsonify(Picture.query.filter_by(name=name).first_or_404())

"""
Announcements API

The Announcements API implements all RESTful methods for demonstration purposes.
As you may note, access control is _not_ implemented yet.
For the moment, that's a feature, so just ignore it.
"""


@api.route("/announcements")
def get_announcements():
    if(session):
        return jsonify(Announcement.query.all())
    else:
        return jsonify(Announcement.query.filter_by(public=1).all())


"""
Bar API

The Announcements API implements all RESTful methods for demonstration purposes.
As you may note, access control is _not_ implemented yet.
For the moment, that's a feature, so just ignore it.
"""

@api.route("/barCharge/<resident_id>")
def get_bar_charge(resident_id):
    return jsonify(BarCharge.query.filter_by(resident_id=resident_id).options(joinedload(BarCharge.sold_items)).all())

@api.route("/items")
def get_items():
    return jsonify(Item.query.all())

@api.route("/soldItemBar", methods=["POST"])
def add_sold_item():
    """
    POST to the list: add a new reply.
    The right type will be defined in the function init_reply
    Don't forget to call db.session.commit()
    """
    item = request.json
    Item.query.get(item["item_id"]).decrease_bar(item["amount"])

    try:
        soldItem2 = SoldItemBar.query.filter_by(bar_charge_id=item["bar_charge_id"]).filter_by(item_id=item["item_id"]).first_or_404()
        soldItem2.add_amount(item["amount"])
        db.session.commit()
        return jsonify(soldItem2)
    except:
        soldItem = SoldItemBar(**request.json)
        db.session.add(soldItem)
        db.session.commit()
        return jsonify(soldItem)


@api.route("/soldItemBar/<bar_charge_id>/<item_id>")
def get_sold_item(bar_charge_id, item_id):
     return jsonify(SoldItemBar.query.filter_by(bar_charge_id=bar_charge_id).filter_by(item_id=item_id).first_or_404())