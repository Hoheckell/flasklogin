from flask import Flask, request, render_template, redirect, flash, session, url_for
from flask_sessions import Session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from models.user import User


userpass = 'mysql://root:123@'
host = 'localhost'
dbname = '/flaskagenda'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = userpass + host + dbname #mysql://username:password@localhost/db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy()
db.init_app(app)
sess = Session()
bcrypt = Bcrypt(app)



app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/404')
def nada():
    return render_template('404.html')


@app.route('/cadastro')
def cadastrar():
    return render_template('cadastro.html')


@app.route('/users')
def lista():
    users = User.query.all()
    return render_template('users.html',users=users)


@app.route('/cadastro',methods=['POST'])
def adduser():
    user = User()
    user.nome = request.form['nome']
    user.email = request.form['email']
    user.password = bcrypt.generate_password_hash(request.form['password'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('.lista'))



@app.route('/',methods=['POST'])
def Autentica():
    error = None
    email = request.form['email']
    password = request.form['password']
    usercheck = User.query.filter_by(email=email).first()
    if bcrypt.check_password_hash(usercheck.password,password):
        flash('Logado com sucesso')
        return  redirect('/')
    else:
        error = 'Invalid credentials'

    return render_template('index.html', error=error)


if __name__ == '__main__':
    app.debug = True
    app.run()
