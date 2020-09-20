from .mythril import Mythril
from .securify import Securify
from .slither import Slither


class ToolFactory():

    TOOLS_CHOICES = ['all', 'mythril', 'securify', 'slither']

    def createTool(tool_type):
        if tool_type == "mythril":
            return [Mythril()]
        if tool_type == "securify":
            return [Securify()]
        if tool_type == "slither":
            return [Slither()]
        if tool_type == "all":
            return [Mythril(), Securify(), Slither()]
        raise ValueError(format)
    createTool = staticmethod(createTool)
