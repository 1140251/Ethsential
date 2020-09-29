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

                    new_issue = {
                        "severity": issue["severity"] if(
                            'severity' in issue) else "",
                        "pattern": issue["title"] if(
                            'pattern' in issue) else "",
                        "description": issue["description"] if(
                            'description' in issue) else "",
                        "lines": [int(issue["lineno"])] if(
                            'lineno' in issue) else [],
                        "function": issue["function"] if(
                            'function' in issue) else "",
                        "contract": issue["contract"] if(
                            'contract' in issue) else "",
                        "raw_output": issue
                    }
                    if('swc-id' in issue):
                        new_issue["pattern"] += " - SWC ID=" + issue["swc-id"]
                    json_response.append(new_issue)

                return Result(True, json_response, None).to_json()

            return Result(False, None, result["error"]).to_json()
