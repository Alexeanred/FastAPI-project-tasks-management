# FastAPI project tasks management

A robust and scalable Task Management System built with **FastAPI**, designed to manage tasks, projects, users, and statuses effectively. This application features project management, task assignment, and more.

---

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)

---

## Features

- **User Management**: Create, update, delete users, and retrieve user details.
- **Project Management**: Manage projects, assign users to projects.
- **Task Management**: Create tasks, Assign tasks to users, update task details, and delete tasks.
- **Status Management**: Add, update, and delete task statuses.
- **Pagination and Filtering**: Efficiently handle large datasets with pagination and query filtering.
- **Database Support**: PostgreSQL integration using SQLAlchemy and SQLModel.

---

## Technologies Used

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLModel
- **Testing**: Pytest
- **Containerization**: Docker

---

## Installation

### Prerequisites

- Python 3.10 or higher
- Docker (for containerized deployment)
- PostgreSQL

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/task-management-system.git
   cd task-management-system
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the `.env` file:

   Create a `.env` file in the root directory with the following content:

   ```env
   DATABASE_URL=postgresql://<username>:<password>@localhost:5432/<database_name>
   SECRET_KEY=your_secret_key
   ```

5. Run the application:

   ```bash
   uvicorn app.main:app --reload
   ```

6. Access the API documentation:

   Open your browser and go to `http://127.0.0.1:8000/docs`.

---

## Run with Docker
- Build the docker image.
```
docker build -t image_name .
```
- Run docker compose (build image)
```
docker compose up --build
```

## Environment Variables

The application uses the following environment variables:

- `DATABASE_URL`: PostgreSQL database connection URL.

---

## API Endpoints

### Users Management

- `POST /users/`: Create a new user.
- `PATCH /users/{user_id}`: Update user details.
- `DELETE /users/{user_id}`: Delete a user.
- `GET /users/{user_id}/projects`: Get projects assigned to a user.

### Projects Management

- `POST /projects/`: Create a new project.
- `PATCH /projects/{project_id}`: Update project details.
- `DELETE /projects/{project_id}`: Delete a project.
- `GET /projects/`: Get all projects (with pagination).
- `POST /projects/assign_user/{project_id}`: Assign a user to a project.

### Tasks Management

- `POST /tasks/`: Create a new task.
- `PATCH /tasks/{task_id}`: Update task details.
- `DELETE /tasks/`: Delete multiple tasks.
- `GET /tasks/`: Get all tasks (with filtering and pagination).
- `PATCH /tasks/update_users/{task_id}`: Assign or reassign a user to a task.

### Status Management

- `POST /status/`: Create a new status.
- `PATCH /status/{status_id}`: Update status details.
- `DELETE /status/{status_id}`: Delete a status.
- `GET /status/`: Get all statuses (with pagination).

---

## Testing

Run the test suite using Pytest:

```bash
pytest tests\
```

---



