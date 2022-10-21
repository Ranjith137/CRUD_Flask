from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/ran'
db = SQLAlchemy(app)


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


@app.route('/index')
def index():
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
