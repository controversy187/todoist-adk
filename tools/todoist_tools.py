"""
ToDoist API tools for task management.
These are the core functions that the ToDoistToolAgent will use.
"""

import os
from typing import List, Dict, Optional
from datetime import datetime, timezone
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


def get_task_comments(task_id: str) -> List[Dict]:
    """
    Fetches all comments for a specific task.
    
    Args:
        task_id (str): The ID of the task to get comments for.
        
    Returns:
        List[Dict]: A list of comment objects.
    """
    try:
        headers = get_todoist_headers()
        base_url = os.getenv('TODOIST_API_BASE_URL', 'https://api.todoist.com/rest/v2')
        
        response = requests.get(f'{base_url}/comments?task_id={task_id}', headers=headers)
        response.raise_for_status()
        
        comments = response.json()
        return comments
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching comments for task {task_id}: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error fetching comments: {e}")
        return []


def get_task_subtasks(task_id: str) -> List[Dict]:
    """
    Fetches all subtasks for a specific task.
    
    Args:
        task_id (str): The ID of the task to get subtasks for.
        
    Returns:
        List[Dict]: A list of subtask objects.
    """
    try:
        headers = get_todoist_headers()
        base_url = os.getenv('TODOIST_API_BASE_URL', 'https://api.todoist.com/rest/v2')
        
        # Get all tasks and filter for subtasks of the given task
        response = requests.get(f'{base_url}/tasks', headers=headers)
        response.raise_for_status()
        
        all_tasks = response.json()
        subtasks = [
            task for task in all_tasks 
            if task.get('parent_id') == task_id and not task.get('is_completed', False)
        ]
        
        return subtasks
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching subtasks for task {task_id}: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error fetching subtasks: {e}")
        return []


def get_task_details(task_id: str) -> Dict:
    """
    Gets comprehensive details for a specific task including comments and subtasks.
    
    Args:
        task_id (str): The ID of the task to get details for.
        
    Returns:
        Dict: Comprehensive task details including comments and subtasks.
    """
    try:
        headers = get_todoist_headers()
        base_url = os.getenv('TODOIST_API_BASE_URL', 'https://api.todoist.com/rest/v2')
        
        # Get the main task
        response = requests.get(f'{base_url}/tasks/{task_id}', headers=headers)
        response.raise_for_status()
        
        task = response.json()
        
        # Get comments and subtasks
        comments = get_task_comments(task_id)
        subtasks = get_task_subtasks(task_id)
        
        # Combine all information
        task_details = {
            'id': str(task.get('id')),
            'content': task.get('content', ''),
            'project_id': task.get('project_id'),
            'priority': task.get('priority', 1),
            'description': task.get('description', ''),
            'due': task.get('due', {}),
            'url': task.get('url', ''),
            'created': task.get('created', ''),
            'labels': task.get('labels', []),
            'comments': comments,
            'subtasks': subtasks,
            'comment_count': len(comments),
            'subtask_count': len(subtasks)
        }
        
        return task_details
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching details for task {task_id}: {e}")
        return {"error": f"API error: {e}"}
    except Exception as e:
        print(f"Unexpected error fetching task details: {e}")
        return {"error": f"Unexpected error: {e}"}


def add_task_comment(task_id: str, content: str) -> Dict:
    """
    Adds a comment to a specific task.
    
    Args:
        task_id (str): The ID of the task to add a comment to.
        content (str): The content of the comment.
        
    Returns:
        Dict: The created comment object.
    """
    try:
        headers = get_todoist_headers()
        base_url = os.getenv('TODOIST_API_BASE_URL', 'https://api.todoist.com/rest/v2')
        
        comment_data = {
            'task_id': task_id,
            'content': content
        }
        
        response = requests.post(f'{base_url}/comments', headers=headers, json=comment_data)
        response.raise_for_status()
        
        created_comment = response.json()
        return created_comment
        
    except requests.exceptions.RequestException as e:
        print(f"Error adding comment to task {task_id}: {e}")
        return {"error": f"API error: {e}"}
    except Exception as e:
        print(f"Unexpected error adding comment: {e}")
        return {"error": f"Unexpected error: {e}"}


def update_task(task_id: str, content: Optional[str] = None, priority: Optional[int] = None, description: Optional[str] = None, due_string: Optional[str] = None) -> Dict:
    """
    Updates a specific task with the provided changes.
    
    Args:
        task_id (str): The ID of the task to update.
        content (Optional[str]): New content/title for the task.
        priority (Optional[int]): New priority level (1=Normal, 2=Medium, 3=High, 4=Urgent).
        description (Optional[str]): New description for the task.
        due_string (Optional[str]): New due date as human-readable string (e.g., "tomorrow at 5pm").
        
    Returns:
        Dict: The updated task object.
    """
    try:
        headers = get_todoist_headers()
        base_url = os.getenv('TODOIST_API_BASE_URL', 'https://api.todoist.com/rest/v2')
        
        # Build updates dictionary with only provided parameters
        updates = {}
        if content is not None:
            updates['content'] = content
        if priority is not None:
            updates['priority'] = priority
        if description is not None:
            updates['description'] = description
        if due_string is not None:
            updates['due_string'] = due_string
        
        # Only proceed if there are actual updates
        if not updates:
            return {"error": "No updates provided"}
        
        response = requests.post(f'{base_url}/tasks/{task_id}', headers=headers, json=updates)
        response.raise_for_status()
        
        updated_task = response.json()
        return updated_task
        
    except requests.exceptions.RequestException as e:
        print(f"Error updating task {task_id}: {e}")
        return {"error": f"API error: {e}"}
    except Exception as e:
        print(f"Unexpected error updating task: {e}")
        return {"error": f"Unexpected error: {e}"}


