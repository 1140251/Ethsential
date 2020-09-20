import json

from .tool import Tool
from .result import Result


class Mythril(Tool):
    def __init__(self):
        pass

    image = "mythril/myth:0.22.7"

    command = "analyze {contract} --solv {version} -o json"

    lang_supported = ["solidity"]

    def parse(self, str_output):

        try:
            data = json.loads(str_output)
            return data
        except Exception as e:
            data = str_output.splitlines()
            result = json.loads(data[-1])

            json_response = []
            if result["success"] and result['issues']:
                for issue in result['issues']:

                    json_response.append({
                        "severity": issue["severity"],
                        "pattern": issue["title"],
                        "description": issue["description"],
                        "lines": [issue["lineno"]],
                        "function": issue["function"],
                        "contract": issue["contract"],
                        "raw_output": issue
                    })

                return Result(True, json_response, None).to_json()

            return Result(False, None, result["error"]).to_json()
