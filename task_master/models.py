from task_master import db
from enum import Enum
from datetime import datetime


class Status(Enum):
    PENDIENTE = "Pendiente"
    INICIADA = "En progreso"
    COMPLETADA = "Completada"


class Task(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(20), unique=False, nullable=False)
    description = db.Column(db.String(250), unique=False, nullable=True)
    status      = db.Column(db.Enum(Status), unique = False, nullable=False, default=Status.PENDIENTE)
    project_id  = db.Column(db.Integer, db.ForeignKey('project.id'), unique=False, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description if self.description else None,
            "status": self.status.value
        }
    

class Project(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(250), unique=False, nullable=True)
    created_at  = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tasks       = db.relationship('Task', backref='project', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description if self.description else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    

    def to_dict_with_tasks(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description if self.description else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "tasks": [task.to_dict() for task in self.tasks]
        }