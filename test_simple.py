#!/usr/bin/env python3
"""
Simple test script to verify the basic ToDoist tools and agent setup.
"""

from tools.todoist_tools import get_open_tasks, create_task
from agents.todoist_tool_agent import todoist_tool_agent


def test_tools():
    """Test the basic tool functions."""
    print("Testing ToDoist tools...")
    
    # Test get_open_tasks
    tasks = get_open_tasks("Test Project")
    print(f"Retrieved {len(tasks)} tasks:")
    for task in tasks:
        print(f"  - {task['content']} (Priority: {task['priority']})")
    
    # Test create_task
    new_task = create_task(
        project_name="Test Project",
        content="New test task",
        due_string="tomorrow at 5pm",
        priority=3,
        description="This is a test task created by our tools"
    )
    print(f"\nCreated new task: {new_task['content']}")
    print(f"Task details: {new_task}")


def test_agent():
    """Test the ToDoistToolAgent."""
    print("\nTesting ToDoistToolAgent...")
    print(f"Agent name: {todoist_tool_agent.name}")
    print(f"Agent description: {todoist_tool_agent.description}")
    print(f"Number of tools: {len(todoist_tool_agent.tools)}")
    
    for i, tool in enumerate(todoist_tool_agent.tools):
        print(f"  Tool {i+1}: {tool.__name__}")


if __name__ == "__main__":
    print("=== ToDoist Multi-Agent System - Simple Test ===\n")
    
    try:
        test_tools()
        test_agent()
        print("\n✅ All tests passed! Basic setup is working.")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 