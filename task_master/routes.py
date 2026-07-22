from task_master import app, db
from task_master.models import Project, Task
from flask import jsonify, request


@app.route("/projects", methods=["GET"])
def get_projects():
    projects = Project.query.all()
    return jsonify([project.to_dict() for project in projects]), 200


@app.route("/projects/<int:id>", methods=["GET"])
def get_project(id: int):
    project = Project.query.filter(Project.id == id).first()
    if not project:
        return jsonify({
            "error": "No existe proyecto con esa id"
        }), 404
    return jsonify(project.to_dict()), 200


@app.route("/projects", methods=["POST"])
def save_project():
    data = request.get_json()

    if not data or not data.get("name"):
        return jsonify({
            "error": "El campo \"name\" es obligatorio"
        }), 400

    try:
        new_project = Project(
            name=data.get("name"),
            description=data.get("description")
        )

        db.session.add(new_project)
        db.session.commit()

        return jsonify({
            "id": new_project.id,
            "name": new_project.name,
            "description": new_project.description,
            "created_at": new_project.created_at
        }), 201
    except Exception as e:
        db.session_rollback()
        return jsonify({
            "error": str(e)
        }), 500