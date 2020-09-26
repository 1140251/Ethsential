import json
import re
from . tool import Tool
from .result import Result


class Securify(Tool):
    def __init__(self):
        pass

    image = "1140251/securify"

    command = 'python3.7 securify/__main__.py {contract}'

    lang_supported = ["solidity"]

    def parse(self, str_output):

        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        result = ansi_escape.sub('', str_output)
        try:
            data = json.loads(result)
            return data
        except Exception as e:
            data = result.splitlines()
            string = "stderr"
            value = -1
            for s in data:
                if string in str(s):
                    value = data.index(s)
            if value != -1:
                result = data[value + 1]
                if('error' in result and 'sources' in result):
                    return Result(True, json.loads(result), None).to_json()
                else:
                    return Result(False, None, "Invalid data").to_json()
            else:
                map(str.strip, data)
                output = []
                for index, line in enumerate(data):
                    if "Severity:" in line:
                        json_response = {
                            "severity": line.replace("Severity:", '').strip(),
                            "pattern": "",
                            "description": "",
                            "type": "",
                            "contract": "",
                            "lines": "",
                            "function": ""
                        }
                    elif "Pattern:" in line:
                        line = line.replace("Pattern:", '')
                        json_response['pattern'] = line.strip()
                    elif "Description:" in line:
                        line_content = line.replace("Description:", '')
                        description = []
                        description.append(line_content.strip())
                        index = data.index(line) + 1
                        for description_line in data[index:]:
                            if "Type:" in description_line:
                                break
                            description.append(description_line.strip())
                        separator = ' '
                        json_response['description'] = separator.join(
                            description)
                    elif "Type:" in line:
                        line = line.replace("Type:", '')
                        json_response['type'] = line.strip()
                    elif "Contract:" in line:
                        line = line.replace("Contract:", '')
                        json_response['contract'] = line.strip()
                    elif "Line:" in line:
                        line = line.replace("Line:", '')
                        json_response['lines'] = [int(line.strip())]
                        output.append(json_response)
                return Result(True, output, None).to_json()
