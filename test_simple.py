#!/usr/bin/env python3
"""
Simple test script to verify the basic ToDoist tools and agent setup.
"""

from tools.todoist_tools import get_open_tasks, create_task
from agents.agents import prioritization, project_manager


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


def test_agents():
    """Test the agents that use ToDoist tools."""
    print("\nTesting Agents with ToDoist Tools...")

    # Test PrioritizationAgent
    print(f"\nPrioritizationAgent:")
    print(f"  Name: {prioritization.name}")
    print(f"  Description: {prioritization.description}")
    print(f"  Number of tools: {len(prioritization.tools)}")
    for i, tool in enumerate(prioritization.tools):
        print(f"    Tool {i+1}: {tool.__name__}")

    # Test ProjectManagerAgent
    print(f"\nProjectManagerAgent:")
    print(f"  Name: {project_manager.name}")
    print(f"  Description: {project_manager.description}")
    print(f"  Number of tools: {len(project_manager.tools)}")
    for i, tool in enumerate(project_manager.tools):
        print(f"    Tool {i+1}: {tool.__name__}")


if __name__ == "__main__":
    print("=== ToDoist Multi-Agent System - Simple Test ===\n")

    try:
        test_tools()
        test_agents()
        print("\n✅ All tests passed! Basic setup is working.")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
