from flask import Flask, render_template, request, session,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from email.message import EmailMessage
import smtplib
import ssl
import os
from werkzeug.utils import secure_filename




with open("config.json", "r") as c:
    params = json.load(c)["params"]



app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['SQLALCHEMY_DATABASE_URI'] = params['sql_url']
db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = params['img_folder']


class User(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(120), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)




@app.route("/")
def home():
    db.create_all()
    if 'username' in session:
        return render_template('home.html', username=session["username"], params=params)
    return render_template('login.html', )


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return render_template('home.html', username=session["username"], params=params)
    elif request.method == 'POST':
        session['username'] = request.form['username']
        return render_template('home.html', params=params)
    else:
        return render_template('login.html')




@app.route("/register", methods=['POST', 'Get'])
def register():
    if 'username' in session:
        return render_template('home.html', username=session["username"], params=params)
    elif request.method == "POST":
        username = request.form.get("username"),
        email = request.form.get("email"),
        password = request.form.get("password"),
        data = User(username=username, email=email, password=password)
        db.session.add(data)
        db.session.commit()

        email_sender = 'zeeshan.malik@maxenius.com'
        email_receiver = 'devzeeshanmalik@gmail.com'
        email_password = 'krlnakfmibztxyun'
        body = 'this is the tesitng body by Zeeshan Malik'

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = 'This is the testing subject'
        em.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_receiver, email_password )
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        return render_template('login.html')
    else:
        return render_template('register.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return render_template('login.html')


@app.route("/users")
def user_list():
    users = User.query.filter_by().all()
    return render_template("user/list.html", users=users,  params=params)

@app.route("/delete/<int:id>", methods=["GET", "POST"])
def user_delete(id):
        # User.query.filter(User.sno == id).delete()
        obj = User.query.filter_by(sno=id).one()
        db.session.delete(obj)
        db.session.commit()
        return redirect(url_for('user_list'))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def user_editf(id):
        obj = User.query.filter_by(sno=id).one()
        return render_template("user/edit.html", data=obj,  params=params)

@app.route("/update/<int:id>", methods=["GET", "POST"])
def user_update(id):
    if request.method == 'POST':
        f = request.files['file1']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        obj = User.query.filter_by(sno=id).one()
        obj.username = request.form.get("username"),
        obj.email = request.form.get("email"),
        obj.password = request.form.get("password"),
        obj.image = f.filename,
        db.session.merge(obj)
        db.session.flush()
        db.session.commit()
        return redirect(url_for('user_list'))

# app.run(debug=True)
