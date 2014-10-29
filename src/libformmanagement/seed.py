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
from werkzeug.utils import secure_filename

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
        access_token = 'pictures'
        file = FileStorage(f, filename="header_wrap_picture.png")
        os.mkdir(os.path.join(app.config["UPLOAD_FOLDER"], access_token))
        filename = access_token + "/" + secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        f = filename
    wrap = Picture(name="header_wrap_picture", image=f)
    db.session.add(wrap)

    db.session.commit()


    announcements_database = (
        {
            "title": "Freibier am Samstag!",
            "content": "Liebe Breulianer, im Zuge des Neuenwochenendes werden wir an diesem Samstag (27.09.) die Bar öffnen, damit man sich schon einmal kennenlernen kann. Starten werden wir spätestens gegen 21 Uhr. Es wird auch Freibier geben, also kommt alle und zahlreich! Eure Tutoren, Lukas und Jules"
        },
        {
            "title": "Liturgieplan Juli 2014",
            "content": "Gottesdienste in der Hauskapelle „Verklärung Christi“ im Juli 2014   Dienstag 1. Juli 7:00 Uhr Heilige Messe L: Am 3,1-8; 4,11-12 Ev: Mt 8,23-27 Mittwoch Mariä Heimsuchung 2. Juli 20:30 Uhr Heilige Messe vom FestL: Röm 12,9-16bEv: Lk 1,39-56 Donnerstag 3. Juli 22:00 Uhr22:30 Uhr Eucharistische AnbetungKomplet Dienstag 8. Juli 7:00 Uhr Heilige MesseL: Hos 8,4-7.11-13Ev: […]"
        },
        {
            "title": "KSHG Turnier",
            "content": "Liebe Mitbewohner, während wir uns heute Abend ab- Achtung!- 18:30  Uhr im Breulcup beim Fußball messen, findet am Sonntag um 11 Uhr das traditionsreiche KSHG-Fußballturnier am Bistumsplatz an der Anette Allee 43 (vgl. Weg vom Breul aus) statt. Es wäre schön, wenn dort nicht nur die Fußball-, sondern auch die Breulbegeisterten vorbeischauen würden, um unsere […]"
        },
        {
            "title": "Maitour",
            "content": "Hallo Jungs, auch wenn das Wetter für morgen nicht allzu gut angesagt ist, werden wir, die Tutoren der Burse und des Breul, ein Programm anbieten. Wir treffen uns um 12 Uhr auf dem großen 400er Balkon (oder in der Nähe) und starten unsere Rallye wenn die Burse um 14 Uhr dazu gestoßen ist. Ein Regenplan […]"
        }
    )

    announcements =[]
    for i in range(len(announcements_database)):
        announcements.append(
            Announcement(
                title=announcements_database[i]["title"],
                content=announcements_database[i]["content"]
            )
        )

    announcements.append( Announcement(
                title="Lorem Impsum",
                content=announcements_database[3]["content"],
                public=1
            ))

    for announcement in announcements:
        db.session.add(announcement)


    db.session.commit()

    drink = Drink(name="Bier", price=1)
    db.session.add(drink)
    db.session.commit()

    barcharge = Barcharge(resident_id=1, done=True)
    db.session.add(barcharge)
    db.session.commit()

    blub = BarchargeDrink(barcharge=barcharge, drink=drink, amount=5)
    db.session.add(blub)
    db.session.commit()

    print("Complete!")