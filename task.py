"""
Task module for the Task Manager application.

This module defines the Task class which represents a single task
in the Task Manager application.
"""

import uuid
from datetime import datetime


class Task:
    """
    A class representing a task in the Task Manager.
    
    Attributes:
        id (str): Unique identifier for the task
        title (str): Brief title of the task
        description (str): Detailed description of the task
        priority (int): Priority level (1-5, with 1 being highest)
        created_at (datetime): When the task was created
        due_date (datetime, optional): When the task is due
        completed (bool): Whether the task is completed
        categories (list): List of categories/tags assigned to the task
    """
    
    def __init__(self, title, description, priority=3, due_date=None, categories=None):
        """
        Initialize a new Task object.
        
        Args:
            title (str): The title of the task
            description (str): The description of the task
            priority (int, optional): Priority level from 1-5 (1 highest). Defaults to 3.
            due_date (str, optional): Due date in format YYYY-MM-DD. Defaults to None.
            categories (list, optional): List of categories/tags. Defaults to empty list.
        """
        self.id = str(uuid.uuid4())[:8]  # Generate a shorter unique ID
        self.title = title
        self.description = description
        self.priority = priority
        self.created_at = datetime.now()
        self.completed = False
        self.categories = categories or []  # Default to empty list if None
        
        # Parse the due_date if provided
        self.due_date = None
        if due_date:
            try:
                self.due_date = datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                # If date format is incorrect, just leave it as None
                print(f"Warning: Invalid date format '{due_date}'. Expected YYYY-MM-DD.")
    
    def mark_completed(self):
        """Mark the task as completed."""
        self.completed = True
    
    def is_overdue(self):
        """
        Check if the task is overdue.
        
        Returns:
            bool: True if the task is overdue, False otherwise
        """
        if not self.due_date or self.completed:
            return False
            
        return datetime.now() > self.due_date
    
    def add_category(self, category):
        """
        Add a category to the task.
        
        Args:
            category (str): The category to add
            
        Returns:
            bool: True if the category was added, False if it already exists
        """
        # Make sure category is a string and convert to lowercase for consistency
        category = str(category).strip().lower()
        
        if not category:
            return False  # Don't add empty categories
        
        if category not in self.categories:
            self.categories.append(category)
            return True
            
        return False  # Category already exists
    
    def remove_category(self, category):
        """
        Remove a category from the task.
        
        Args:
            category (str): The category to remove
            
        Returns:
            bool: True if the category was removed, False if it wasn't found
        """
        # Make sure category is a string and convert to lowercase for consistency
        category = str(category).strip().lower()
        
        if category in self.categories:
            self.categories.remove(category)
            return True
            
        return False  # Category not found
    
    def to_dict(self):
        """
        Convert task to dictionary for serialization.
        
        Returns:
            dict: Dictionary representation of the task
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'created_at': self.created_at.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed': self.completed,
            'categories': self.categories
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Task instance from a dictionary.
        
        Args:
            data (dict): Dictionary containing task data
            
        Returns:
            Task: A new Task instance
        """
        # Create a basic task
        task = cls(
            title=data['title'],
            description=data['description'],
            priority=data['priority'],
            due_date=None,  # We'll set this manually below
            categories=data.get('categories', [])  # Handle legacy data without categories
        )
        
        # Set the remaining attributes
        task.id = data['id']
        task.completed = data['completed']
        
        # Parse the dates
        task.created_at = datetime.fromisoformat(data['created_at'])
        if data['due_date']:
            task.due_date = datetime.fromisoformat(data['due_date'])
        
        return task
    
    def __str__(self):
        """
        Return a string representation of the task.
        
        Returns:
            str: String representation
        """
        status = "✓" if self.completed else "✗"
        priority_str = "!" * self.priority
        due_str = f", Due: {self.due_date.strftime('%Y-%m-%d')}" if self.due_date else ""
        overdue = " (OVERDUE!)" if self.is_overdue() else ""
        
        # Add categories if they exist
        category_str = ""
        if self.categories:
            categories_formatted = ", ".join(f"#{cat}" for cat in self.categories)
            category_str = f" [{categories_formatted}]"
        
        return f"[{self.id}] {status} {self.title} ({priority_str}){due_str}{overdue}{category_str}" 