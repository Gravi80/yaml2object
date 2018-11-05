import keyword
import logging
import re

logger = logging.getLogger(__name__)
PYTHON_KEYWORDS = keyword.kwlist


class NodeMeta(type):

    def __new__(mcs, name, bases, node_dict):
        sanatize_dict = mcs._sanitize_values(node_dict)
        sanatize_dict['to_dict'] = lambda cls: node_dict
        child_class = super().__new__(mcs, name, bases, sanatize_dict)
        return child_class

    @staticmethod
    def _sanitize_values(dictionary):
        sanitized_dict = {}
        for key, value in dictionary.items():
            if re.match(r'^\w+$', key):
                if key in PYTHON_KEYWORDS:
                    logger.warning(
                        f'Param {key} is a python keyword. '
                        f'Adding _ (underscore) before the param and can be accessed as _{key}')
                    sanitized_dict[f'_{key}'] = value
                else:
                    sanitized_dict[key] = value
            else:
                logger.warning(
                    f'Skipping invalid param {key}. '
                    f'Param can only contain any word character (letter, number, underscore)')
        return sanitized_dict
