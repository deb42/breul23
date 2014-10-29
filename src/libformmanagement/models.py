# encoding: utf-8
from __future__ import absolute_import, print_function, division, unicode_literals
from werkzeug.security import generate_password_hash, check_password_hash
import os
import binascii

from . import db, utils
from datetime import date as _date


"""
We use SQLAlchemy and Flask-SQLAlchemy to map SQL tables to Python classes.
http://pythonhosted.org/Flask-SQLAlchemy/ <- excellent simple examples
http://de.slideshare.net/jbellis/pycon-2010-sqlalchemy-tutorial <- intro to sqlalchemy presentation
http://www.sqlalchemy.org/ <- api reference
TL;DR: It's awesome.
"""

TYPE_PATIENT = 0b0001
TYPE_PHYSICIAN = 0b0010
TYPE_ADMINISTRATOR = 0b0100 | TYPE_PHYSICIAN

"""
the typs of questionnaires are defined here
remember: TYPE_HADS has to have the lowest number
          in case of change: api.py l. 272
          @api.route("/reply/<int:type>/<int:id>", methods=["POST"]) must be improved
"""

TYPE_HADS = 0b1001
TYPE_DLQI = 0b1010
TYPE_PBI_FOLLOWUP = 0b1011
TYPE_PBI_NEW = 0b1100


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    pw_hash = db.Column(db.String(100))
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    birthday = db.Column(db.String(12))
    # Contains Type of current object, needed for inheritance
    type = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_on': type
    }

    def __repr__(self):
        return self.username

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def __getitem__(self, item):
        if item == "id": return self.id


class Resident(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    barcharge = db.relationship("Barcharge", backref="Resident", foreign_keys="Barcharge.resident_id")
    __mapper_args__ = {
        'polymorphic_identity': TYPE_PATIENT
    }

class Administrator(User):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': TYPE_ADMINISTRATOR
    }

class Duty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

class ResidentDuty(db.Model):
    resident_id = db.Column(db.Integer, db.ForeignKey('resident.id'), primary_key=True)
    duty_id = db.Column(db.Integer, db.ForeignKey('duty.id'), primary_key=True)

class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    image = db.Column(db.String(200))



class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    content = db.Column(utils.JSONType(5000))

    def __repr__(self):
        return "%s: %s" % (self.title)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))

class AnnouncementCategories(db.Model):
    announcement_id = db.Column(db.Integer, db.ForeignKey('announcement.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key=True)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    price = db.Column(db.Integer)

class Barcharge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey('resident.id'))



class BarchargeDrinks(db.Model):
    barcharge_id = db.Column(db.Integer, db.ForeignKey('barcharge.id'), primary_key=True)
    drink_id = db.Column(db.Integer, db.ForeignKey('drink.id'), primary_key=True)
    amount = db.Column(db.Integer)



