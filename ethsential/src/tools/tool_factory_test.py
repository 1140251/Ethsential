import unittest
from .tool_factory import ToolFactory
from .mythril import Mythril


class ToolFactoryTest(unittest.TestCase):

    def test_create_mythril_pass(self):
        tool_name = 'mythril'
        tools = ToolFactory.createTool(tool_name)
        self.assertIsInstance(tools[0], Mythril)

    def test_create_all_pass(self):
        tool_name = 'all'
        tools = ToolFactory.createTool(tool_name)
        self.assertEqual(len(tools), 3)

    def test_create_tool_fail(self):
        try:
            tool_name = 'tool'
            _ = ToolFactory.createTool(tool_name)
        except Exception as identifier:
            self.assertIsInstance(identifier, ValueError)
