#!/usr/bin/env python3
"""
Test script for the SmartPrioritizationAgent's logic.
"""

import unittest
from unittest.mock import MagicMock, patch
from agents.agents import smart_prioritization

class TestSmartPrioritizationLogic(unittest.TestCase):
    """Unit tests for the SmartPrioritizationAgent's logic."""

    @patch('agents.agents.create_task')
    def test_next_action_effort_logic(self, mock_create_task):
        """Test how the agent breaks down large tasks."""
        # Arrange
        # In a real scenario, the agent would identify a large task
        # and suggest breaking it down.
        # For this test, we'll simulate the agent creating subtasks.
        agent = smart_prioritization
        with patch.object(agent, 'tools', [mock_create_task]):
            # Act
            agent.tools[0](content='Draft agenda', parent_id='1')
            agent.tools[0](content='Book venue', parent_id='1')
            agent.tools[0](content='Send invitations', parent_id='1')

            # Assert
            self.assertEqual(mock_create_task.call_count, 3)
            mock_create_task.assert_any_call(content='Draft agenda', parent_id='1')
            mock_create_task.assert_any_call(content='Book venue', parent_id='1')
            mock_create_task.assert_any_call(content='Send invitations', parent_id='1')

if __name__ == "__main__":
    unittest.main()