import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from task_manager import Task, TaskManager


class TestTaskManager(unittest.TestCase):

	def setUp(self):
		self.storage = MagicMock()
		self.manager = TaskManager(self.storage)

	def test_add_task(self):
		self.storage.get_task.return_value = None

		task = self.manager.add_task("Buy a Car", "Description")
		
		self.storage.save_task.assert_called_once()
		self.assertEqual(task.title, "Buy a Car")
		self.assertEqual(task.description, "Description")


	def test_list_tasks_exclude_completed(self):
		tasks = [
		    Task("Buy a Car", "Must be a 4 wheeler"),
		    Task("Buy a House", "Must have a basketball court"),
		    Task("Play basketball", "Need to train a lot more")
		]
		tasks[1].completed = True
		self.storage.get_all_tasks.return_value = tasks
		result = self.manager.list_tasks()
		self.assertEqual(len(result), 2)
		self.assertNotIn(tasks[1], result)

	def test_generate_report(self):
		tasks = [
			Task("Buy a Car", "Must be a 4 wheeler"),
		    Task("Buy a House", "Must have a basketball court"),
		    Task("Play basketball", "Need to train a lot more")
		]
		
		tasks[0].completed = True
		tasks[1].completed = True  # Mark another task as completed

		self.storage.get_all_tasks.return_value = tasks
		report = self.manager.generate_report()
		
		self.assertEqual(report["total"], 3)
		self.assertEqual(report["completed"], 2)  # Now two tasks are completed
		self.assertEqual(report["pending"], 1)


	def test_complete_nonexistent_task(self):
		self.storage.get_task.return_value = None
		result = self.manager.complete_task("Non-existent Task")
		self.assertFalse(result)


if __name__ == "__main__":
	unittest.main()
