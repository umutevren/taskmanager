"""
TaskManager module for the Task Manager application.

This module defines the TaskManager class which is responsible for
managing the collection of tasks and their operations.
"""

import json
import os
from task import Task


class TaskManager:
    """
    A class to manage tasks in the Task Manager application.
    
    This class provides methods to add, view, update, and delete tasks,
    as well as save and load tasks from storage.
    """
    
    def __init__(self, storage_file="tasks.json"):
        """
        Initialize a new TaskManager.
        
        Args:
            storage_file (str, optional): File path to store tasks. Defaults to "tasks.json".
        """
        self.tasks = {}  # Dictionary to store tasks with id as key
        self.storage_file = storage_file
    
    def add_task(self, title, description, priority=3, due_date=None, categories=None):
        """
        Add a new task to the task manager.
        
        Args:
            title (str): The title of the task
            description (str): The description of the task
            priority (int, optional): Priority level (1-5). Defaults to 3.
            due_date (str, optional): Due date in YYYY-MM-DD format. Defaults to None.
            categories (list, optional): List of category strings. Defaults to None.
            
        Returns:
            str: The ID of the new task
        """
        # Input validation
        if not title:
            raise ValueError("Task title cannot be empty")
        
        if not isinstance(priority, int) or priority < 1 or priority > 5:
            raise ValueError("Priority must be an integer between 1 and 5")
        
        # Create and store the task
        task = Task(title, description, priority, due_date, categories)
        self.tasks[task.id] = task
        
        # Save the tasks to file
        self.save_tasks()
        
        return task.id
    
    def get_task(self, task_id):
        """
        Get a task by its ID.
        
        Args:
            task_id (str): The ID of the task to retrieve
            
        Returns:
            Task: The task object if found, None otherwise
        """
        return self.tasks.get(task_id)
    
    def get_all_tasks(self):
        """
        Get all tasks.
        
        Returns:
            list: List of all Task objects
        """
        # Convert to list and sort by priority (highest first)
        return sorted(self.tasks.values(), key=lambda x: (x.completed, x.priority))
    
    def get_tasks_by_priority(self, priority):
        """
        Get tasks with the specified priority.
        
        Args:
            priority (int): Priority level to filter by
            
        Returns:
            list: List of Task objects with the specified priority
        """
        return [task for task in self.tasks.values() if task.priority == priority]
    
    def get_tasks_by_category(self, category):
        """
        Get tasks with the specified category.
        
        Args:
            category (str): Category to filter by (case insensitive)
            
        Returns:
            list: List of Task objects with the specified category
        """
        category = category.lower()  # Make case-insensitive
        return [task for task in self.tasks.values() if category in task.categories]
    
    def get_all_categories(self):
        """
        Get all unique categories used across all tasks.
        
        Returns:
            list: Sorted list of unique category strings
        """
        # Use a set to collect unique categories
        categories = set()
        for task in self.tasks.values():
            categories.update(task.categories)
        
        # Return sorted list
        return sorted(list(categories))
    
    def add_category_to_task(self, task_id, category):
        """
        Add a category to a specific task.
        
        Args:
            task_id (str): The ID of the task
            category (str): The category to add
            
        Returns:
            bool: True if successful, False if task not found or category already exists
        """
        task = self.get_task(task_id)
        if task:
            result = task.add_category(category)
            if result:
                self.save_tasks()
            return result
        return False
    
    def remove_category_from_task(self, task_id, category):
        """
        Remove a category from a specific task.
        
        Args:
            task_id (str): The ID of the task
            category (str): The category to remove
            
        Returns:
            bool: True if successful, False if task not found or category not found
        """
        task = self.get_task(task_id)
        if task:
            result = task.remove_category(category)
            if result:
                self.save_tasks()
            return result
        return False
    
    def mark_task_completed(self, task_id):
        """
        Mark a task as completed.
        
        Args:
            task_id (str): The ID of the task to mark as completed
            
        Returns:
            bool: True if the task was found and marked, False otherwise
        """
        task = self.get_task(task_id)
        if task:
            task.mark_completed()
            self.save_tasks()
            return True
        return False
    
    def delete_task(self, task_id):
        """
        Delete a task.
        
        Args:
            task_id (str): The ID of the task to delete
            
        Returns:
            bool: True if the task was found and deleted, False otherwise
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            self.save_tasks()
            return True
        return False
    
    def search_tasks(self, query):
        """
        Search for tasks containing the query in title, description, or categories.
        
        Args:
            query (str): The search query
            
        Returns:
            list: List of matching Task objects
        """
        query = query.lower()
        results = []
        
        for task in self.tasks.values():
            if (query in task.title.lower() or 
                query in task.description.lower() or
                any(query in category for category in task.categories)):
                results.append(task)
        
        return results
    
    def save_tasks(self):
        """Save all tasks to the storage file."""
        # Convert tasks to dictionary format
        tasks_dict = {task_id: task.to_dict() for task_id, task in self.tasks.items()}
        
        # Write to file
        with open(self.storage_file, 'w') as f:
            json.dump(tasks_dict, f, indent=4)
    
    def load_tasks(self):
        """Load tasks from the storage file if it exists."""
        if not os.path.exists(self.storage_file):
            return
        
        try:
            with open(self.storage_file, 'r') as f:
                tasks_dict = json.load(f)
            
            # Convert dictionary data back to Task objects
            for task_id, task_data in tasks_dict.items():
                self.tasks[task_id] = Task.from_dict(task_data)
                
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading tasks: {e}")
            # If there's an error, start with an empty task list
            self.tasks = {} 