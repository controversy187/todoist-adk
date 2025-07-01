"""
ToDoist API tools for task management.
These are the core functions that the ToDoistToolAgent will use.
"""

import os
import time
from typing import List, Dict, Optional
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv
from functools import lru_cache, wraps

# Load environment variables
load_dotenv()

# Default project name
DEFAULT_PROJECT = "Work"


def retry_on_request_exception(func):
    """A decorator to retry a function on RequestException."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        retries = 3
        delay = 1
        for i in range(retries):
            try:
                return func(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2
        return {"error": "API request failed after multiple retries."}

    return wrapper


def get_todoist_headers():
    """Get headers for ToDoist API requests."""
    api_token = os.getenv("TODOIST_API_TOKEN")
    if not api_token:
        raise ValueError("TODOIST_API_TOKEN not found in environment variables")

    return {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}


@lru_cache(maxsize=1)
@retry_on_request_exception
def get_project_by_name(project_name: str) -> Optional[Dict]:
    """Get a project by its name."""
    headers = get_todoist_headers()
    base_url = os.getenv("TODOIST_API_BASE_URL", "https://api.todoist.com/rest/v2")

    # Get all projects
    response = requests.get(f"{base_url}/projects", headers=headers)
    response.raise_for_status()
    projects = response.json()

    # Find the project
    for project in projects:
        if project.get("name", "").lower() == project_name.lower():
            return project

    # If project not found, return None
    return None


@lru_cache(maxsize=1)
def get_work_project_id():
    """Get the project ID for the 'Work' project."""
    work_project = get_project_by_name(DEFAULT_PROJECT)
    if work_project:
        return work_project["id"]
    return None


@retry_on_request_exception
def create_project(project_name: str) -> Dict:
    """Creates a new project."""
    headers = get_todoist_headers()
    base_url = os.getenv("TODOIST_API_BASE_URL", "https://api.todoist.com/rest/v2")

    project_data = {"name": project_name}

    response = requests.post(f"{base_url}/projects", headers=headers, json=project_data)
    response.raise_for_status()

    created_project = response.json()
    return created_project


@retry_on_request_exception
def delete_project(project_id: str) -> bool:
    """Deletes a project."""
    headers = get_todoist_headers()
    base_url = os.getenv("TODOIST_API_BASE_URL", "https://api.todoist.com/rest/v2")

    response = requests.delete(f"{base_url}/projects/{project_id}", headers=headers)
    response.raise_for_status()

    return True


@retry_on_request_exception
def move_task_to_project(task_id: str, project_id: str) -> Dict:
    """Moves a task to a different project."""
    headers = get_todoist_headers()
    base_url = os.getenv("TODOIST_API_BASE_URL", "https://api.todoist.com/rest/v2")

    task_data = {"project_id": project_id}

    response = requests.post(
        f"{base_url}/tasks/{task_id}", headers=headers, json=task_data
    )
    response.raise_for_status()

    updated_task = response.json()
    return updated_task


@retry_on_request_exception
def get_open_tasks(project_name: Optional[str] = None) -> List[Dict]:
    """
    Fetches all open tasks from the Work project in ToDoist.

    Args:
        project_name (Optional[str]): The name of the project to fetch tasks from. If None, uses default 'Work'.

    Returns:
        List[Dict]: A list of task objects with their details.
    """
    headers = get_todoist_headers()
    base_url = os.getenv("TODOIST_API_BASE_URL", "https://api.todoist.com/rest/v2")

    project_to_use = project_name if project_name else DEFAULT_PROJECT
    project = get_project_by_name(project_to_use)
    if not project:
        print(
            f"Project '{project_to_use}' not found. Please create a project named '{project_to_use}' in ToDoist."
        )
        return []

    # Get all tasks from the specified project
    response = requests.get(
        f"{base_url}/tasks?project_id={project['id']}", headers=headers
    )
    response.raise_for_status()

    tasks = response.json()

    # Format the response to match our expected structure
    formatted_tasks = []
    for task in tasks:
        formatted_task = {
            "id": str(task.get("id")),
            "content": task.get("content", ""),
            "project_id": task.get("project_id"),
            "priority": task.get("priority", 1),
            "description": task.get("description", ""),
            "due": task.get("due", {}),
            "url": task.get("url", ""),
            "created": task.get("created", ""),
            "labels": task.get("labels", []),
        }
        formatted_tasks.append(formatted_task)

    return formatted_tasks


@retry_on_request_exception
def get_task_comments(task_id: str) -> List[Dict]:
    """
    Fetches all comments for a specific task.

    Args:
        task_id (str): The ID of the task to get comments for.

    Returns:
        List[Dict]: A list of comment objects.
    """
    headers = get_todoist_headers()
    base_url = os.getenv("TODOIST_API_BASE_URL", "https://api.todoist.com/rest/v2")

    response = requests.get(f"{base_url}/comments?task_id={task_id}", headers=headers)
    response.raise_for_status()

    comments = response.json()
    return comments


@retry_on_request_exception
def get_task_subtasks(task_id: str) -> List[Dict]:
    """
    Fetches all subtasks for a specific task.

    Args:
        task_id (str): The ID of the task to get subtasks for.

    Returns:
        List[Dict]: A list of subtask objects.
    """
    headers = get_todoist_headers()
    base_url = os.getenv("TODOIST_API_BASE_URL", "https://api.todoist.com/rest/v2")

    # Get all tasks and filter for subtasks of the given task
    response = requests.get(f"{base_url}/tasks?task_id={task_id}", headers=headers)
    response.raise_for_status()

    all_tasks = response.json()
    subtasks = [
        task
        for task in all_tasks
        if task.get("parent_id") == task_id
        and not task.get("is_completed", False)
    ]

    return subtasks


@retry_on_request_exception
def get_task_details(task_id: str) -> Dict:
    """
    Gets comprehensive details for a specific task including comments and subtasks.

    Args:
        task_id (str): The ID of the task to get details for.

    Returns:
        Dict: Comprehensive task details including comments and subtasks.
    """
    headers = get_todoist_headers()
    base_url = os.getenv("TODOIST_API_BASE_URL", "https://api.todoist.com/rest/v2")

    # Get the main task
    response = requests.get(f"{base_url}/tasks/{task_id}", headers=headers)
    response.raise_for_status()

    task = response.json()

    # Get comments and subtasks
    comments = get_task_comments(task_id)
    subtasks = get_task_subtasks(task_id)

    # Combine all information
    task_details = {
        "id": str(task.get("id")),
        "content": task.get("content", ""),
        "project_id": task.get("project_id"),
        "priority": task.get("priority", 1),
        "description": task.get("description", ""),
        "due": task.get("due", {}),
        "url": task.get("url", ""),
        "created": task.get("created", ""),
        "labels": task.get("labels", []),
        "comments": comments,
        "subtasks": subtasks,
        "comment_count": len(comments),
        "subtask_count": len(subtasks),
    }

    return task_details


@retry_on_request_exception
def add_task_comment(task_id: str, content: str) -> Dict:
    """
    Adds a comment to a specific task.

    Args:
        task_id (str): The ID of the task to add a comment to.
        content (str): The content of the comment.

    Returns:
        Dict: The created comment object.
    """
    headers = get_todoist_headers()
    base_url = os.getenv("TODOIST_API_BASE_URL", "https://api.todoist.com/rest/v2")

    comment_data = {"task_id": task_id, "content": content}

    response = requests.post(
        f"{base_url}/comments", headers=headers, json=comment_data
    )
    response.raise_for_status()

    created_comment = response.json()
    return created_comment


@retry_on_request_exception
def update_task(
    task_id: str,
    content: Optional[str] = None,
    priority: Optional[int] = None,
    description: Optional[str] = None,
    due_string: Optional[str] = None,
) -> Dict:
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
    headers = get_todoist_headers()
    base_url = os.getenv("TODOIST_API_BASE_URL", "https://api.todoist.com/rest/v2")

    # Build updates dictionary with only provided parameters
    updates = {}
    if content is not None:
        updates["content"] = content
    if priority is not None:
        updates["priority"] = priority
    if description is not None:
        updates["description"] = description
    if due_string is not None:
        updates["due_string"] = due_string

    # Only proceed if there are actual updates
    if not updates:
        return {"error": "No updates provided"}

    response = requests.post(
        f"{base_url}/tasks/{task_id}", headers=headers, json=updates
    )
    response.raise_for_status()

    updated_task = response.json()
    return updated_task


@retry_on_request_exception
def create_task(
    content: str,
    project_name: Optional[str] = None,  # Make project_name optional
    parent_id: Optional[str] = None,  # <-- ADD THIS NEW ARGUMENT
    due_string: Optional[str] = None,
    priority: Optional[int] = None,
    description: str = "",
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
    headers = get_todoist_headers()
    base_url = os.getenv("TODOIST_API_BASE_URL", "https://api.todoist.com/rest/v2")

    # Prepare task data
    task_data = {"content": content}

    # Add optional fields to the request body if they are provided
    if description:
        task_data["description"] = description
    if priority:
        task_data["priority"] = priority
    if due_string:
        task_data["due_string"] = due_string
    if parent_id:
        task_data["parent_id"] = parent_id  # <-- INCLUDE parent_id IN THE API CALL
    else:
        # Only add project_id if it's not a subtask
        work_project_id = get_work_project_id()
        if not work_project_id:
            return {"error": "Work project not found and no parent_id provided"}
        task_data["project_id"] = work_project_id

    # Create the task
    response = requests.post(f"{base_url}/tasks", headers=headers, json=task_data)
    response.raise_for_status()

    created_task = response.json()

    return {
        "id": str(created_task.get("id")),
        "content": created_task.get("content", ""),
        "project_id": created_task.get("project_id"),
        "parent_id": created_task.get("parent_id"),
        "priority": created_task.get("priority"),
        "description": created_task.get("description", ""),
        "due": created_task.get("due", {}),
        "status": "created",
    }


@retry_on_request_exception
def get_last_activity_ts(task_id: str) -> str:
    """
    Gets the ISO 8601 timestamp of the last activity on a task.
    Activity is defined as the task's creation date or the date of the most recent comment.
    This helps determine how "stale" a task is.
    """
    headers = get_todoist_headers()
    base_url = os.getenv("TODOIST_API_BASE_URL", "https://api.todoist.com/rest/v2")

    # 1. Call Todoist API to get task details, including created_at
    task_response = requests.get(f"{base_url}/tasks/{task_id}", headers=headers)
    task_response.raise_for_status()
    task = task_response.json()

    # Get task creation timestamp
    task_created_ts = task.get("created", "")

    # 2. Call Todoist API to get task comments
    comments_response = requests.get(
        f"{base_url}/comments?task_id={task_id}", headers=headers
    )
    comments_response.raise_for_status()
    comments = comments_response.json()

    # 3. Find the most recent comment timestamp
    latest_comment_ts = ""
    if comments:
        # Sort comments by created timestamp (newest first)
        sorted_comments = sorted(
            comments, key=lambda x: x.get("created", ""), reverse=True
        )
        latest_comment_ts = sorted_comments[0].get("created", "")

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
