from confar.aggregate import Aggregator
import unittest


class AggregatorTest(unittest.TestCase):

    def parse_yaml(self):
        Aggregator().parse_file(file_path='sample.yml')


unittest.main()
