from pygls.server import LanguageServer

from pygls.features import (COMPLETION, TEXT_DOCUMENT_DID_CHANGE,
                            TEXT_DOCUMENT_DID_CLOSE, TEXT_DOCUMENT_DID_OPEN,
                            WORKSPACE_DID_CHANGE_CONFIGURATION, INITIALIZE)
from ..services import analyse_file, install_tools
from ..tools.tool_factory import ToolFactory


class EthSencialLS(LanguageServer):
    CMD_ANALYSE = 'analyse'
    CMD_INSTALL = 'install'

    def __init__(self):
        super().__init__()


ETHSENTIAL = EthSencialLS()


@ETHSENTIAL.feature(EthSencialLS.CMD_ANALYSE)
async def doAnalysisFeat(ls: EthSencialLS, params):

    uri = params.textDocument.uri
    active_doc = ls.workspace.get_document(uri)

    tools = []
    for tool in params.tools:
        new_tool = ToolFactory.createTool(tool)
        tools.extend(x for x in new_tool if x not in tools)
    result = analyse_file(active_doc.path.replace(
        '\\', '/'), params.lang, tools)
    return result  # parse error TODO


@ETHSENTIAL.feature(EthSencialLS.CMD_INSTALL)
async def doInstallFeat(ls: EthSencialLS, params):
    tools = []
    for tool in params.tools:
        new_tool = ToolFactory.createTool(tool)
        tools.extend(x for x in new_tool if x not in tools)
    try:
        install_tools(tools)
        return '200'
    except Exception as e:
        if hasattr(e, 'message'):
            return getattr(e, 'message', repr(e))
        else:
            return e


@ ETHSENTIAL.feature(WORKSPACE_DID_CHANGE_CONFIGURATION)
async def didChangeWorkspace(ls: EthSencialLS, *args):
    return


@ ETHSENTIAL.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls, params):

    text_doc = ls.workspace.get_document(params.textDocument.uri)
