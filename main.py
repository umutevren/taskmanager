#!/usr/bin/env python3
"""
Task Manager - A simple task management application

This module serves as the entry point for the Task Manager application.
It handles the command-line interface and user interaction.

Usage:
    python main.py
"""

import os
import sys
from task_manager import TaskManager
from utils import clear_screen, print_colored


def display_menu():
    """Display the main menu options."""
    print("\n===== Task Manager =====")
    print("1. Add a new task")
    print("2. View all tasks")
    print("3. View tasks by priority")
    print("4. Mark task as completed")
    print("5. Delete a task")
    print("6. Search tasks")
    print("7. Exit")
    print("=======================")


def main():
    """Main function to run the application."""
    # Initialize the task manager
    task_manager = TaskManager()
    
    # Load any existing tasks from storage
    task_manager.load_tasks()
    
    while True:
        clear_screen()
        display_menu()
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == '1':
            # Add a new task
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            
            # Let's make sure priority is a number
            while True:
                try:
                    priority = int(input("Enter priority (1-5, 1 being highest): "))
                    if 1 <= priority <= 5:
                        break
                    else:
                        print("Priority must be between 1 and 5.")
                except ValueError:
                    print("Please enter a valid number.")
            
            due_date = input("Enter due date (YYYY-MM-DD) or leave blank: ")
            
            task_id = task_manager.add_task(title, description, priority, due_date)
            print_colored(f"\nTask added successfully with ID: {task_id}", "green")
        
        elif choice == '2':
            # View all tasks
            tasks = task_manager.get_all_tasks()
            if tasks:
                print("\n=== All Tasks ===")
                for task in tasks:
                    print(task)
            else:
                print_colored("\nNo tasks found!", "yellow")
        
        elif choice == '3':
            # View tasks by priority
            while True:
                try:
                    priority = int(input("Enter priority level (1-5): "))
                    if 1 <= priority <= 5:
                        break
                    else:
                        print("Priority must be between 1 and 5.")
                except ValueError:
                    print("Please enter a valid number.")
            
            tasks = task_manager.get_tasks_by_priority(priority)
            if tasks:
                print(f"\n=== Priority {priority} Tasks ===")
                for task in tasks:
                    print(task)
            else:
                print_colored(f"\nNo tasks with priority {priority} found!", "yellow")
        
        elif choice == '4':
            # Mark task as completed
            task_id = input("Enter task ID to mark as completed: ")
            if task_manager.mark_task_completed(task_id):
                print_colored("\nTask marked as completed!", "green")
            else:
                print_colored("\nTask not found!", "red")
        
        elif choice == '5':
            # Delete a task
            task_id = input("Enter task ID to delete: ")
            if task_manager.delete_task(task_id):
                print_colored("\nTask deleted successfully!", "green")
            else:
                print_colored("\nTask not found!", "red")
        
        elif choice == '6':
            # Search tasks
            query = input("Enter search term: ")
            results = task_manager.search_tasks(query)
            
            if results:
                print(f"\n=== Search Results for '{query}' ===")
                for task in results:
                    print(task)
            else:
                print_colored(f"\nNo tasks found matching '{query}'", "yellow")
        
        elif choice == '7':
            # Exit the application
            print_colored("\nSaving tasks and exiting...", "blue")
            task_manager.save_tasks()
            print("Goodbye!")
            sys.exit(0)
        
        else:
            print_colored("\nInvalid choice! Please enter a number between 1 and 7.", "red")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication terminated by user. Saving data...")
        # This is a bit of a hack - we create a new manager just to save tasks
        # In a more robust application, we'd handle this differently
        TaskManager().save_tasks()
        sys.exit(0) 