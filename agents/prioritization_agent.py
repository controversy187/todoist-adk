"""
PrioritizationAgent - Analyzes user tasks to determine priorities.
"""

from google.adk.agents import Agent
from tools.todoist_tools import get_open_tasks, create_task


prioritization_agent = Agent(
    name="PrioritizationAgent",
    model="gemini-2.5-flash",
    description="Agent that analyzes tasks and determines user priorities",
    instruction=(
        "Your goal is to provide the user with their top 3-5 priorities. "
        "To do this, you must first get the list of open tasks from the Work project. "
        "Use the get_open_tasks tool to retrieve tasks. "
        "Once you receive the list of tasks, analyze it based on due dates and priority flags. "
        "Formulate a final, user-facing summary of the recommended priorities."
    ),
    tools=[get_open_tasks, create_task],
) 