import yaml
import os
import re


path_matcher = re.compile(r'.*\$\{([^}^{]+)\}.*')


def path_constructor(loader, node):
    return os.path.expandvars(node.value)


class EnvVarLoader(yaml.SafeLoader):
    pass


EnvVarLoader.add_implicit_resolver('!path', path_matcher, None)
EnvVarLoader.add_constructor('!path', path_constructor)


class YAMLParser:

    def __init__(self) -> None:
        self.ext = ['.yaml', '.yml']

    def parse(self, file: str = ""):
        with open(file=file, mode="r") as stream:
            processed_yaml = yaml.load(stream=stream, Loader=EnvVarLoader)
            return processed_yaml
