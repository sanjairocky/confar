from .utils.parser import ParserFactory
from uuid import uuid4 as uuid


class Aggregator:

    def parse_file(self, file_path=''):

        if not file_path:
            raise FileNotFoundError(file_path)

        # Create a parser factory
        parser_factory = ParserFactory()

        # Get the parser based on the file extension
        parser = parser_factory.get_parser(file_path)

        # Parse the input file using the selected parser
        parsed_data = parser.parse(file_path)

        if 'name' not in parsed_data:
            raise KeyError('name is mandatory field')

        return parsed_data
