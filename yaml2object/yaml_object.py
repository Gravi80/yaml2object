import keyword
import logging

from yaml2object import MissingSourceError, YAMLLoader, NodeMeta, Node

logger = logging.getLogger(__name__)
PYTHON_KEYWORDS = keyword.kwlist


class YAMLObject(type):
    def __new__(mcs, name, bases, fields):
        source = fields.get('source')
        namespace = fields.get('namespace')
        YAMLObject._valid_source(source)
        namespace_content = YAMLObject._namespace_content(namespace, source)
        if isinstance(namespace_content, dict):
            namespace_content_copy = dict(namespace_content)
            mcs._create_node_for(namespace_content_copy)
            child_class = type.__new__(mcs, name, bases, {**fields, **namespace_content_copy})
            child_class.to_dict = lambda: namespace_content
        else:
            child_class = type.__new__(mcs, name, bases, {**fields, **{namespace: namespace_content}})
        return child_class

    @classmethod
    def _valid_source(cls, source):
        if source and (YAMLObject._string_present(source) or isinstance(source, dict)):
            return source
        else:
            raise MissingSourceError('No file specified as YAML source')

    @classmethod
    def _namespace_content(cls, namespace, source):
        yaml_content = source if isinstance(source, dict) else YAMLLoader.load(source)
        if namespace:
            if YAMLObject._string_present(namespace) and (namespace in yaml_content):
                return yaml_content.get(namespace)
            else:
                logger.warning(f"Missing '{namespace}' param in '{source}'."
                               f"Converting '{source}' to object.")
                return yaml_content
        else:
            logger.warning(f"Missing namespace attribute.Converting '{source}' to object.")
            return yaml_content

    @classmethod
    def _create_node_for(cls, content_hash):
        for param_key in content_hash:
            if isinstance(content_hash[param_key], dict):
                node_dict = content_hash[param_key]
                content_hash[param_key] = NodeMeta(param_key.title(), (Node,), node_dict)()
                cls._create_node_for(content_hash[param_key])

    @classmethod
    def _string_present(mcs, string):
        return isinstance(string, str) and string is not ''
