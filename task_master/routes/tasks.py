from task_master import db
from task_master.models import Task, Status
from flask import jsonify, request, Blueprint


tasks_db = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_db.route("/<int:id>", methods=["PUT"])
def edit_project_task(id: int):
    task = Task.query.filter(Task.id == id).first()

    if not task:
        return jsonify({
            "error": "Project Task not found"
        }), 404

    data = request.get_json()

    if not data or not data.get("status"):
        return jsonify({
            "error": "El campo \"status\" es obligatorio"
        }), 400
    
    try:
        new_status = Status(data.get("status"))
        task.status = new_status
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": str(e)
        }), 500

    return jsonify(
        task.to_dict()
    ), 200


@tasks_db.route("/<int:id>", methods=["DELETE"])
def delete_project_task(id: int):
    task = Task.query.filter(Task.id == id).first()

    if not task:
        return jsonify({
            "error": "Project Task not found"
        }), 404
    
    db.session.delete(task)
    db.session.commit()

    return jsonify(), 204