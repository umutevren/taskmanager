"""
Utility functions for the Task Manager application.

This module contains helper functions used throughout the application.
"""

import os
import platform


def clear_screen():
    """
    Clear the terminal screen.
    
    This function detects the operating system and uses the appropriate
    command to clear the terminal screen.
    """
    # Check the operating system
    if platform.system() == "Windows":
        os.system("cls")
    else:  # For Linux and Mac
        os.system("clear")


def print_colored(text, color):
    """
    Print text in the specified color.
    
    Args:
        text (str): The text to print
        color (str): The color to use ('red', 'green', 'yellow', 'blue')
    """
    # ANSI color codes
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'reset': '\033[0m'
    }
    
    # Check if the color is supported
    if color not in colors:
        # If not, just print the text normally
        print(text)
        return
    
    # Print the colored text
    print(f"{colors[color]}{text}{colors['reset']}")


def get_priority_emoji(priority):
    """
    Convert a priority level to an emoji representation.
    
    Args:
        priority (int): Priority level (1-5)
        
    Returns:
        str: Emoji representation of the priority
    """
    # Map priority levels to emojis
    priority_emojis = {
        1: "🔴",  # Highest priority
        2: "🟠",
        3: "🟡",
        4: "🟢",
        5: "🔵",  # Lowest priority
    }
    
    return priority_emojis.get(priority, "❓")  # Default to question mark if invalid 