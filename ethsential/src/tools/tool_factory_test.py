import unittest
from .tool_factory import ToolFactory
from .mythril import Mythril


class ToolFactoryTest(unittest.TestCase):

    def test_createTools_pass(self):
        tools = ToolFactory.createTool('mythril')
        self.assertIsInstance(tools[0], Mythril)

    def test_createTools_fail(self):
        try:
            _ = ToolFactory.createTool('tool')
        except Exception as identifier:
            self.assertIsInstance(identifier, ValueError)
