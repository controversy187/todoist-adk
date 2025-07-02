#!/usr/bin/env python3
"""
Test script to verify the agent hierarchy and structure.
"""

from agents.agents import (
    coordinator,
    prioritization,
    project_manager,
    morning_briefing,
    google_calendar,
)


def test_agent_hierarchy():
    """Test the agent hierarchy and relationships."""
    print("=== Testing Agent Hierarchy ===\n")

    # Test coordinator agent
    print(f"Coordinator Agent: {coordinator.name}")
    print(f"  Description: {coordinator.description}")
    print(f"  Sub-agents: {len(coordinator.sub_agents)}")
    for i, agent in enumerate(coordinator.sub_agents):
        print(f"    {i+1}. {agent.name}")

    # Test prioritization agent
    print(f"\nPrioritization Agent: {prioritization.name}")
    print(f"  Description: {prioritization.description}")
    print(f"  Tools: {len(prioritization.tools)}")
    for i, tool in enumerate(prioritization.tools):
        print(f"    {i+1}. {tool.__name__}")

    # Test project manager agent
    print(f"\nProject Manager Agent: {project_manager.name}")
    print(f"  Description: {project_manager.description}")
    print(f"  Tools: {len(project_manager.tools)}")
    for i, tool in enumerate(project_manager.tools):
        print(f"    {i+1}. {tool.__name__}")


def test_agent_imports():
    """Test that all agents can be imported correctly."""
    print("\n=== Testing Agent Imports ===\n")

    agents = [
        ("Coordinator", coordinator),
        ("Prioritization", prioritization),
        ("Project Manager", project_manager),
        ("Morning Briefing", morning_briefing),
        ("Google Calendar", google_calendar),
    ]

    for name, agent in agents:
        try:
            print(f"✅ {name} Agent imported successfully")
            print(f"   Name: {agent.name}")
            print(f"   Model: {agent.model}")
        except Exception as e:
            print(f"❌ {name} Agent import failed: {e}")


if __name__ == "__main__":
    print("=== ToDoist Multi-Agent System - Agent Hierarchy Test ===\n")

    try:
        test_agent_hierarchy()
        test_agent_imports()
        print("\n✅ All agent tests passed! Hierarchy is working correctly.")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
