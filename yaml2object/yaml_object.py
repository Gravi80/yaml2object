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
            child_class = YAMLObject._create_node_for(name, namespace_content, mcs, bases, fields)
        else:
            child_class = type.__new__(mcs, name, bases, {**fields, **{namespace: namespace_content}})
        return child_class

    @classmethod
    def _create_node_for(cls, node_name, node_content, mcs, bases, fields):
        node_content_copy = dict(node_content)
        cls._create_sub_nodes_for(node_content_copy)
        child_class = type.__new__(mcs, node_name, bases, {**fields, **node_content_copy})
        child_class.to_dict = lambda: node_content
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
        source_log = 'source' if isinstance(source, dict) else f"'{source}'"
        if namespace:
            if YAMLObject._string_present(namespace) and (namespace in yaml_content):
                return yaml_content.get(namespace)
            else:
                logger.warning(f"Missing '{namespace}' param in {source_log}."
                               f" Converting {source_log} to object.")
                return yaml_content
        else:
            logger.warning(f"Missing namespace attribute. Converting {source_log} to object.")
            return yaml_content

    @classmethod
    def _create_sub_nodes_for(cls, content_hash):
        for param_key in content_hash:
            if isinstance(content_hash[param_key], list):
                for idx, elm in enumerate(content_hash[param_key]):
                    if isinstance(elm, dict):
                        content_hash[param_key][idx] = cls._create_node(f"{param_key.title()}{idx}",
                                                                        content_hash[param_key][idx])
                        cls._create_sub_nodes_for(content_hash[param_key][idx])
            if isinstance(content_hash[param_key], dict):
                content_hash[param_key] = cls._create_node(param_key.title(), content_hash[param_key])
                cls._create_sub_nodes_for(content_hash[param_key])

    @classmethod
    def _create_node(cls, name, node_dict):
        node = NodeMeta(name, (Node,), node_dict)()
        return node

    @classmethod
    def _string_present(mcs, string):
        return isinstance(string, str) and string is not ''
