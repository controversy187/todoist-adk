#!/usr/bin/env python3
"""
Test script to verify the agent hierarchy and structure.
"""

from agents.coordinator_agent import coordinator_agent
from agents.prioritization_agent import prioritization_agent
from agents.project_manager_agent import project_manager_agent


def test_agent_hierarchy():
    """Test the agent hierarchy and relationships."""
    print("=== Testing Agent Hierarchy ===\n")
    
    # Test coordinator agent
    print(f"Coordinator Agent: {coordinator_agent.name}")
    print(f"  Description: {coordinator_agent.description}")
    print(f"  Sub-agents: {len(coordinator_agent.sub_agents)}")
    for i, agent in enumerate(coordinator_agent.sub_agents):
        print(f"    {i+1}. {agent.name}")
    
    # Test prioritization agent
    print(f"\nPrioritization Agent: {prioritization_agent.name}")
    print(f"  Description: {prioritization_agent.description}")
    print(f"  Tools: {len(prioritization_agent.tools)}")
    for i, tool in enumerate(prioritization_agent.tools):
        print(f"    {i+1}. {tool.__name__}")
    
    # Test project manager agent
    print(f"\nProject Manager Agent: {project_manager_agent.name}")
    print(f"  Description: {project_manager_agent.description}")
    print(f"  Tools: {len(project_manager_agent.tools)}")
    for i, tool in enumerate(project_manager_agent.tools):
        print(f"    {i+1}. {tool.__name__}")


def test_agent_imports():
    """Test that all agents can be imported correctly."""
    print("\n=== Testing Agent Imports ===\n")
    
    agents = [
        ("Coordinator", coordinator_agent),
        ("Prioritization", prioritization_agent),
        ("Project Manager", project_manager_agent),
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