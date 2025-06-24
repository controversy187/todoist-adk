"""
ToDoist API tools for task management.
These are the core functions that the ToDoistToolAgent will use.
"""

import os
from typing import List, Dict, Optional
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Default project name
DEFAULT_PROJECT = "Work"


def get_todoist_headers():
    """Get headers for ToDoist API requests."""
    api_token = os.getenv('TODOIST_API_TOKEN')
    if not api_token:
        raise ValueError("TODOIST_API_TOKEN not found in environment variables")
    
    return {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }


def get_work_project_id():
    """Get the project ID for the 'Work' project."""
    try:
        headers = get_todoist_headers()
        base_url = os.getenv('TODOIST_API_BASE_URL', 'https://api.todoist.com/rest/v2')
        
        # Get all projects
        response = requests.get(f'{base_url}/projects', headers=headers)
        response.raise_for_status()
        projects = response.json()
        
        # Find the Work project
        for project in projects:
            if project.get('name', '').lower() == DEFAULT_PROJECT.lower():
                print(f"Found Work project ID: {project['id']}")
                return project['id']
        
        # If Work project not found, return None
        return None
        
    except Exception as e:
        print(f"Error getting Work project ID: {e}")
        return None


def get_open_tasks(project_name: Optional[str] = None) -> List[Dict]:
    """
    Fetches all open tasks from the Work project in ToDoist.
    
    Args:
        project_name (Optional[str]): Ignored - always uses "Work" project.
        
    Returns:
        List[Dict]: A list of task objects with their details.
    """
    try:
        headers = get_todoist_headers()
        base_url = os.getenv('TODOIST_API_BASE_URL', 'https://api.todoist.com/rest/v2')
        
        # Get the Work project ID
        work_project_id = get_work_project_id()
        if not work_project_id:
            print(f"Work project not found. Please create a project named '{DEFAULT_PROJECT}' in ToDoist.")
            return []
        
        # Get all tasks
        response = requests.get(f'{base_url}/tasks', headers=headers)
        response.raise_for_status()
        
        tasks = response.json()
        
        # Filter for open tasks in the Work project only
        open_tasks = [
            task for task in tasks 
            if not task.get('is_completed', False) and task.get('project_id') == work_project_id
        ]
        
        # Format the response to match our expected structure
        formatted_tasks = []
        for task in open_tasks:
            formatted_task = {
                'id': str(task.get('id')),
                'content': task.get('content', ''),
                'project_id': task.get('project_id'),
                'priority': task.get('priority', 1),
                'description': task.get('description', ''),
                'due': task.get('due', {}),
                'url': task.get('url', ''),
                'created': task.get('created', ''),
                'labels': task.get('labels', [])
            }
            formatted_tasks.append(formatted_task)
        
        return formatted_tasks
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching tasks from ToDoist API: {e}")
        # Fallback to mock data for testing
        return [
            {
                "id": "1",
                "content": "Test task 1 (API Error Fallback)",
                "project_name": DEFAULT_PROJECT,
                "due": {"date": "2024-01-15"},
                "priority": 2,
                "description": "This is a fallback task due to API error"
            }
        ]
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


def create_task(project_name: str, content: str, due_string: str, priority: int, description: str = "") -> Dict:
    """
    Creates a new task in the Work project in ToDoist.
    
    Args:
        project_name (str): Ignored - always uses "Work" project.
        content (str): The main title of the task.
        due_string (str): A human-readable due date (e.g., "tomorrow at 5pm").
        priority (int): The priority level (1=Normal, 2=Medium, 3=High, 4=Urgent).
        description (str): A detailed description or notes for the task.
        
    Returns:
        Dict: A dictionary representing the newly created task.
    """
    try:
        headers = get_todoist_headers()
        base_url = os.getenv('TODOIST_API_BASE_URL', 'https://api.todoist.com/rest/v2')
        
        # Get the Work project ID
        work_project_id = get_work_project_id()
        if not work_project_id:
            print(f"Work project not found. Please create a project named '{DEFAULT_PROJECT}' in ToDoist.")
            return {"error": "Work project not found"}
        
        # Prepare task data
        task_data = {
            'content': content,
            'project_id': work_project_id,
            'priority': priority,
            'description': description
        }
        
        # Add due date if provided
        if due_string:
            task_data['due_string'] = due_string
        
        # Create the task
        response = requests.post(f'{base_url}/tasks', headers=headers, json=task_data)
        response.raise_for_status()
        
        created_task = response.json()
        
        return {
            "id": str(created_task.get('id')),
            "content": created_task.get('content', content),
            "project_id": created_task.get('project_id'),
            "priority": created_task.get('priority', priority),
            "description": created_task.get('description', description),
            "due": created_task.get('due', {}),
            "status": "created"
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Error creating task in ToDoist API: {e}")
        return {"error": f"API error: {e}"}
    except Exception as e:
        print(f"Unexpected error creating task: {e}")
        return {"error": f"Unexpected error: {e}"} 