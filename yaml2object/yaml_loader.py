from os import path

import yaml

from yaml2object import MissingSourceError


class YAMLLoader:

    @classmethod
    def load(cls, file_path):
        full_path = path.abspath(path.expanduser(file_path))
        try:
            with open(full_path) as file:
                content = yaml.safe_load(file)
            return content
        except FileNotFoundError:
            raise MissingSourceError('Invalid YAML source')
