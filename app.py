from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import sys
import json
from flask_heroku import Heroku
import copy
import psycopg2
import os
app = Flask( __name__ )
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DATABASE_URL = os.environ['DATABASE_URL']
heroku = Heroku(app)
db = SQLAlchemy(app)


class Dataentry(db.Model):
    __tablename__ = "dataentry"
    id = db.Column(db.Integer, primary_key=True)
    mydata = db.Column(db.Text())

    def __init__ (self, mydata):
        self.mydata = mydata


@app.route("/submit", methods=["POST"])
def post_to_db():

    
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
    cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",(100, "abc'def"))
    conn.commit()
    cur.close()
    conn.close()
    indata = Dataentry(request.form['mydata'])
    data = copy.copy(indata. __dict__ )
    del data["_sa_instance_state"]
    try:
        db.session.add(indata)
        db.session.commit()
    except Exception as e:
        print("\n FAILED entry: {}\n".format(json.dumps(data)))
        print(e)
        sys.stdout.flush()
    return 'Success! To enter more data, <a href="{}">click here!</a>'.format(url_for("enter_data"))


@app.route("/")
def enter_data(): 
    return render_template("dataentry.html")


if __name__ == ' __main__':
    #app.debug = True
    app.run()
