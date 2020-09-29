import argparse
import os
import json
import errno
from time import time
from ..services import analyse_file, install_tools
from ..tools.tool_factory import ToolFactory


class Command():

    def exec_cmd(self, args: argparse.Namespace):
        files_to_analyze = []
        tools = []
        for tool in args.tools:
            new_tool = ToolFactory.createTool(tool)
            tools.extend(x for x in new_tool if x not in tools)
        for file in args.file:
            # analyse files
            if not os.path.exists(file):
                raise FileNotFoundError(
                    errno.ENOENT, os.strerror(errno.ENOENT), file)
            if os.path.basename(file).endswith('.sol'):
                files_to_analyze.append((file, 'solidity'))
            elif os.path.basename(file).endswith('.py'):
                files_to_analyze.append((file, 'vyper'))
                # analyse dirs recursively
            elif os.path.isdir(file):
                for root, _, files in os.walk(file):
                    for name in files:
                        if name.endswith('.sol'):
                            files_to_analyze.append(
                                (os.path.join(root, name), 'solidity'))
                        if name.endswith('.py'):
                            files_to_analyze.append(
                                (os.path.join(root, name), 'vyper'))

            else:
                raise ValueError(
                    '%s is not a directory or a solidity/vyper file' % file)
        for file, lang in files_to_analyze:
            start = time()
            available_tools = list(
                filter(lambda tool: lang in tool.lang_supported, tools))
            result = analyse_file(file, lang, available_tools)
            file_name = os.path.splitext(os.path.basename(file))[0]
            end = time()

            if not os.path.exists(args.outputPath):
                os.makedirs(args.outputPath)
            result_file_full_path = args.outputPath + 'result_' + \
                file_name + '_' + str(time()) + '.json'
            with open(os.path.join(os.path.curdir, result_file_full_path), 'w') as f:
                json.dump({"result": result, "duration": str(
                    round(end-start))}, f, indent=2)

    def install(self):
        install_tools(ToolFactory.createTool('all'))


CLI = Command()
