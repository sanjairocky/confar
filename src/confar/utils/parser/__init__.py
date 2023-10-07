from .json import JSONParser
from .yaml import YAMLParser
import os


class ParserFactory:
    def __init__(self):
        self.parsers = {
            ".yaml": YAMLParser,
            ".yml": YAMLParser,
            ".json": JSONParser,
        }

    def get_parser(self, file_path):
        file_ext = os.path.splitext(file_path)[-1].lower()
        parser_class = self.parsers.get(file_ext)
        if parser_class:
            return parser_class()
        else:
            raise ValueError(
                f"No parser available for file extension: {file_ext}")
