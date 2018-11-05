import pytest

from yaml2object import NodeMeta


class TestNode(object):

    def test_should_create_node_using_meta_class(self):
        node_dict = {'var1': 'value1', 'var2': 'value2'}
        TestNode = NodeMeta('TestNode', (object,), node_dict)

        assert TestNode.var1 == 'value1'
        assert TestNode.var2 == 'value2'
        assert TestNode.to_dict(TestNode) == node_dict

    def test_should_skip_non_word_character_param(self):
        node_dict = {'var1': 'value1', 'non-word-key': 'value2'}
        TestNode = NodeMeta('TestNode', (object,), node_dict)

        assert TestNode.var1 == 'value1'
        assert hasattr(TestNode, 'non-word-key') is False

    def test_should_add_underscore_before_keys_similary_to_python_keywords(self):
        node_dict = {'from': 'value1', 'None': 'value2'}
        TestNode = NodeMeta('TestNode', (object,), node_dict)

        assert TestNode._from == 'value1'
        assert TestNode._None == 'value2'

    @pytest.mark.parametrize("node_dict", [({'var1': 'value1', 'non-word-key': 'value2'}),
                                           ({'from': 'value1', 'None': 'value2'})])
    def test_to_dict_should_return_original_dict(self, node_dict):
        TestNode = NodeMeta('TestNode', (object,), node_dict)

        assert TestNode.to_dict(TestNode) == node_dict
