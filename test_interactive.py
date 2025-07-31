#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for interactive menu functionality.
This script demonstrates the new interactive CLI interface.
"""

import os
import sys

def test_interactive_menu():
    """Test the interactive menu functionality."""
    print("Testing Interactive Menu Functionality")
    print("=" * 40)
    
    # Check if inquirer is available
    try:
        import inquirer
        print("✓ inquirer package is available")
    except ImportError:
        print("✗ inquirer package is not installed")
        print("Install it with: pip install inquirer")
        return False
    
    # Check if file_organizer.py exists
    if os.path.exists('file_organizer.py'):
        print("✓ file_organizer.py found")
    else:
        print("✗ file_organizer.py not found")
        return False
    
    print("\nTo test the interactive menu:")
    print("1. Run: python file_organizer.py")
    print("2. Use arrow keys to navigate the menu")
    print("3. Press Enter to select options")
    print("4. Follow the prompts to configure your command")
    
    print("\nInteractive menu features:")
    print("• Language selection (English/Chinese)")
    print("• Command selection (organize/undo/stats/analyze)")
    print("• Parameter configuration with visual prompts")
    print("• File/directory browser integration")
    print("• Automatic command execution")
    
    return True

if __name__ == '__main__':
    success = test_interactive_menu()
    if success:
        print("\n✓ Interactive menu setup complete!")
        print("Run 'python file_organizer.py' to start the interactive interface.")
    else:
        print("\n✗ Setup incomplete. Please check the requirements.")
        sys.exit(1)