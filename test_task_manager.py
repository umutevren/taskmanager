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
        self.assertEqual(task.categories, [])  # Default empty list
        
        # Check due date parsing
        self.assertIsNotNone(task.due_date)
        self.assertEqual(task.due_date.year, 2023)
        self.assertEqual(task.due_date.month, 12)
        self.assertEqual(task.due_date.day, 31)
        
        # Create a task with categories
        task_with_categories = Task(
            "Task with Categories", "Description", 2, categories=["work", "urgent"]
        )
        self.assertEqual(task_with_categories.categories, ["work", "urgent"])
    
    def test_mark_completed(self):
        """Test marking a task as completed."""
        task = Task("Test Task", "This is a test task")
        self.assertFalse(task.completed)
        
        task.mark_completed()
        self.assertTrue(task.completed)
    
    def test_add_remove_category(self):
        """Test adding and removing categories."""
        task = Task("Test Task", "This is a test task")
        
        # Add a category
        result = task.add_category("work")
        self.assertTrue(result)
        self.assertIn("work", task.categories)
        
        # Add the same category again
        result = task.add_category("work")
        self.assertFalse(result)  # Should return False when category already exists
        self.assertEqual(len(task.categories), 1)  # Should still have just one entry
        
        # Add another category
        result = task.add_category("URGENT")  # Test case conversion
        self.assertTrue(result)
        self.assertIn("urgent", task.categories)  # Should be stored as lowercase
        
        # Remove a category
        result = task.remove_category("work")
        self.assertTrue(result)
        self.assertNotIn("work", task.categories)
        
        # Try to remove a non-existent category
        result = task.remove_category("non-existent")
        self.assertFalse(result)
    
    def test_to_dict_and_from_dict(self):
        """Test conversion to and from dictionary."""
        # Create a task with categories
        original_task = Task(
            "Test Task", "This is a test task", 2, "2023-12-31", ["work", "urgent"]
        )
        
        # Convert to dict
        task_dict = original_task.to_dict()
        
        # Check dict values
        self.assertEqual(task_dict['title'], "Test Task")
        self.assertEqual(task_dict['description'], "This is a test task")
        self.assertEqual(task_dict['priority'], 2)
        self.assertFalse(task_dict['completed'])
        self.assertEqual(task_dict['categories'], ["work", "urgent"])
        
        # Convert back to Task
        reconstructed_task = Task.from_dict(task_dict)
        
        # Check reconstructed task
        self.assertEqual(reconstructed_task.id, original_task.id)
        self.assertEqual(reconstructed_task.title, original_task.title)
        self.assertEqual(reconstructed_task.description, original_task.description)
        self.assertEqual(reconstructed_task.priority, original_task.priority)
        self.assertEqual(reconstructed_task.completed, original_task.completed)
        self.assertEqual(reconstructed_task.categories, original_task.categories)


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
        # Add a task with categories
        task_id = self.task_manager.add_task(
            "Test Task", "This is a test task", 1, "2023-12-31", ["work", "urgent"]
        )
        
        # Check that the task was added
        self.assertIn(task_id, self.task_manager.tasks)
        
        # Check that the task has the right properties
        task = self.task_manager.get_task(task_id)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "This is a test task")
        self.assertEqual(task.priority, 1)
        self.assertEqual(task.categories, ["work", "urgent"])
    
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
    
    def test_get_tasks_by_category(self):
        """Test getting tasks by category."""
        # Add tasks with categories
        id1 = self.task_manager.add_task(
            "Work Task", "A work task", 1, categories=["work"]
        )
        id2 = self.task_manager.add_task(
            "Home Task", "A home task", 2, categories=["home"]
        )
        id3 = self.task_manager.add_task(
            "Urgent Work", "An urgent work task", 1, categories=["work", "urgent"]
        )
        
        # Get tasks by category
        work_tasks = self.task_manager.get_tasks_by_category("work")
        home_tasks = self.task_manager.get_tasks_by_category("home")
        urgent_tasks = self.task_manager.get_tasks_by_category("urgent")
        
        # Check counts
        self.assertEqual(len(work_tasks), 2)
        self.assertEqual(len(home_tasks), 1)
        self.assertEqual(len(urgent_tasks), 1)
        
        # Check specific tasks
        work_ids = [task.id for task in work_tasks]
        self.assertIn(id1, work_ids)
        self.assertIn(id3, work_ids)
        self.assertNotIn(id2, work_ids)
    
    def test_get_all_categories(self):
        """Test getting all categories."""
        # Add tasks with categories
        self.task_manager.add_task(
            "Work Task", "A work task", 1, categories=["work"]
        )
        self.task_manager.add_task(
            "Home Task", "A home task", 2, categories=["home"]
        )
        self.task_manager.add_task(
            "Urgent Work", "An urgent work task", 1, categories=["work", "urgent"]
        )
        
        # Get all categories
        categories = self.task_manager.get_all_categories()
        
        # Check that we have the right categories
        self.assertEqual(len(categories), 3)
        self.assertIn("work", categories)
        self.assertIn("home", categories)
        self.assertIn("urgent", categories)
        
        # Should be sorted
        self.assertEqual(categories, sorted(categories))
    
    def test_add_remove_category_from_task(self):
        """Test adding and removing categories from a task."""
        # Add a task
        task_id = self.task_manager.add_task("Test Task", "Description")
        
        # Add a category to the task
        result = self.task_manager.add_category_to_task(task_id, "work")
        self.assertTrue(result)
        self.assertIn("work", self.task_manager.get_task(task_id).categories)
        
        # Add another category
        result = self.task_manager.add_category_to_task(task_id, "urgent")
        self.assertTrue(result)
        self.assertIn("urgent", self.task_manager.get_task(task_id).categories)
        
        # Remove a category
        result = self.task_manager.remove_category_from_task(task_id, "work")
        self.assertTrue(result)
        self.assertNotIn("work", self.task_manager.get_task(task_id).categories)
        
        # Try with non-existent task ID
        result = self.task_manager.add_category_to_task("non-existent", "category")
        self.assertFalse(result)
        
        result = self.task_manager.remove_category_from_task("non-existent", "category")
        self.assertFalse(result)
    
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
        # Add some tasks with categories
        self.task_manager.add_task(
            "Apple Task", "A task about apples", 1, categories=["fruit"]
        )
        self.task_manager.add_task(
            "Banana Task", "A task about bananas", 2, categories=["fruit", "yellow"]
        )
        self.task_manager.add_task(
            "Work Task", "An important task", 1, categories=["work", "important"]
        )
        
        # Search for tasks containing "apple" in title/description
        results = self.task_manager.search_tasks("apple")
        self.assertEqual(len(results), 1)
        
        # Search for tasks containing "fruit" in categories
        results = self.task_manager.search_tasks("fruit")
        self.assertEqual(len(results), 2)
        
        # Search for tasks containing "important" in categories
        results = self.task_manager.search_tasks("important")
        self.assertEqual(len(results), 1)


if __name__ == "__main__":
    unittest.main() 