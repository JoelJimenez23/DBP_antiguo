from flask import Flask,render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime
import sys
import os

app = Flask(__name__)

# ... Para que cada uno trabaje en su maquina: 

# Obtiene el usuario y la contraseña de las variables de entorno
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')

# Construye la URI de la base de datos
db_uri = f"postgresql://{db_user}:{db_password}@localhost:5432/skinloot"

# Configura la URI en la aplicación Flask
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:546362@localhost:5432/skinloot' esto ya no.

app.config['UPLOAD_FOLDER'] = 'static/usuarios'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:230204@localhost:5432/skinloot'
app.config['UPLOAD_FOLDER'] = 'static/skins'
db = SQLAlchemy(app)
ALLOWED_EXTENSIONS = {'png','jpeg','jpg'}


# codigo correo nickname saldo

#CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
#\dx to check if uuid-ossp is installed

# begin models:

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36),primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"))
    nickname = db.Column(db.String(100),unique=False,nullable=False)
    e_mail = db.Column(db.String(100),primary_key=True,nullable=False,unique=True)
    password = db.Column(db.String(100),unique=False,nullable=False)
    #saldo = db.Column(db.Integer,nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.text("now()"))

    def __init__(self,nickname,e_mail,saldo):
        self.nickname = nickname
        self.e_mail = e_mail    
        self.saldo = saldo
        self.created_at = datetime.utcnow()
    def serialize(self):
        return{
            'id': self.id,
            'nickname' : self.nickname,
            'e_mail' : self.e_mail,
            'password' : self.password,
            #'saldo' : self.saldo,
            'created_at':self.created_at
        }
class Skin(db.Model):
    __tablename__='skins'
    hash = db.Column(db.String(36),primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text("uuid_generate_v4()"))
    name = db.Column(db.String(100),unique=False,nullable=False)
    category = db.Column(db.String(100),unique=False,nullable=False)
    game_name = db.Column(db.String(100),unique=False,nullable=False)
    company_name = db.Column(db.String(100),unique=False,nullable=False)
    image = db.Column(db.String(500),nullable=True)

    def __init__(self, name,category,game_name,company_name,image):
        self.name = name
        self.category = category
        self.game_name = game_name
        self.company_name = company_name    
    
    def serialize(self):
        return{
            'hash':self.hash,
            'name':self.name,
            'category':self.category,
            'game_name':self.game_name,
            'company_name':self.company_name,
            'image':self.image
        }

with app.app_context():db.create_all()

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

"""
@app.route('/home', methods=['GET'])
def home():
    return render_template('wel3.html')
"""

@app.route('/register',methods=["GET"])
def register():
    return render_template('login.html')

@app.route('/register-user',methods=["POST"])
@app.route('/register-user', methods=["POST"])
def register_user():
    try:
        nickname = request.form.get('nickname')
        e_mail = request.form.get('e_mail')
        saldo = request.form.get('saldo')
        user = User(nickname, e_mail, saldo)
        db.session.add(user)
        db.session.commit()
        return jsonify({'id': user.id, 'success': True, 'message': 'User created successfully!'}), 200
    except Exception as e:
        print(e)
        print(sys.exc_info())
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error creating user'}), 500
    finally:
        db.session.close()

@app.route('/skins',methods=['GET'])
def skins():
    try:
        nickname = request.form.get('nickname')
        e_mail = request.form.get('e_mail')
        password = request.form.get('password')
        user = User(nickname, e_mail, password)
        db.session.add(user)

        skins = Skin.query.all()
        skins_serialized = [skin.serialize() for skin in skins]
        return jsonify({'success':True,'skins':skins_serialized}),200
    except:
        return jsonify({'success':False})
    
@app.route('/new-skin', methods = ['GET'])
def new_skin():
    return render_template('new_skin.html')

@app.route('/register-skin',methods=["POST"])
def register_skin():
    try:
        name = request.form.get('name')
        category = request.form.get('category')
        game_name = request.form.get('game_name')
        company_name = request.form.get('company_name')

        if 'image' not in request.files:
            return jsonify({'success':False,'message':'html error'}),400
        file = request.files['image']

        if file.filename == '':
            return jsonify({'success':False,'message':'no image selected'}),400
        
        if not allowed_file(file.filename):
            return jsonify({'success':False,'message':'Image format not allowed'}),400
        
        skin = Skin(name,category,game_name,company_name)
        db.session.add(skin)
        db.session.commit()

        cwd = os.getcwd()
        skin_dir = os.path.join(app.config['UPLOAD_FOLDER'], skin.hash)
        os.makedirs(skin_dir, exist_ok=True)

        upload_folder = os.path.join(cwd, skin_dir)

        file.save(os.path.join(upload_folder, file.filename))

        skin.image = file.filename
        db.session.commit()

        return jsonify({'id':skin.hash,'success':True,'message':'Skin Created succesfully!'}),200
    except Exception as e:
        print(e)
        print(sys.exc_info())
        db.session.rollback()
        return jsonify({'success':False,'message':'Error creating skin'})
    finally:
        db.session.close()



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
else:
    print('Importing {}'.format(__name__))