from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres123@localhost/height_collector'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://u9gop5rs91odkc:p6d3a876433339bb73ec91fb812a3113e420b9912e59b262b4f217c12eeed5e56@c1i13pt05ja4ag.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d89j50vs0u5d9i?sslmode=require'
db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    height = db.Column(db.Integer)
    
    def __init__(self, email, height):
        self.email = email
        self.height = height

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        email_ = request.form["email_name"]
        height_ = request.form["height_name"]
        if db.session.query(Data).filter(Data.email == email_).count() == 0:
            data = Data(email_, height_)
            db.session.add(data)
            db.session.commit()
            average_height = db.session.query(func.avg(Data.height)).scalar()
            average_height = round(average_height, 1)
            count = db.session.query(Data.height).count()
            send_email(email_, height_, average_height, count)
            return render_template("success.html")
    return render_template("index.html", text = "We have that email address already!")
    
if __name__ == '__main__':
    app.debug = True
    app.run()

