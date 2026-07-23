from task_master import app, db
from task_master.models import Project, Task, Status
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
            "error": "Project not found"
        }), 404
    return jsonify(
        project.to_dict_with_tasks()
    ), 200


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

        return jsonify(
            new_project.to_dict()
        ), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/projects/<int:id>/tasks", methods=["POST"])
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
    
    try:
        new_task =  Task(
            title=data.get("title"),
            description=data.get("description"),
            status=Status(data.get("status")),
            project_id=id
        )

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
    

@app.route("/tasks/<int:id>", methods=["PUT"])
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


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_project_task(id: int):
    task = Task.query.filter(Task.id == id).first()

    if not task:
        return jsonify({
            "error": "Project Task not found"
        }), 404
    
    db.session.delete(task)
    db.session.commit()

    return jsonify(), 204