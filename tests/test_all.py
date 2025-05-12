import pytest
from datetime import date, timedelta
from app.models.task import Task
from app.controllers.tasks_controller import create_task, get_tasks, update_task

@pytest.fixture
def sample_task():
    return {
        'title': 'Test Task',
        'description': 'Test Description',
        'due_date': date.today() + timedelta(days=1),
        'priority': 'high',
        'status': 'pending'
    }

def test_task_creation(sample_task):
    task = create_task(**sample_task)
    assert task.id is not None
    assert task.title == sample_task['title']

def test_get_tasks(sample_task):
    create_task(**sample_task)
    tasks = get_tasks()
    assert len(tasks) > 0
    assert any(t.title == sample_task['title'] for t in tasks)
