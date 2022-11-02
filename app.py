from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from flask_mail import Mail, Message
import datetime
import pytz
import random
from flask_migrate import Migrate
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from wtforms import StringField, SubmitField
from flask_wtf imop

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/Fork'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
s = URLSafeTimedSerializer('SecretKey')

MST = pytz.timezone('US/Mountain')
mail = Mail(app)  # instantiate the mail class

# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ranjith@erssmail.com'
app.config['MAIL_PASSWORD'] = 'ERSS@123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


# @app.route('/', methods=['GET', 'POST'])
# def tokenmethod():
#     if request.method == 'GET':
#         return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'
#
#     email = request.form['email']
#     token = s.dumps(email, salt='email-confirm')
#     msg = Message('Confirm Email', sender='ranjith@erssmail.com', recipients=['karthick@erssmail.com'])
#     link = url_for('confirm_email', token=token, _external=True)
#     msg.body = 'Your link is {}'.format(link)
#     mail.send(msg)
#     return f'<h1> The email entered is {email}. The token is {token} </h1> .format(email, token)'
#
#
# @app.route('/confirm_email/<token>')
# def confirm_email(token):
#     try:
#         email = s.loads(token, salt='email-confirm', max_age=3600)
#     except SignatureExpired:
#         return '<h1>The token is expired!</h1>'
#     return '<h1>The token works!</h1>'


class Warehouse(db.Model):
    __tablename__ = "warehouse"
    WarehouseId = db.Column(db.Integer, primary_key=True)
    WarehouseName = db.Column(db.String(50), nullable=False)
    IsActive = db.Column(db.Boolean, default=1)
    CreatedOn = db.Column(db.DateTime)
    ModifiedOn = db.Column(db.DateTime)


if __name__ == "__main__":
    app.run(debug=True)


# def home(header,code,name,reason):
#     # code = random.choice(range(100000, 999999))  # generating 6 digit random code
#     # header = "Forklift Forget Password Successfully"
#     msg = Message(header, sender='ranjith@erssmail.com', recipients=["karthick@erssmail.com"])
#     msg.html = render_template("sendmail.html", name=name, OTP=code, reason=reason)
#     mail.send(msg)
#     return 'Sent'
#
#
# @app.route('/')
# def index():
#     code = random.choice(range(100000, 999999))  # generating 6 digit random code
#     header = "Forklift Registration Successful"
#     header1 = "Reset your Forklift password"
#     name = "Patrick"
#     reason = "This is to inform you that you have registered successfully with Forklift Warehouse account."
#     reason1 = "We have received a request to reset the password for your Forklift Warehouse account."
#
#     sendmail = home(header,code,name,reason)
#     if sendmail == "Sent":
#         return 'Sent'
#     else:
#         return render_template('index.html')


# @app.route('/submit', methods=['POST'])
# def submit():
#     if request.method == 'POST':
#         fname = request.form['fname']
#         lname = request.form['lname']
#         email = request.form['email']
#         db.session.add(student)
#         db.session.commit()
#         return redirect(url_for('display'))


# @app.route('/display')
# def display():
#     # mycursor.execute("SELECT * FROM students")
#     # data = mycursor.fetchall()
#     data = Student.query.all()
#     print(data)
#     # return "Hi"
#     return render_template('display.html', data=data)


# @app.route('/delete/<int:id>')
# def delete(id):
#     student = Student.query.get(id)
#     db.session.delete(student)
#     db.session.commit()
#     return redirect(url_for('display'))
#
#
# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     student = Student.query.get(id)
#     if request.method == 'GET':
#         return render_template('update.html', student=student)
#     if  request.method == 'POST':
#         student.fname = request.form['fname']
#         student.lname = request.form['lname']
#         student.email = request.form['email']
#         db.session.commit()
#         return redirect(url_for('display'))


@app.route('/')
def warehousess():
    return render_template('warehouse-index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        warehouse = request.form['Warehouse']
        ware = Warehouse(WarehouseName=warehouse, CreatedOn=datetime.datetime.now(MST),ModifiedOn=datetime.datetime.now(MST))
        db.session.add(ware)
        db.session.commit()
        print(warehouse)
        return redirect(url_for('warehousess'))
