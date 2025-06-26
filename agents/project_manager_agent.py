"""
ProjectManagerAgent - Breaks down complex goals into actionable tasks.
"""

from google.adk.agents import Agent
from tools.todoist_tools import get_open_tasks, create_task


project_manager_agent = Agent(
    name="ProjectManagerAgent",
    model="gemini-2.5-pro",
    description="Agent that breaks down complex goals into actionable tasks",
    instruction=(
        "Your purpose is to take a complex user goal (e.g., 'Plan my product launch') "
        "and break it down into a list of specific, actionable tasks. "
        "For each task you devise, use the create_task tool to create it in the Work project, "
        "providing a clear title, description, and a reasonable due date. "
        "All tasks will be created in the Work project. "
        "After creating all tasks, confirm with the user that "
        "the project plan has been created in ToDoist."
    ),
    tools=[get_open_tasks, create_task],
) 