def create_task(
    content: str, 
    project_name: Optional[str] = None, # Make project_name optional
    parent_id: Optional[str] = None,   # <-- ADD THIS NEW ARGUMENT
    due_string: Optional[str] = None, 
    priority: Optional[int] = None, 
    description: str = ""
) -> Dict:
    """
    Creates a new task in ToDoist. Can be a top-level task or a subtask.
    
    Args:
        content (str): The main title of the task.
        project_name (Optional[str]): The name of the project. If None, uses default 'Work'.
        parent_id (Optional[str]): The ID of the parent task to create this as a subtask.
        due_string (Optional[str]): A human-readable due date (e.g., "tomorrow at 5pm").
        priority (Optional[int]): The priority level (1-4).
        description (str): A detailed description for the task.
        
    Returns:
        Dict: A dictionary representing the newly created task.
    """
    try:
        headers = get_todoist_headers()
        base_url = os.getenv('TODOIST_API_BASE_URL', 'https://api.todoist.com/rest/v2')
        
        # Prepare task data
        task_data = {'content': content}
        
        # Add optional fields to the request body if they are provided
        if description:
            task_data['description'] = description
        if priority:
            task_data['priority'] = priority
        if due_string:
            task_data['due_string'] = due_string
        if parent_id:
            task_data['parent_id'] = parent_id # <-- INCLUDE parent_id IN THE API CALL
        else:
            # Only add project_id if it's not a subtask
            work_project_id = get_work_project_id()
            if not work_project_id:
                return {"error": "Work project not found and no parent_id provided"}
            task_data['project_id'] = work_project_id

        # Create the task
        response = requests.post(f'{base_url}/tasks', headers=headers, json=task_data)
        response.raise_for_status()
        
        created_task = response.json()
        
        return {
            "id": str(created_task.get('id')),
            "content": created_task.get('content', ''),
            "project_id": created_task.get('project_id'),
            "parent_id": created_task.get('parent_id'),
            "priority": created_task.get('priority'),
            "description": created_task.get('description', ''),
            "due": created_task.get('due', {}),
            "status": "created"
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Error creating task in ToDoist API: {e}")
        return {"error": f"API error: {e}"}
    except Exception as e:
        print(f"Unexpected error creating task: {e}")
        return {"error": f"Unexpected error: {e}"}
    
def get_last_activity_ts(task_id: str) -> str:
    """
    Gets the ISO 8601 timestamp of the last activity on a task.
    Activity is defined as the task's creation date or the date of the most recent comment.
    This helps determine how "stale" a task is.
    """
    try:
        headers = get_todoist_headers()
        base_url = os.getenv('TODOIST_API_BASE_URL', 'https://api.todoist.com/rest/v2')
        
        # 1. Call Todoist API to get task details, including created_at
        task_response = requests.get(f'{base_url}/tasks/{task_id}', headers=headers)
        task_response.raise_for_status()
        task = task_response.json()
        
        # Get task creation timestamp
        task_created_ts = task.get('created', '')
        
        # 2. Call Todoist API to get task comments
        comments_response = requests.get(f'{base_url}/comments?task_id={task_id}', headers=headers)
        comments_response.raise_for_status()
        comments = comments_response.json()
        
        # 3. Find the most recent comment timestamp
        latest_comment_ts = ''
        if comments:
            # Sort comments by created timestamp (newest first)
            sorted_comments = sorted(comments, key=lambda x: x.get('created', ''), reverse=True)
            latest_comment_ts = sorted_comments[0].get('created', '')
        
        # 4. Compare task.created_at with the latest comment timestamp
        # 5. Return the most recent of the two as an ISO 8601 string
        if latest_comment_ts and task_created_ts:
            # Compare timestamps and return the most recent
            if latest_comment_ts > task_created_ts:
                return latest_comment_ts
            else:
                return task_created_ts
        elif latest_comment_ts:
            return latest_comment_ts
        elif task_created_ts:
            return task_created_ts
        else:
            # Fallback to current timestamp if no timestamps found
            return datetime.now(timezone.utc).isoformat()
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching last activity timestamp for task {task_id}: {e}")
        # Return current timestamp as fallback
        return datetime.now(timezone.utc).isoformat()
    except Exception as e:
        print(f"Unexpected error getting last activity timestamp: {e}")
        # Return current timestamp as fallback
        return datetime.now(timezone.utc).isoformat()