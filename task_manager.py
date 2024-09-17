from datetime import datetime
import uuid

class Task:

	def __init__(self, title, description, completed=False, created_at=None, id=None, completed_at=None, time=None):
		self.title = title
		self.description = description
		self.completed = completed
		self.created_at = created_at if created_at else datetime.now().isoformat()
		self.completed_at = completed_at
		self.id = id if id else str(uuid.uuid4()) 
		self.time = time

class TaskManager:

	def __init__(self, storage):
		self.storage = storage

	def add_task(self, title, description):
		try:	
			task = self.storage.get_task(title)
			if task:
				raise ValueError(f"Task with title '{title}' already exists.")

			newTask = Task(title, description)
			self.storage.save_task(newTask)
			
			return newTask

		except ValueError as e:
			print(e)
			
			return None
		

	def complete_task(self, title):
		task = self.storage.get_task(title)
		if task:
            
			if not task.completed:
                
				task.completed = True
                
				task.completed_at = datetime.now().isoformat()

				created_time = datetime.fromisoformat(task.created_at)
                
				completed_time = datetime.fromisoformat(task.completed_at)
                
				time_diff = completed_time - created_time
                
				task.time = self.format_timedelta(time_diff)
                
				self.storage.update_task(task)
                
				return True
            
			else:
                
				print(f"Task '{title}' is already completed.")
                
				return False
        
		return False

	def format_timedelta(self, time_diff):
		hours, remainder = divmod(time_diff.total_seconds(), 3600)
		minutes, seconds = divmod(remainder, 60)

		return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

	def list_tasks(self, include_completed=False):
		tasks = self.storage.get_all_tasks()
		if not include_completed:	
			tasks = [task for task in tasks if not task.completed]
    	
		return tasks

	def generate_report(self):
		tasks = self.storage.get_all_tasks()
		total_tasks = len(tasks)
		completed_tasks = [task for task in tasks if task.completed]
		pending_tasks = total_tasks - len(completed_tasks)
		total_time = sum(
            (datetime.fromisoformat(task.completed_at) - datetime.fromisoformat(task.created_at)).total_seconds()
            for task in completed_tasks if task.completed_at and task.created_at
        )
		average_time = total_time / len(completed_tasks) if completed_tasks else 0
		avg_time_formatted = self.format_timedelta_avg_time(average_time)
		report = {
            "total": total_tasks,
            "completed": len(completed_tasks),
            "pending": pending_tasks,
            "average_time": avg_time_formatted
        }

		return report

    
	def format_timedelta_avg_time(self, total_seconds):
		hours, remainder = divmod(total_seconds, 3600)
		minutes, seconds = divmod(remainder, 60)
        
		return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

