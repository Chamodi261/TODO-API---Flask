# TODO API

## 🚀 Introduction
This is a simple TODO API built with Flask that allows you to manage your tasks efficiently. You can create, retrieve, update, and delete tasks using this API.

## 📦 Installation

### Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
```

### Activate the Virtual Environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS and Linux:**
```bash
source venv/bin/activate
```

### Install the Required Packages
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
python app.py
```

### Access the API
Open your browser and navigate to:
- Swagger UI Documentation: `http://127.0.0.1:5000/docs`
- Redoc Documentation: `http://127.0.0.1:5000/redoc`

## 📡 API Endpoints

### Task Collection
- **GET /todo/tasks**  
  Retrieve a list of tasks. Supports query parameters for sorting:
  - `order_by`: Sort tasks by task or created
  - `order`: Sort direction `asc` or `desc`

- **POST /todo/tasks**  
  Create a new task. Requires a JSON body with the following structure:
  ```json
  {
      "task": "Your task description"
  }
  ```

### Single Task
- **GET /todo/tasks/<uuid:task_id>**  
  Retrieve a specific task by its ID.

- **PUT /todo/tasks/<uuid:task_id>**  
  Update an existing task. Requires a JSON body with the following structure:
  ```json
  {
      "task": "Updated task description",
      "completed": true
  }
  ```

- **DELETE /todo/tasks/<uuid:task_id>**  
  Delete a specific task by its ID.

## 📝 Example Usage
Here’s an example of how to interact with the API using curl.

### Create a Task
```bash
curl -X POST http://127.0.0.1:5000/todo/tasks -H "Content-Type: application/json" -d '{"task": "Learn Flask"}'
```

### Get All Tasks
```bash
curl -X GET http://127.0.0.1:5000/todo/tasks
```

### Update a Task
```bash
curl -X PUT http://127.0.0.1:5000/todo/tasks/<your-task-id> -H "Content-Type: application/json" -d '{"task": "Learn Flask", "completed": true}'
```

### Delete a Task
```bash
curl -X DELETE http://127.0.0.1:5000/todo/tasks/<your-task-id>
```

## 📚 References
- [YouTube Video Reference](https://www.youtube.com/watch?v=mt-0F_5KvQw)

### Instructions to Customize:
- Replace `https://github.com/yourusername/todo-api.git` with the actual URL of your repository.
- Update the author section with your name and GitHub profile link.
- Modify any sections to reflect the specific details of your project or any additional features you've added.
