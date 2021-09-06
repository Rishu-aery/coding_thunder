from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json

with open("config.json","r") as c:
    params= json.load(c)["params"]
local_server=True


app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)
mail=Mail(app)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']


db = SQLAlchemy(app)


class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    mes = db.Column(db.String(120),  nullable=False)



@app.route("/")
def home():
    return render_template('index.html', params=params)

@app.route("/portfolio-details")
def portfolio():
    return render_template('portfolio-details.html', params=params)

@app.route("/contact", methods=['GET','POST'])
def contact():
    if (request.method=='POST'):
        '''Add entry to database'''
        name = request.form.get('name')
        email = request.form.get('email')
        subj = request.form.get('subject')
        message = request.form.get('message')

        entry = Contacts(name=name, email=email, subject=subj, mes=message)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from Blog',
                          sender=email,
                          recipients=[params['gmail-user']],
                          body= message + '\n' + name

                          )

    return render_template('contact.html', params=params)

@app.route("/inner-page")
def inner_page():
    return render_template('inner-page.html', params=params)

app.run(debug=True)