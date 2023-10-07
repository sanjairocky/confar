from .utils.parser import ParserFactory


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

        return parsed_data
