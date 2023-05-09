from flask import Flask,render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import  datetime
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:josue2003@localhost:5432/skinloot'
app.config['UPLOAD_FOLDER'] = 'static/usuarios'
db = SQLAlchemy(app)
ALLOWED_EXTENSIONS = {'png','jpeg','jpg','gif'}


# codigo correo nickname saldo

#CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
#\dx to check if uuid-ossp is installed

# begin models:

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36),primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"))
    nickname = db.Column(db.String(100),unique=False,nullable=False)
    e_mail = db.Column(db.String(100),primary_key=True,nullable=False,unique=True)
    saldo = db.Column(db.Integer,nullable=False)
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
    
with app.app_context():
    db.create_all()

# end models.

#Routes
@app.route('/register',methods=["GET"])
def index():
    return render_template('login.html')

@app.route('/register-user',methods=["POST"])
def register_user():
    try:
        nickname = request.form.get('nickname')
        e_mail = request.form.get('e_mail')
        saldo = request.form.get('saldo')

        user = User(nickname,e_mail,saldo)
        db.session.add(user)
        db.session.commit()

        return jsonify({'id':user.id,'success':True,'message':'User created successfully!'}),200
    except Exception as e:
        print(e)
        print(sys.exc_info())
        db.session.rollback()
        return jsonify({'succes':False, 'message':'Error creating user'}),500
    finally:
        db.session.close()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
else:
    print('Importing {}'.format(__name__))