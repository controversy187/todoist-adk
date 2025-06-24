# ToDoist Multi Agent Manager

This project leverages ToDoist to manage a user's workload using Google's Agent Development Kit (ADK) with a multi-agent architecture. The system provides recommendations for top priority items and helps break projects down into reasonable tasks with timelines, all within a dedicated "Work" project in ToDoist.

## System Architecture Overview
This architecture employs a hierarchical, multi-agent system designed for clear separation of concerns. It consists of a primary Coordinator Agent that routes tasks to specialized Reasoning Agents. These Reasoning Agents have direct access to ToDoist API tools, eliminating the need for separate tool agents. This modular design allows for easily adding new tools (e.g., for email or calendar) in the future without modifying the existing reasoning logic.

## Agent Definitions

### Coordinator Agent
**Name:** TeamCoordinator

**Role:** The primary entry point for all user requests. Its sole responsibility is to analyze the user's high-level goal and delegate it to the appropriate Reasoning Agent.

**Sub-Agents:** PrioritizationAgent, ProjectManagerAgent

**Instructions:**
- If the user asks for their priorities or wants to know what to work on, delegate to the PrioritizationAgent
- If the user wants to plan a project, break down a goal, or create multiple tasks, delegate to the ProjectManagerAgent
- It should not attempt to answer questions or use tools directly

### Reasoning Agents
These agents are responsible for thought and planning. They break down a high-level goal into a series of steps and execute those steps using ToDoist API tools directly.

#### Prioritization Agent
**Name:** PrioritizationAgent

**Role:** Analyzes user tasks to determine priorities.

**Tools:** get_open_tasks, create_task

**Instructions:**
- Your goal is to provide the user with their top 3-5 priorities
- To do this, you must first get the list of open tasks from the Work project using the get_open_tasks tool
- Once you receive the list of tasks, analyze it based on due dates and priority flags
- Formulate a final, user-facing summary of the recommended priorities

#### Project Manager Agent
**Name:** ProjectManagerAgent

**Role:** Breaks down complex goals into actionable tasks.

**Tools:** get_open_tasks, create_task

**Instructions:**
- Your purpose is to take a complex user goal (e.g., "Plan my product launch") and break it down into a list of specific, actionable tasks
- For each task you devise, use the create_task tool to create it in the Work project, providing a clear title, description, and a reasonable due date
- All tasks will be created in the Work project
- After creating all tasks, confirm with the user that the project plan has been created in ToDoist

## Tool Definitions (tools/todoist_tools.py)
These are the Python functions that grant the agents their ToDoist abilities.

### get_open_tasks(project_name: Optional[str] = None)
**Description:** Fetches all open tasks from the "Work" project in ToDoist.

**Arguments:**
- project_name (Optional[str]): Ignored - always uses "Work" project

**Returns:** A list of task objects with all their details (id, content, priority, due date, description, etc.)

### create_task(project_name: str, content: str, due_string: str, priority: int, description: str = "")
**Description:** Creates a new task in the "Work" project in ToDoist.

**Arguments:**
- project_name (str): Ignored - always uses "Work" project
- content (str): The main title of the task
- due_string (str): A human-readable due date (e.g., "tomorrow at 5pm")
- priority (int): The priority level (1=Normal, 2=Medium, 3=High, 4=Urgent)
- description (str): A detailed description or notes for the task

**Returns:** A dictionary representing the newly created task

## Project Structure
```
TaskAgent/
├── README.md
├── .env (your actual config)
├── .env_sample
├── .gitignore
├── requirements.txt
├── agents/
│   ├── __init__.py
│   ├── coordinator_agent.py
│   ├── prioritization_agent.py
│   └── project_manager_agent.py
├── tools/
│   ├── __init__.py
│   └── todoist_tools.py
├── test_simple.py
├── test_agents.py
└── test_api.py
```

## Setup Instructions

### 1. Environment Setup
1. Clone this repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`

### 2. ToDoist Configuration
1. Get your ToDoist API token from https://app.todoist.com/app/settings/integrations/developer
2. Create a project named "Work" in your ToDoist account
3. Copy `.env_sample` to `.env` and add your API token:
   ```
   TODOIST_API_TOKEN=your_actual_todoist_api_token_here
   ```

### 3. Google ADK Configuration
1. Get your Google API key
2. Add it to your `.env` file:
   ```
   GOOGLE_API_KEY=your_actual_google_api_key_here
   ```

## Usage

### Testing
Run the test scripts to verify everything is working:
```bash
python test_api.py          # Test ToDoist API integration
python test_agents.py       # Test agent hierarchy
```

### Web Interface
Start the ADK web interface:
```bash
adk web
```

This will open a web browser where you can interact with your multi-agent system.

### Example Interactions
- **"What are my priorities today?"** - Gets your top 3-5 tasks from the Work project
- **"Plan a product launch"** - Breaks down the goal into actionable tasks in your Work project
- **"What should I work on?"** - Analyzes your tasks and provides recommendations

## Key Features
- **Work Project Focus:** All tasks are managed within a dedicated "Work" project in ToDoist
- **Real-time Integration:** Direct API calls to ToDoist for live task data
- **Intelligent Prioritization:** AI-powered analysis of due dates and priorities
- **Project Planning:** Automatic breakdown of complex goals into actionable tasks
- **Web Interface:** Easy-to-use chat interface powered by Google ADK

## Error Handling
The system includes robust error handling:
- API connection failures fall back to mock data for testing
- Clear error messages for missing configuration
- Graceful handling of missing "Work" project

## Future Enhancements
- Add support for multiple projects
- Integrate with calendar systems
- Add email integration for task notifications
- Support for task dependencies and subtasks