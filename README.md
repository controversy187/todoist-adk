# Task Agent

This project implements a multi-agent system for task management and prioritization, integrating with Todoist and Google Calendar. The system is designed to help users manage their tasks, prioritize their work, and stay organized.

## Features

- **Multi-Agent System**: The project uses a coordinator agent to route user requests to the appropriate specialized agent.
- **Todoist Integration**: The agents can interact with the Todoist API to manage tasks, projects, and comments.
- **Google Calendar Integration**: The agents can manage Google Calendar events.
- **Smart Prioritization**: The `SmartPrioritizationAgent` uses a RIN (Recency, Impact, Next-Action Effort) framework to help users prioritize their tasks.
- **Morning Briefing**: The `MorningBriefingAgent` provides a summary of the day's priorities.
- **Project Planning**: The `ProjectManagerAgent` can break down complex goals into actionable tasks.

## Getting Started

### Prerequisites

- Python 3.x
- Pip
- Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd TaskAgent
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up your credentials:**
    -   **Todoist:**
        1.  Get your API token from the [Todoist developer settings](https://todoist.com/app/settings/integrations/developer).
        2.  Create a `.env` file in the root of the project and add the following line:
            ```
            TODOIST_API_TOKEN=<your-todoist-api-token>
            ```
    -   **Google Calendar:**
        1.  Follow the instructions [here](https://developers.google.com/workspace/guides/create-credentials) to create your `credentials.json` file.
        2.  Place the `credentials.json` file in the root of the project.
        3.  The first time you run the application, you will be prompted to authorize access to your Google Calendar.

## Usage

You can interact with the agents using the `adk` command-line tool. The main entry point for the agent is `main.py`, which uses the `CoordinatorAgent` to route your requests.

### Examples

-   **Get your morning briefing:**
    ```bash
    adk web "morning briefing"
    ```
-   **Prioritize your tasks:**
    ```bash
    adk web "prioritize my tasks"
    ```
-   **Plan a new project:**
    ```bash
    adk web "plan my product launch"
    ```
-   **Create a calendar event:**
    ```bash
    adk web "schedule a meeting with John tomorrow at 2pm"
    ```

## Roadmap

Here are some potential future enhancements for this project:

-   **Enhanced Natural Language Understanding**: Improve the coordinator agent's ability to understand more complex and nuanced user requests.
-   **Support for More Tools**: Integrate with other popular productivity tools like Slack, Jira, or Trello.
-   **Proactive Agents**: Develop agents that can proactively suggest actions or provide reminders without explicit user requests.
-   **Web Interface**: Create a web-based user interface for interacting with the agents.
-   **More Sophisticated Prioritization**: Enhance the `SmartPrioritizationAgent` with more advanced machine learning models to provide even more accurate and personalized prioritizations.
-   **Long-Term Memory**: Implement a mechanism for the agents to remember user preferences and context across conversations.
-   **Testing and Evaluation Framework**: Develop a comprehensive framework for testing and evaluating the performance of the agents.
