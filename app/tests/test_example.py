import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models import Task
from app.schema import TaskCreate

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

def test_get_tasks(client: TestClient, db_session: Session):
    response = client.get("/tasks/")
    assert response.status_code == 200


    tasks = response.json()
    assert isinstance(tasks, list)

    if tasks:
        task = tasks[0]
        assert 'title' in task
        assert 'description' in task
        assert 'deadline' in task
        assert 'is_completed' in task


    expected_task = db_session.query(Task).filter(Task.title == "Test Task").first()
    if expected_task:
        assert any(t['title'] == expected_task.title for t in tasks)
        assert any(t['description'] == expected_task.description for t in tasks)
        assert any(t['deadline'] == expected_task.deadline.isoformat() for t in tasks)
        assert any(t['is_completed'] == expected_task.is_completed for t in tasks)
