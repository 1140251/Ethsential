import unittest
from .tool_factory import ToolFactory
from .mythril import Mythril


class ToolFactoryTest(unittest.TestCase):

    def test_create_mythril_pass(self):
        tools = ToolFactory.createTool('mythril')
        self.assertIsInstance(tools[0], Mythril)

    def test_create_all_pass(self):
        tools = ToolFactory.createTool('all')
        self.assertEqual(len(tools), 3)

    def test_create_tool_fail(self):
        try:
            _ = ToolFactory.createTool('tool')
        except Exception as identifier:
            self.assertIsInstance(identifier, ValueError)
