# encoding: utf-8
from __future__ import absolute_import, print_function, division, unicode_literals
from datetime import *
import random
from werkzeug.datastructures import FileStorage
from werkzeug.security import generate_password_hash
import string

import flask
import shutil
import json

from .models import *
from . import app
from .api import upload_file
from .questionnaire_api import anxiety_scale, depression_scale, dlqi_score , pbi_score, pbi_score_new



def seed_dir(relative_path):
    return os.path.join(os.path.dirname(__file__), "seed", relative_path)


def seed():
    """
    Seed function to populate the database with initial values.
    """
    try:
        if User.query.first() and not app.config["DEBUG"]:
            return  # dev mode: always seed db on restart
    except:
        pass

    print("Create Tables...")

    if not app.config["UPLOAD_FOLDER"]:  # pragma: no cover
        raise RuntimeError("No upload folder specified!")
    if os.path.exists(app.config["UPLOAD_FOLDER"]):
        shutil.rmtree(app.config["UPLOAD_FOLDER"])
    os.makedirs(app.config["UPLOAD_FOLDER"])

    db.drop_all()
    db.create_all()

    print("Seeding...")



    # Kunden seeden
    patient_datasets = (
        {
            "username": "kreft",
            "name": "Siegrun Kreft",
            "birthday": "19.07.1963",
            "gender": "weiblich"
        },
        {
            "username": "laengerich",
            "name": "Lena Laengerich",
            "birthday": "12.04.1983",
            "gender": "weiblich"
        },
        {
            "username": "becker",
            "forename": "Peter",
            "name": "Peter Becker"
        },
        {
            "username": "meier3",
            "name": "Lilo Meier"
        },
        {
            "username": "meier1",
            "name": "Hardmut Meier"
        },
        {
            "username": "richter",
            "name": "Peter Richter"
        },
        {
            "username": "hhimmel",
            "name": "Harald Himmelkütter"
        },
        {
            "username": "weigle",
            "name": "Lisa Weigle"
        },
        {
            "username": "kunert",
            "name": "Günter Kunert"
        },
        {
            "username": "hansen",
            "name": "Viktoria Hansen"
        },
        {
            "username": "brecht",
            "name": "Lili Brecht"
        },
    )

    patients = []
    for i in range(len(patient_datasets)):
        patients.append(
            Resident(
                username=patient_datasets[i]["username"],
                pw_hash=generate_password_hash('123456'),
                name=patient_datasets[i]["name"],
                birthday=patient_datasets[i].get("birthday", ""),
                email="kunde" + str(i) + "@example.com",
            )
        )

    for patient in patients:
        db.session.add(patient)

    admin = Administrator(
        username="admin",
        name="Administrator",
        pw_hash=generate_password_hash('admin')
    )
    db.session.add(admin)



    with open(seed_dir("pictures\header_wrap_picture.PNG"), "rb") as f:
        f = upload_file(FileStorage(f, filename="header_wrap_picture.png"))
    wrap = Picture(name="header_wrap_picture", image=f)
    db.session.add(wrap)


    db.session.commit()

    print("Complete!")