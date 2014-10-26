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



    # Kundenberater seeden
    physician_datasets = (
        {
            "username": "meier",
            "password": "123456",
            "name": "Dr. Meier"
        },
        {
            "username": "gaul",
            "password": "123456",
            "name": "Dr. Gaul"
        },
        {
            "username": "hubner",
            "password": "123456",
            "name": "Dr. Hubner"
        },
        {
            "username": "bayer",
            "password": "123456",
            "name": "Dr. Bayer"
        },
        {
            "username": "sommer",
            "password": "123456",
            "name": "Dr. Sommer"
        },
        {
            "username": "wulf",
            "password": "123456",
            "name": "Dr. Wulf"
        }
    )

    physicians = []
    for i in range(len(physician_datasets)):
        physicians.append(
            Physician(
                username=physician_datasets[i]["username"],
                pw_hash=generate_password_hash(physician_datasets[i]["password"]),
                name=physician_datasets[i]["name"]
            )
        )
    for i in range(len(physician_datasets)):
        db.session.add(physicians[i])

    db.session.commit()


    # physician_datasets[0]["username"], physician_datasets[0]["password"], physician_datasets[0]["name"]
    #for i in range(len(physician_datasets))]
    # for i in range(len(physician_datasets)):
    #db.session.add(physicians[i])



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
        physician = physicians[0]
        patients.append(
            Patient(
                username=patient_datasets[i]["username"],
                pw_hash=generate_password_hash('123456'),
                name=patient_datasets[i]["name"],
                gender=patient_datasets[i].get("gender", ""),
                birthday=patient_datasets[i].get("birthday", ""),
                email="kunde" + str(i) + "@example.com",
                # Kundenberater zufällig zuweisen
                physician=physician
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

    json_data = open("./libformmanagement/seed/questionnaires/hads.json")
    hads_data = json.load(json_data)

    hads = Questionnaire(
        title="HADS",
        content=hads_data["content"],
        type=TYPE_HADS,
        value=hads_data["value"],
        scores=hads_data["scores"],
        instruction = hads_data["instruction"]
    )

    db.session.add(hads)

    json_data = open("./libformmanagement/seed/questionnaires/dlqi.json")
    dlqi_data = json.load(json_data)

    dlqi = Questionnaire(
        title="DLQI",
        content=dlqi_data["content"],
        type=10,
        value=dlqi_data["value"],
        scores=dlqi_data["scores"],
        instruction = dlqi_data["instruction"]
    )

    db.session.add(dlqi)

    json_data = open("./libformmanagement/seed/questionnaires/pbi_followup.json")
    pbi_data = json.load(json_data)

    pbi = Questionnaire(
        title="PBI Follow-Up",
        content=pbi_data["content"],
        type=11,
        value=pbi_data["value"],
        scores=pbi_data["scores"],
        instruction = pbi_data["instruction"]
    )

    db.session.add(pbi)

    json_data = open("./libformmanagement/seed/questionnaires/pbi_new.json")
    pbi_data = json.load(json_data)


    pbi = Questionnaire(
        title="PBI Erstaufnahme",
        content=pbi_data["content"],
        type=12,
        value=pbi_data["value"],
        scores=pbi_data["scores"],
        instruction = pbi_data["instruction"]
    )

    db.session.add(pbi)

    db.session.commit()

    for i in range(0, 30, 2):
        answers = []
        for j in range(0, 14):
            answers.append(random.randint(0, 3))
        questionnaire = Questionnaire.query.filter_by(type=TYPE_HADS).first_or_404()
        hadsresult = Hads(
            patient=patients[1],
            date=date.today() - timedelta(days=i * 7),
            data=answers,
            anxiety_scale=anxiety_scale(answers, questionnaire["value"]),
            depression_scale=depression_scale(answers, questionnaire["value"])
        )
        db.session.add(hadsresult)

    for i in range(1, 30, 2):
        answers = []
        for j in range(0, 3):
            answers.append(random.randint(0, 3))
        questionnaire = Questionnaire.query.filter_by(type=TYPE_HADS).first_or_404()
        hadsresult = Dlqi(
            patient=patients[0],
            date=date.today() - timedelta(days=i * 7),
            data=answers,
            score=dlqi_score(answers, questionnaire["value"]),

        )
        db.session.add(hadsresult)

    for i in range(1, 30, 2):
        answers = []
        for j in range(0, 14):
            answers.append(random.randint(0, 3))
        questionnaire = Questionnaire.query.first_or_404()
        hadsresult = Hads(
            patient=patients[0],
            date=date.today() - timedelta(days=i * 7),
            data=answers,
            anxiety_scale=anxiety_scale(answers, questionnaire["value"]),
            depression_scale=depression_scale(answers, questionnaire["value"])
        )
        db.session.add(hadsresult)

    for i in range(0, 30, 2):
        answers = []
        for j in range(0, 3):
            answers.append(random.randint(0, 3))
        questionnaire = Questionnaire.query.filter_by(type=TYPE_HADS).first_or_404()
        hadsresult = Dlqi(
            patient=patients[1],
            date=date.today() - timedelta(days=i * 7),
            data=answers,
            score=dlqi_score(answers, questionnaire["value"]),

        )
        db.session.add(hadsresult)

    answers = []
    for j in range(0, 25):
        answers.append(random.randint(0, 4))
    questionnaire = Questionnaire.query.filter_by(type=TYPE_PBI_NEW).first_or_404()
    pbiresult = PbiNew(
        patient=patients[0],
        date=date.today() - timedelta(days=i * 7),
        data=answers,
        score=pbi_score_new(answers, questionnaire["value"])
    )
    db.session.add(pbiresult)
    db.session.commit()

    for i in range(1, 30, 2):
        answers = []
        for j in range(0, 25):
            answers.append(random.randint(0, 4))
        questionnaire = Questionnaire.query.filter_by(type=TYPE_PBI_FOLLOWUP).first_or_404()
        pbiresult = PbiFollowUp(
            patient=patients[0],
            date=date.today() - timedelta(days=i * 7),
            data=answers,
            score=pbi_score(answers, questionnaire["value"], patients[0]["id"])
        )
        db.session.add(pbiresult)

    db.session.commit()

    with open(seed_dir("pictures\header_wrap_picture.PNG"), "rb") as f:
        f = upload_file(FileStorage(f, filename="header_wrap_picture.png"))
    wrap = Picture(name="header_wrap_picture", image=f)
    db.session.add(wrap)


    db.session.commit()

    print("Complete!")