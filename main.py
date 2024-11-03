from flask import Flask, render_template, abort
from flask_smorest import Api, Blueprint
from flask.views import MethodView
from datetime import datetime, timezone
from marshmallow import Schema, fields
import uuid
import enum  


# Initialize Flask application
app = Flask(__name__)


# Configuration class for API settings
class APIConfig:
    API_TITLE = "TODO API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_UI_URL = "https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js"


# Load the API configuration
app.config.from_object(APIConfig)


# Initialize the API
api = Api(app)


# Create a blueprint for the TODO API
todo = Blueprint("todo", "todo", url_prefix="/todo", description="TODO API")


# Sample task data
tasks = [
    {
        "id": uuid.UUID("14c971db-e792-48bb-ac62-cd7e5335eb9e"),
        "created": datetime.now(timezone.utc),
        "completed": False,
        "task": "Create Flask API"
    }
]


# Schema for creating a task
class CreateTask(Schema):
    task = fields.String(required=True)


# Schema for updating a task, inheriting from CreateTask
class UpdateTask(CreateTask):
    completed = fields.Bool()


# Schema for a task, including its ID and creation date
class Task(UpdateTask):
    id = fields.UUID()
    created = fields.DateTime()


# Schema for listing tasks
class ListTasks(Schema):  # Schema for response with a list of tasks
    tasks = fields.List(fields.Nested(Task))


# Enum for sorting by task attribute
class ShortByEnum(enum.Enum):
    task = "task"
    created = "created"


# Enum for sort direction
class SortDirectionEnum(enum.Enum):
    asc = "asc"
    desc = "desc"


# Schema for listing task parameters
class ListTaskParameters(Schema):
    order_by = fields.Enum(ShortByEnum, load_default=ShortByEnum.created)
    order = fields.Enum(SortDirectionEnum, load_default=SortDirectionEnum.asc)


# Define the TodoCollection resource
@todo.route("/tasks")
class TodoCollection(MethodView):


    # GET method to retrieve tasks with optional sorting
    @todo.arguments(ListTaskParameters, location="query")
    @todo.response(status_code=200, schema=ListTasks)  # Response schema for list of tasks
    def get(self, parameters):

        # Sort tasks based on query parameters
        return {"tasks": sorted(
            tasks,
            key=lambda task: task[parameters["order_by"].value],
            reverse=(parameters["order"] == SortDirectionEnum.desc)
        )}


    # POST method to create a new task
    @todo.arguments(CreateTask)
    @todo.response(status_code=201, schema=Task)
    def post(self, task):

        # Assign an ID and created timestamp to the new task
        task["id"] = uuid.uuid4()
        task["created"] = datetime.now(timezone.utc)
        task["completed"] = False
        tasks.append(task)  # Add the new task to the tasks list
        return task  # Return the created task


# Define the TodoTask resource with a specific task ID
@todo.route("/tasks/<uuid:task_id>")
class TodoTask(MethodView):

    # GET method to retrieve a task by its ID
    @todo.response(status_code=200, schema=Task) 
    def get(self, task_id):

        # Search for the task with the given ID
        for task in tasks:
            if task["id"] == task_id:
                return task  # Return the found task
        abort(404, f"Task with ID {task_id} not found.")  # Not found response


    # PUT method to update a task
    @todo.arguments(UpdateTask)
    @todo.response(status_code=200, schema=Task) 
    def put(self, task_id, payload):

        # Search for the task to update
        for task in tasks: 
            if task["id"] == task_id:

                # Update task attributes based on payload
                task["completed"] = payload.get("completed", task["completed"])
                task["task"] = payload.get("task", task["task"])
                return task  # Return the updated task
        abort(404, f"Task with ID {task_id} not found.")  # Not found response


    # DELETE method to remove a task
    @todo.response(status_code=204)
    def delete(self, task_id):

        # Search for the task to delete
        for index, task in enumerate(tasks):
            if task["id"] == task_id:
                tasks.pop(index)  # Remove the task from the list
                return '', 204  # No content response
        abort(404, f"Task with ID {task_id} not found.")  # Not found response


# Register the blueprint with the API
api.register_blueprint(todo)


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
