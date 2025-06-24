"""
TeamCoordinator - The primary entry point for all user requests.
"""

from google.adk.agents import Agent
from agents.prioritization_agent import prioritization_agent
from agents.project_manager_agent import project_manager_agent


coordinator_agent = Agent(
    name="TeamCoordinator",
    model="gemini-2.0-flash",
    description="Primary coordinator that routes user requests to appropriate agents",
    instruction=(
        "You are the primary entry point for all user requests. "
        "Your sole responsibility is to analyze the user's high-level goal and delegate it to the appropriate Reasoning Agent. "
        "If the user asks for their priorities or wants to know what to work on, delegate to the PrioritizationAgent. "
        "If the user wants to plan a project, break down a goal, or create multiple tasks, delegate to the ProjectManagerAgent. "
        "You should not attempt to answer questions or use tools directly."
    ),
    sub_agents=[prioritization_agent, project_manager_agent],
) 