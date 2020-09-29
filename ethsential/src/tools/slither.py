import json

from . tool import Tool


class Slither(Tool):
    def __init__(self):
        pass

    image = "1140251/slither"

    command = '/bin/bash -c "solc use {version} && slither {contract} --json -"'

    lang_supported = ["solidity"]

    def parse(self, str_output):
        result = {}
        try:
            result = json.loads(str_output)

        except Exception:
            data = str_output.splitlines()
            result = json.loads(data[-1])
        finally:
            result["issues"] = []
            if result["success"] and result['results'] and "detectors" in result['results']:

                for detector in result['results']['detectors']:

                    for element in detector["elements"]:
                        json_response = {
                            "severity": detector["impact"] if(
                                'impact' in detector) else "",
                            "pattern": detector["check"] if(
                                'check' in detector) else "",
                            "description": detector["description"] if(
                                'description' in detector) else "",
                            "lines": [int(i) for i in element["source_mapping"]["lines"]],
                            "function": element["name"] if(
                                'name' in detector) else "",
                            "contract": ""
                        }

                        if element["type"] == "function":
                            if "type_specific_fields" in element and "signature" in element["type_specific_fields"]:
                                json_response["function"] = element["type_specific_fields"]["signature"]

                        if element["type"] != "contract":
                            json_response["contract"] = self.get_contract_name(
                                element)

                        result["issues"].append(json_response)
                result['results'] = None
            return result

    def get_contract_name(self, element):
        if "type_specific_fields" in element and "parent" in element["type_specific_fields"]:
            if "type" in element["type_specific_fields"]["parent"] and element["type_specific_fields"]["parent"]["type"] == "contract":
                return element["type_specific_fields"]["parent"]["name"]
            else:
                return self.get_contract_name(element["type_specific_fields"]["parent"])
        else:
            return None
