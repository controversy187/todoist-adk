#!/usr/bin/env python3
"""
Test script to verify ToDoist API integration.
"""

import os
from dotenv import load_dotenv
from tools.todoist_tools import get_open_tasks, get_todoist_headers

# Load environment variables
load_dotenv()


def test_api_connection():
    """Test basic API connection and authentication."""
    print("=== Testing ToDoist API Connection ===\n")
    
    try:
        # Test headers creation
        headers = get_todoist_headers()
        print(f"✅ API headers created successfully")
        print(f"   Authorization: Bearer {headers['Authorization'][:20]}...")
        
        # Test API token presence
        api_token = os.getenv('TODOIST_API_TOKEN')
        if api_token:
            print(f"✅ TODOIST_API_TOKEN found in environment")
        else:
            print(f"❌ TODOIST_API_TOKEN not found in environment")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing API connection: {e}")
        return False


def test_get_tasks():
    """Test fetching tasks from the Work project."""
    print("\n=== Testing Task Retrieval from Work Project ===\n")
    
    try:
        # Test getting tasks from Work project
        print("Fetching tasks from Work project...")
        work_tasks = get_open_tasks()
        print(f"✅ Retrieved {len(work_tasks)} open tasks from Work project")
        
        if work_tasks:
            print("\nTasks in Work project:")
            for i, task in enumerate(work_tasks[:5]):  # Show first 5 tasks
                print(f"  {i+1}. {task.get('content', 'No content')}")
                print(f"     Priority: {task.get('priority', 'Unknown')}")
                print(f"     Due: {task.get('due', 'No due date')}")
                print()
        else:
            print("No tasks found in Work project.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing task retrieval: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=== ToDoist API Integration Test (Work Project) ===\n")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please create a .env file with your TODOIST_API_TOKEN")
        print("You can copy from .env_sample as a starting point")
        exit(1)
    
    # Run tests
    connection_ok = test_api_connection()
    
    if connection_ok:
        tasks_ok = test_get_tasks()
        if tasks_ok:
            print("\n✅ All API tests passed! ToDoist integration is working with Work project.")
        else:
            print("\n❌ Task retrieval test failed.")
    else:
        print("\n❌ API connection test failed.") 