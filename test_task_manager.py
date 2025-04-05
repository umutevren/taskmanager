"""
Test module for the Task Manager application.

This module contains simple tests for the Task and TaskManager classes.
"""

import os
import unittest
from datetime import datetime
from task import Task
from task_manager import TaskManager


class TestTask(unittest.TestCase):
    """Tests for the Task class."""
    
    def test_task_creation(self):
        """Test that a task is created with the correct attributes."""
        # Create a task
        task = Task("Test Task", "This is a test task", 1, "2023-12-31")
        
        # Check basic attributes
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "This is a test task")
        self.assertEqual(task.priority, 1)
        self.assertFalse(task.completed)
        
        # Check due date parsing
        self.assertIsNotNone(task.due_date)
        self.assertEqual(task.due_date.year, 2023)
        self.assertEqual(task.due_date.month, 12)
        self.assertEqual(task.due_date.day, 31)
    
    def test_mark_completed(self):
        """Test marking a task as completed."""
        task = Task("Test Task", "This is a test task")
        self.assertFalse(task.completed)
        
        task.mark_completed()
        self.assertTrue(task.completed)
    
    def test_to_dict_and_from_dict(self):
        """Test conversion to and from dictionary."""
        # Create a task
        original_task = Task("Test Task", "This is a test task", 2, "2023-12-31")
        
        # Convert to dict
        task_dict = original_task.to_dict()
        
        # Check dict values
        self.assertEqual(task_dict['title'], "Test Task")
        self.assertEqual(task_dict['description'], "This is a test task")
        self.assertEqual(task_dict['priority'], 2)
        self.assertFalse(task_dict['completed'])
        
        # Convert back to Task
        reconstructed_task = Task.from_dict(task_dict)
        
        # Check reconstructed task
        self.assertEqual(reconstructed_task.id, original_task.id)
        self.assertEqual(reconstructed_task.title, original_task.title)
        self.assertEqual(reconstructed_task.description, original_task.description)
        self.assertEqual(reconstructed_task.priority, original_task.priority)
        self.assertEqual(reconstructed_task.completed, original_task.completed)


class TestTaskManager(unittest.TestCase):
    """Tests for the TaskManager class."""
    
    def setUp(self):
        """Set up test environment."""
        # Use a test-specific storage file
        self.test_file = "test_tasks.json"
        self.task_manager = TaskManager(self.test_file)
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove the test file if it exists
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_add_task(self):
        """Test adding a task."""
        # Add a task
        task_id = self.task_manager.add_task(
            "Test Task", "This is a test task", 1, "2023-12-31"
        )
        
        # Check that the task was added
        self.assertIn(task_id, self.task_manager.tasks)
        
        # Check that the task has the right properties
        task = self.task_manager.get_task(task_id)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "This is a test task")
        self.assertEqual(task.priority, 1)
    
    def test_get_all_tasks(self):
        """Test getting all tasks."""
        # Add some tasks
        id1 = self.task_manager.add_task("Task 1", "Description 1", 1)
        id2 = self.task_manager.add_task("Task 2", "Description 2", 2)
        id3 = self.task_manager.add_task("Task 3", "Description 3", 3)
        
        # Get all tasks
        tasks = self.task_manager.get_all_tasks()
        
        # Check that we have 3 tasks
        self.assertEqual(len(tasks), 3)
        
        # Check that tasks are sorted by priority
        self.assertEqual(tasks[0].id, id1)
        self.assertEqual(tasks[1].id, id2)
        self.assertEqual(tasks[2].id, id3)
    
    def test_mark_task_completed(self):
        """Test marking a task as completed."""
        # Add a task
        task_id = self.task_manager.add_task("Test Task", "Description")
        
        # Mark it as completed
        result = self.task_manager.mark_task_completed(task_id)
        
        # Check the result and task status
        self.assertTrue(result)
        self.assertTrue(self.task_manager.get_task(task_id).completed)
    
    def test_delete_task(self):
        """Test deleting a task."""
        # Add a task
        task_id = self.task_manager.add_task("Test Task", "Description")
        
        # Delete it
        result = self.task_manager.delete_task(task_id)
        
        # Check the result and task list
        self.assertTrue(result)
        self.assertNotIn(task_id, self.task_manager.tasks)
    
    def test_search_tasks(self):
        """Test searching for tasks."""
        # Add some tasks
        self.task_manager.add_task("Apple Task", "A task about apples", 1)
        self.task_manager.add_task("Banana Task", "A task about bananas", 2)
        self.task_manager.add_task("Apple and Banana", "Both fruits", 3)
        
        # Search for tasks containing "apple"
        results = self.task_manager.search_tasks("apple")
        
        # Should find 2 tasks
        self.assertEqual(len(results), 2)
        
        # Search for tasks containing "banana"
        results = self.task_manager.search_tasks("banana")
        
        # Should find 2 tasks
        self.assertEqual(len(results), 2)
        
        # Search for tasks containing "fruit"
        results = self.task_manager.search_tasks("fruit")
        
        # Should find 1 task
        self.assertEqual(len(results), 1)


if __name__ == "__main__":
    unittest.main() 