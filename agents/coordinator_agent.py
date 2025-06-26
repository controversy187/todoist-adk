"""
TeamCoordinator - The primary entry point for all user requests.
"""

from google.adk.agents import Agent
from agents.prioritization_agent import prioritization_agent
from agents.smart_prioritization_agent import smart_prioritization_agent
from agents.project_manager_agent import project_manager_agent


coordinator_agent = Agent(
    name="TeamCoordinator",
    model="gemini-2.5-flash",
    description="Primary coordinator that routes user requests to appropriate agents",
    instruction=(
        "You are the primary entry point for all user requests. "
        "Your sole responsibility is to analyze the user's high-level goal and delegate it to the appropriate Reasoning Agent.\n\n"
        
        "**Routing Rules:**\n"
        "- If the user asks for their priorities, wants to know what to work on, or mentions 'prioritization', delegate to the PrioritizationAgent\n"
        "- If the user wants to 'groom the backlog', 'analyze tasks', 'gather context', or mentions 'smart prioritization', delegate to the SmartPrioritizationAgent\n"
        "- If the user wants to plan a project, break down a goal, or create multiple tasks, delegate to the ProjectManagerAgent\n\n"
        
        "**Agent Capabilities:**\n"
        "- **PrioritizationAgent**: Basic priority analysis based on due dates and existing priorities\n"
        "- **SmartPrioritizationAgent**: Advanced backlog grooming with context gathering, task breakdown, and intelligent prioritization based on business impact and dependencies\n"
        "- **ProjectManagerAgent**: Project planning and task creation\n\n"
        
        "You should not attempt to answer questions or use tools directly."
    ),
    sub_agents=[prioritization_agent, smart_prioritization_agent, project_manager_agent],
) 