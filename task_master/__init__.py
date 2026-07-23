from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    db.init_app(app)


    from task_master.routes.projects import projects_bp
    from task_master.routes.tasks import tasks_db
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_db)

    
    return app