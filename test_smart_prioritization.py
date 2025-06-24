#!/usr/bin/env python3
"""
Test script for the SmartPrioritizationAgent functionality.
"""

import os
from dotenv import load_dotenv
from tools.todoist_tools import (
    get_open_tasks, 
    get_task_details, 
    add_task_comment, 
    update_task, 
    create_task
)

# Load environment variables
load_dotenv()

def test_basic_functionality():
    """Test basic functionality of the new tools."""
    print("Testing Smart Prioritization Tools...")
    
    # Test getting open tasks
    print("\n1. Testing get_open_tasks...")
    tasks = get_open_tasks()
    print(f"Found {len(tasks)} open tasks")
    
    if tasks:
        # Test getting task details for the first task
        first_task = tasks[0]
        task_id = first_task['id']
        print(f"\n2. Testing get_task_details for task {task_id}...")
        details = get_task_details(task_id)
        print(f"Task details: {details.get('content', 'N/A')}")
        print(f"Comments: {details.get('comment_count', 0)}")
        print(f"Subtasks: {details.get('subtask_count', 0)}")
        
        # Test adding a comment
        print(f"\n3. Testing add_task_comment...")
        comment_result = add_task_comment(task_id, "Test comment from smart prioritization system")
        if 'error' not in comment_result:
            print("✓ Comment added successfully")
        else:
            print(f"✗ Error adding comment: {comment_result['error']}")
        
        # Test updating task priority
        print(f"\n4. Testing update_task...")
        current_priority = first_task.get('priority', 1)
        new_priority = 3 if current_priority < 3 else 1
        update_result = update_task(task_id, {'priority': new_priority})
        if 'error' not in update_result:
            print(f"✓ Task priority updated from {current_priority} to {new_priority}")
        else:
            print(f"✗ Error updating task: {update_result['error']}")
    
    # Test creating a new task
    print(f"\n5. Testing create_task...")
    new_task_result = create_task(
        project_name="Work",
        content="Test task for smart prioritization",
        due_string="tomorrow",
        priority=2,
        description="This is a test task created by the smart prioritization system"
    )
    if 'error' not in new_task_result:
        print("✓ Test task created successfully")
        print(f"  Task ID: {new_task_result.get('id')}")
        print(f"  Content: {new_task_result.get('content')}")
    else:
        print(f"✗ Error creating task: {new_task_result['error']}")

def test_agent_import():
    """Test that the new agent can be imported correctly."""
    print("\nTesting SmartPrioritizationAgent import...")
    try:
        from agents.smart_prioritization_agent import smart_prioritization_agent
        print("✓ SmartPrioritizationAgent imported successfully")
        print(f"  Agent name: {smart_prioritization_agent.name}")
        print(f"  Available tools: {len(smart_prioritization_agent.tools)}")
    except ImportError as e:
        print(f"✗ Error importing SmartPrioritizationAgent: {e}")

def test_coordinator_update():
    """Test that the coordinator includes the new agent."""
    print("\nTesting Coordinator Agent update...")
    try:
        from agents.coordinator_agent import coordinator_agent
        print("✓ Coordinator agent imported successfully")
        print(f"  Sub-agents: {len(coordinator_agent.sub_agents)}")
        agent_names = [agent.name for agent in coordinator_agent.sub_agents]
        print(f"  Agent names: {agent_names}")
        
        if "SmartPrioritizationAgent" in agent_names:
            print("✓ SmartPrioritizationAgent is included in coordinator")
        else:
            print("✗ SmartPrioritizationAgent is NOT included in coordinator")
            
    except ImportError as e:
        print(f"✗ Error importing coordinator agent: {e}")

if __name__ == "__main__":
    print("=== Smart Prioritization System Test ===\n")
    
    # Check if API token is available
    api_token = os.getenv('TODOIST_API_TOKEN')
    if not api_token:
        print("⚠️  TODOIST_API_TOKEN not found in environment variables")
        print("   Some tests may fail or use fallback data")
    else:
        print("✓ TODOIST_API_TOKEN found")
    
    # Run tests
    test_basic_functionality()
    test_agent_import()
    test_coordinator_update()
    
    print("\n=== Test Complete ===")
    print("\nTo use the smart prioritization system:")
    print("1. Start the ADK web interface: adk web")
    print("2. Ask: 'Groom my backlog' or 'Analyze my tasks'")
    print("3. The system will guide you through an interactive session") 