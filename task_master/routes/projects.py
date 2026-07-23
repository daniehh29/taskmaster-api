from task_master import db
from task_master.models import Project, Task, Status
from flask import jsonify, request, Blueprint


projects_bp = Blueprint("projects", __name__, url_prefix="/projects")


@projects_bp.route("/", methods=["GET"])
def get_projects():
    projects = Project.query.all()
    return jsonify([project.to_dict() for project in projects]), 200


@projects_bp.route("/<int:id>", methods=["GET"])
def get_project(id: int):
    project = Project.query.filter(Project.id == id).first()
    if not project:
        return jsonify({
            "error": "Project not found"
        }), 404
    return jsonify(
        project.to_dict_with_tasks()
    ), 200


@projects_bp.route("/", methods=["POST"])
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

        return jsonify(
            new_project.to_dict()
        ), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": str(e)
        }), 500


@projects_bp.route("/<int:id>/tasks", methods=["POST"])
def save_project_task(id: int):
    project = Project.query.filter(Project.id == id).first()

    if not project:
        return jsonify({
            "error": "Project not found"
        }), 404

    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({
            "error": "El campo \"title\" es obligatorio"
        }), 400
    
    task_args = {
        "title": data.get("title"),
        "description": data.get("description"),
        "project_id": id
    }

    raw_status = data.get("status")

    if raw_status is not None:
        try:
            task_args["status"] = Status(raw_status)
        except ValueError:
            valids_status = [s.value for s in Status]
            return jsonify({
                "error": f"El estado '{raw_status}' no es válido. Estados permitidos: {valids_status}"
            }), 400

    try:
        new_task =  Task(**task_args)

        db.session.add(new_task)
        db.session.commit()

        return jsonify(
            new_task.to_dict()
        ), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": str(e)
        }), 500