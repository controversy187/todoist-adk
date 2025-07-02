# Project Improvements

This document outlines the planned improvements for the Task Agent project.

## Phase 1: Refactoring and Simplification

- [x] **Consolidate Agent Definitions**: Currently, agent definitions are spread across multiple files. Consolidating them into a single `agents.py` file will improve readability and maintainability.
- [x] **Simplify Tooling**: The `todoist_tools.py` file can be simplified. The `get_work_project_id` function is called frequently and can be cached.
- [x] **Standardize Agent Naming**: Ensure all agent names follow a consistent convention.
- [x] **Improve Test Coverage**: Add more comprehensive tests for the `SmartPrioritizationAgent`.

## Phase 2: Feature Enhancements

- [x] **Add a 'morning briefing' feature**: Create a new agent that provides a summary of the day's priorities.
- [x] **Integrate with Google Calendar**: Add the ability to sync ToDoist tasks with Google Calendar.

## Phase 3: Bug Fixes and Performance

- [x] **Address API Rate Limiting**: Implement proper handling of ToDoist API rate limits.
- [x] **Optimize Task Fetching**: Improve the performance of fetching tasks, especially for large projects.
- [x] **Fix Subtask Handling**: Ensure subtasks are correctly handled in all agents.



╭─────────────────────────────────────╮
│                                     │
│  Agent powering down. Goodbye!      │
│                                     │
│                                     │
│  Cumulative Stats (2 Turns)         │
│                                     │
│  Input Tokens            7,155,977  │
│  Output Tokens              48,977  │
│  Thoughts Tokens               255  │
│  Cached Tokens   5,534,820 (76.8%)  │
│  ─────────────────────────────────  │
│  Total Tokens            7,205,209  │
│                                     │
│  Total duration (API)      10m 44s  │
│  Total duration (wall)  11h 56m 4s  │
│                                     │
╰─────────────────────────────────────╯
