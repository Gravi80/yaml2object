import pytest
from mock import patch

from yaml2object import YAMLObject, MissingSourceError, Node


class TestYAMLObject(object):

    def test_should_raise_error_when_no_yaml_source_is_present(self):
        with pytest.raises(MissingSourceError) as excinfo:
            class Test(metaclass=YAMLObject):
                pass
        assert 'No file specified as YAML source' in str(excinfo.value)

    def test_should_raise_error_when_yaml_source_is_empty(self):
        with pytest.raises(MissingSourceError) as excinfo:
            class Test(metaclass=YAMLObject):
                source = ''
        assert 'No file specified as YAML source' in str(excinfo.value)

    def test_should_raise_error_when_yaml_source_is_not_string(self):
        with pytest.raises(MissingSourceError) as excinfo:
            class Test(metaclass=YAMLObject):
                source = ['some_path']
        assert 'No file specified as YAML source' in str(excinfo.value)

    @patch('yaml2object.yaml_object.YAMLLoader')
    def test_should_not_raise_error_for_valid_yaml_source(self, mock_yaml_loader):
        try:
            class Test(metaclass=YAMLObject):
                source = 'yamlf file path'
        except MissingSourceError:
            pytest.fail(f"Should not have received MissingSourceError error")

    @patch('yaml2object.yaml_object.YAMLLoader')
    def test_should_yaml_content_from_source(self, mock_yaml_loader):
        class Test(metaclass=YAMLObject):
            source = 'yaml file path'

        mock_yaml_loader.load.assert_called_once_with('yaml file path')

    @patch('yaml2object.yaml_object.YAMLLoader')
    def test_should_add_namespace_keys_as_attribute_to_child_class(self, mock_yaml_loader):
        yaml_content = {'key1': {'key11': 'value11'}, 'key2': 'value2'}
        mock_yaml_loader.load.return_value = yaml_content

        class Test(metaclass=YAMLObject):
            source = 'yaml file path'
            namespace = 'key1'

        assert 'value11' == Test.key11
        assert {'key11': 'value11'} == Test.to_dict()

    @pytest.mark.parametrize("key_value", [3, [1, 2, 3], 'value'])
    @patch('yaml2object.yaml_object.YAMLLoader')
    def test_should_add_assing_key_as_attribute_when_key_value_is_not_dict(self, mock_yaml_loader, key_value):
        yaml_content = {'key1': key_value}
        mock_yaml_loader.load.return_value = yaml_content

        class Test(metaclass=YAMLObject):
            source = 'yaml file path'
            namespace = 'key1'

        assert key_value == Test.key1
        assert hasattr(Test, 'to_dict') is False

    @patch('yaml2object.yaml_object.YAMLLoader')
    def test_should_add_all_keys_as_attributes_when_namespace_is_not_present(self, mock_yaml_loader):
        yaml_content = {'key1': {'key11': 'value11'}, 'key2': 'value2'}
        mock_yaml_loader.load.return_value = yaml_content

        class Test(metaclass=YAMLObject):
            source = 'yaml file path'

        assert issubclass(Test.key1.__class__, Node) is True
        assert 'value11' == Test.key1.key11
        assert {'key11': 'value11'} == Test.key1.to_dict()
        assert {'key1': {'key11': 'value11'}, 'key2': 'value2'} == Test.to_dict()
        assert 'value2' == Test.key2

    @patch('yaml2object.yaml_object.YAMLLoader')
    def test_should_add_all_keys_as_attributes_when_namespace_is_invalid(self, mock_yaml_loader):
        yaml_content = {'key1': {'key11': 'value11'}, 'key2': 'value2'}
        mock_yaml_loader.load.return_value = yaml_content

        class Test(metaclass=YAMLObject):
            source = 'yaml file path'
            namespace = 'invalid'

        assert issubclass(Test.key1.__class__, Node) is True
        assert 'value11' == Test.key1.key11
        assert {'key11': 'value11'} == Test.key1.to_dict()
        assert {'key1': {'key11': 'value11'}, 'key2': 'value2'} == Test.to_dict()
        assert 'value2' == Test.key2

    @patch('yaml2object.yaml_object.YAMLLoader')
    def test_should_create_nested_params_as_node(self, mock_yaml_loader):
        yaml_content = {'key1': {'key11': {'key111': {'key1111': 'value'}}}}
        mock_yaml_loader.load.return_value = yaml_content

        class Test(metaclass=YAMLObject):
            source = 'yaml file path'
            namespace = 'key1'

        assert issubclass(Test.key11.__class__, Node) is True
        assert issubclass(Test.key11.key111.__class__, Node) is True
        assert issubclass(Test.key11.key111.key1111.__class__, Node) is False

    @patch('yaml2object.yaml_object.logger')
    @patch('yaml2object.yaml_object.YAMLLoader')
    def test_should_log_warning_when_namespace_is_missing(self, mock_yaml_loader, logger_mock):
        yaml_content = {'key': 'value'}
        mock_yaml_loader.load.return_value = yaml_content

        class Test(metaclass=YAMLObject):
            source = 'yaml file path'

        logger_mock.warning.assert_called_once_with("Missing namespace attribute."
                                                    " Converting 'yaml file path' to object.")

    @patch('yaml2object.yaml_object.logger')
    @patch('yaml2object.yaml_object.YAMLLoader')
    def test_should_log_warning_when_namespace_is_invalid(self, mock_yaml_loader, logger_mock):
        yaml_content = {'key': 'value'}
        mock_yaml_loader.load.return_value = yaml_content

        class Test(metaclass=YAMLObject):
            source = 'yaml file path'
            namespace = 'invalid'

        logger_mock.warning.assert_called_once_with("Missing 'invalid' param in 'yaml file path'."
                                                    " Converting 'yaml file path' to object.")

    def test_should_allow_source_to_be_dictionary(self):
        yaml_content = {'key1': {'key11': 'value11'}, 'key2': 'value2'}

        class Test(metaclass=YAMLObject):
            source = yaml_content
            namespace = 'key1'

        assert 'value11' == Test.key11
        assert {'key11': 'value11'} == Test.to_dict()

    @patch('yaml2object.yaml_object.logger')
    def test_should_log_warning_when_namespace_is_missing_for_dict_source(self, logger_mock):
        yaml_content = {'key': 'value'}

        class Test(metaclass=YAMLObject):
            source = yaml_content

        logger_mock.warning.assert_called_once_with("Missing namespace attribute."
                                                    " Converting source to object.")

    @patch('yaml2object.yaml_object.logger')
    def test_should_log_warning_when_namespace_is_invalid_for_dict_source(self, logger_mock):
        yaml_content = {'key': 'value'}

        class Test(metaclass=YAMLObject):
            source = yaml_content
            namespace = 'invalid'

        logger_mock.warning.assert_called_once_with("Missing 'invalid' param in source."
                                                    " Converting source to object.")
