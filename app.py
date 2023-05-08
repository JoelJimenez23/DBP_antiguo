from flask import Flask,render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy, CheckConstraint
import uuid
import os
from datetime import  datetime
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:230204@localhost:5432/dbp'
app.config['UPLOAD_FOLDER'] = 'static/usuarios'
db = SQLAlchemy(app)
ALLOWED_EXTENSIONS = {'png','jpeg','jpg','gif'}


# codigo correo nickname saldo

#CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36),primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"))
    nickname = db.Column(db.String(100),unique=False,nullable=False)
    e_mail = db.Column(db.String(100),primary_key=True,nullable=False,unique=True)
    saldo = db.Column(db.Integer,CheckConstraint('saldo >= 0',name='saldo_check'),nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.text("now()"))

    def __init__(self,nickname,e_mail,saldo,created_at):
        self.nickname = nickname
        self.e_mail = e_mail    
        self.saldo = saldo
        self.created_at = created_at
    
    def serialize(self):
        return{
            'id': self.id,
            'nickname' : self.nickname,
            'e_mail' : self.e_mail,
            'saldo' : self.saldo,
            'created_at':self.created_at
        }
    
