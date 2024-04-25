from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gymusers.db'
app.secret_key = 'gym'
db = SQLAlchemy(app)




class GymUsers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)


@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    phone = request.form['phone']

    user = GymUsers(name=name, email=email, password=password, phone=phone)
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = GymUsers.query.filter_by(email=email, password=password).first()

    if user is not None:
        return redirect(url_for('index'))

    error_msg = "Invalid username or password"
    return render_template('index.html', css=url_for('static', filename='index.css'), error=error_msg)


@app.route('/')
def index():
    return render_template('index.html', css=url_for('static', filename='index.css'))


@app.route('/background')
def services():
    return render_template("background.html")


@app.route('/programs')
def programs():
    return render_template("programs.html")


@app.route('/About_me')
def About_me():
    return render_template('About_me.html', css=url_for('static', filename='about_me.css'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        db.session.commit()
app.run(debug=True)
