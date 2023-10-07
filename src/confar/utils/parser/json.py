import json


class JSONParser:
    def parse(self, file_path):
        with open(file_path, "r") as stream:
            return json.load(stream)
