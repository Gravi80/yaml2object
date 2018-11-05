import yaml

from yaml2object import MissingSourceError


class YAMLLoader:

    @classmethod
    def load(cls, file_path):
        try:
            with open(file_path) as file:
                content = yaml.safe_load(file)
            return content
        except FileNotFoundError:
            raise MissingSourceError('Invalid YAML source')
