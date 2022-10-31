from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from flask_mail import Mail, Message
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/ran'
db = SQLAlchemy(app)

mail = Mail(app)  # instantiate the mail class

# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ranjith@erssmail.com'
app.config['MAIL_PASSWORD'] = 'ERSS@123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(40))
    lname = db.Column(db.String(40))
    email = db.Column(db.String(40))

    def __init__(self, fname, lname, email):
        self.fname = fname
        self.lname = lname
        self.email = email

if __name__ == "__main__":
    app.run(debug=True)

# @app.route('/')
def home(header,code,name,reason):
    # code = random.choice(range(100000, 999999))  # generating 6 digit random code
    # header = "Forklift Forget Password Successfully"
    msg = Message(header, sender='ranjith@erssmail.com', recipients=["karthick@erssmail.com"])
    msg.html = render_template("sendmail.html", name=name, OTP=code, reason=reason)
    mail.send(msg)
    return 'Sent'


@app.route('/')
def index():
    code = random.choice(range(100000, 999999))  # generating 6 digit random code
    header = "Forklift Registration Successful"
    header1 = "Reset your Forklift password"
    name = "Ranjith"
    reason = "This is to inform you that you have registered successfully with Forklift Warehouse account."
    reason1 = "We have received a request to reset the password for your Forklift Warehouse account."

    sendmail = home(header1,code,name,reason1)
    if sendmail == "Sent":
        return 'Sent'
    else:
        return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']

        student = Student(fname, lname, email)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('display'))


conn = psycopg2.connect(database="ran", user="postgres", password="root", host="localhost")

mycursor = conn.cursor()


@app.route('/display')
def display():
    # mycursor.execute("SELECT * FROM students")
    # data = mycursor.fetchall()
    data = Student.query.all()
    print(data)
    # return "Hi"
    return render_template('display.html', data=data)


@app.route('/delete/<int:id>')
def delete(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('display'))


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    student = Student.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', student = student)
    if  request.method == 'POST':
        student.fname = request.form['fname']
        student.lname = request.form['lname']
        student.email = request.form['email']
        db.session.commit()
        return redirect(url_for('display'))
