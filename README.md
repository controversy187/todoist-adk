# ToDoist Multi Agent Manager

This project leverages ToDoist to manage a user's workload. Using a mutli-agent architecture and tools, agents provide recommendations for top priority items. It also helps break projects down into reasonable tasks with timelines.

## System Architecture Overview
This architecture employs a hierarchical, multi-agent system designed for clear separation of concerns. It consists of a primary Coordinator Agent that routes tasks to specialized Reasoning Agents. These Reasoning Agents, in turn, delegate all interactions with the ToDoist API to a dedicated ToDoist Tool Agent. This modular design allows for easily adding new tool agents (e.g., for email or calendar) in the future without modifying the existing reasoning logic.

## Agent Definitions
### Coordinator Agent
Name: TeamCoordinator

Role: The primary entry point for all user requests. Its sole responsibility is to analyze the user's high-level goal and delegate it to the appropriate Reasoning Agent.
Sub-Agents: PrioritizationAgent, ProjectManagerAgent.
Instructions:
If the user asks for their priorities or wants to know what to work on, delegate to the PrioritizationAgent.
If the user wants to plan a project, break down a goal, or create multiple tasks, delegate to the ProjectManagerAgent.
It should not attempt to answer questions or use tools directly.

### Reasoning Agents
These agents are responsible for thought and planning. They break down a high-level goal into a series of steps but delegate the actual execution of those steps to the ToDoistToolAgent.

#### Prioritization Agent
Name: PrioritizationAgent
Role: Analyzes user tasks to determine priorities.
Sub-Agents: ToDoistToolAgent.
Instructions:
Your goal is to provide the user with their top 3-5 priorities.
To do this, you must first get the list of open tasks. Delegate this task to the ToDoistToolAgent.
Once you receive the list of tasks from the tool agent, analyze it based on due dates and priority flags.
Formulate a final, user-facing summary of the recommended priorities.

#### Project Manager Agent
Name: ProjectManagerAgent
Role: Breaks down complex goals into actionable tasks.
Sub-Agents: ToDoistToolAgent.
Instructions:
Your purpose is to take a complex user goal (e.g., "Plan my product launch") and break it down into a list of specific, actionable tasks.
For each task you devise, delegate its creation to the ToDoistToolAgent, providing a clear title, description, and a reasonable due date.
After delegating the creation of all tasks, confirm with the user that the project plan has been created in ToDoist.

## Tool-Using Agent
This agent is a specialized worker that only knows how to use a specific set of tools. It doesn't perform complex reasoning; it simply executes requests from other agents.

Name: ToDoistToolAgent
Role: The only agent that directly interacts with the ToDoist API tools.
Tools: get_open_tasks, create_task.
Instructions:
You are an assistant that operates tools for ToDoist.
When another agent asks you to get tasks or create a task, use the appropriate tool with the arguments they provide.
Return the result of the tool call directly to the requesting agent.

## Tool Definitions (todoist_tools.py)
These are the Python functions that grant the ToDoistToolAgent its abilities.

get_open_tasks(project_name: str)
Description: Fetches all open tasks, including their subtasks, comments, due dates, and priority, from a specified ToDoist project.
Arguments:
project_name (str): The exact name of the project to fetch tasks from.
Returns: A list of task objects with all their details.

create_task(project_name: str, content: str, due_string: str, priority: int, description: str = "")
Description: Creates a new task in a specified ToDoist project.
Arguments:
project_name (str): The name of the project to add the task to.
content (str): The main title of the task.
due_string (str): A human-readable due date (e.g., "tomorrow at 5pm").
priority (int): The priority level (1=Normal, 2=Medium, 3=High, 4=Urgent).
description (str): A detailed description or notes for the task.
Returns: A dictionary representing the newly created task.