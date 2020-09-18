import json


class Result:
    def __init__(self, success, issues, error):
        self.success = success
        self.issues = issues
        self.error = error

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda obj: self.__dict__))
