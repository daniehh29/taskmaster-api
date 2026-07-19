from enum import Enum
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Project(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(250), unique=False, nullable=True)
    created_at  = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tasks       = db.relationship('Task', backref='contain', lazy=True)

    def __repr__(self):
        return f"Project({self.name}, {self.description}, {self.created_at})"


class Status(Enum):
    FINISHED = "finished"


class Task(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(250), unique=False, nullable=True)
    status      = db.Column(db.Enum(Status), unique = False, nullable=False)
    project_id  = db.Column(db.Integer, db.ForeignKey('project.id'), unique=False, nullable=False)


@app.route("/")
def hello():
    return "Hello World"


if __name__ == "__main__":
    app.run(debug=True)