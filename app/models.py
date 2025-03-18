from app import db

class DeepData(db.Model):
    __tablename__ = 'Deepdata'
    URL = db.Column(db.String, primary_key=True)
    Directory = db.Column(db.String, primary_key=True)
    HTML = db.Column(db.Text)

class DeepConnections(db.Model):
    __tablename__ = 'Deepconnections'
    URL = db.Column(db.String, primary_key=True)
    URLDIR = db.Column(db.String, primary_key=True)
    SITE = db.Column(db.String, primary_key=True)
    SITEDIR = db.Column(db.String, primary_key=True)