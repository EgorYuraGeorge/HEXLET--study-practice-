from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import case, and_
from app.models.db import SessionLocal
from app.models.task import Task
from typing import Optional, Dict, List


class TaskController:
    def __init__(self) -> None:
        self.session: Session = SessionLocal()

    def __del__(self) -> None:
        self.session.close()

    def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        due_date: Optional[date] = None,
        priority: str = 'medium',
        status: str = 'pending',
        tag: Optional[str] = None
    ) -> Task:
        """Создание новой задачи"""
        try:
            if not title:
                raise ValueError("Title is required")

            if due_date and due_date < date.today():
                raise ValueError("Due date cannot be in the past")

            valid_priorities = ['low', 'medium', 'high']
            if priority not in valid_priorities:
                raise ValueError(f"Priority must be one of {valid_priorities}")

            task = Task(
                title=title,
                description=description,
                due_date=due_date,
                priority=priority,
                status=status,
                tag=tag
            )
            self.session.add(task)
            self.session.commit()
            return task
        except Exception as e:
            self.session.rollback()
            raise e

    def get_tasks(
        self,
        filters: Optional[Dict[str, str]] = None,
        sort_by: Optional[str] = None
    ) -> List[Task]:
        """Получение задач с фильтрацией и сортировкой"""
        query = self.session.query(Task)

        # Фильтры
        if filters:
            conditions = []
            if 'status' in filters:
                conditions.append(Task.status == filters['status'])
            if 'priority' in filters:
                conditions.append(Task.priority == filters['priority'])
            if 'tag' in filters:
                conditions.append(Task.tag == filters['tag'])

            if conditions:
                query = query.filter(and_(*conditions))

        # Сортировка
        if sort_by == 'due_date':
            query = query.order_by(Task.due_date.asc())
        elif sort_by == 'priority':
            priority_order = case(
                (Task.priority == 'high', 1),
                (Task.priority == 'medium', 2),
                (Task.priority == 'low', 3),
                else_=4
            )
            query = query.order_by(priority_order)

        return query.all()

    def update_task(self, task_id: int, **kwargs) -> Task:
        """Обновление задачи"""
        try:
            task = self.session.get(Task, task_id)
            if not task:
                raise ValueError("Task not found")

            if 'due_date' in kwargs:
                due = kwargs['due_date']
                if due and isinstance(due, date) and due < date.today():
                    raise ValueError("Due date cannot be in the past")

            for key, value in kwargs.items():
                setattr(task, key, value)

            self.session.commit()
            return task
        except Exception as e:
            self.session.rollback()
            raise e

    def delete_task(self, task_id: int) -> None:
        """Удаление задачи"""
        try:
            task = self.session.get(Task, task_id)
            if not task:
                raise ValueError("Task not found")

            self.session.delete(task)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
