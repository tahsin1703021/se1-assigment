import json
import os
from task_manager import Task

class Storage:

    def __init__(self, file_path="tasks.json"):
        self.file_path = file_path
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                tasks_data = json.load(f)
                return [Task(**task_data) for task_data in tasks_data] 
        return []

    def _save_tasks(self):
        with open(self.file_path, "w") as f:
            tasks_data = [task.__dict__ for task in self.tasks]
            json.dump(tasks_data, f)

    def save_task(self, task):
        self.tasks.append(task)
        self._save_tasks()

    def update_task(self, updated_task):
        for i, task in enumerate(self.tasks):
            if task.title == updated_task.title:
                self.tasks[i] = updated_task
                break
        self._save_tasks()

    def get_task(self, title):
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    def get_all_tasks(self):
        return list(self.tasks)

    def clear_all_tasks(self):
        self.tasks = []
        self._save_tasks()
