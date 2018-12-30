import pytest
from mock import patch, ANY
from os.path import dirname

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

    def test_should_create_dict_inside_arrays_as_node(self):
        source = {'matrix': {'include': [1,
                                         'str',
                                         [1, 2],
                                         {'python': 3.6},
                                         {'python': 3.7, 'dist': 'xenial', 'sudo': True}]}}

        MatrixConfig = YAMLObject('MatrixConfig', (object,), {'source': source, 'namespace': 'matrix'})

        assert isinstance(MatrixConfig.include[0], int) is True
        assert isinstance(MatrixConfig.include[1], str) is True
        assert isinstance(MatrixConfig.include[2], list) is True
        assert issubclass(MatrixConfig.include[3].__class__, Node) is True
        assert issubclass(MatrixConfig.include[4].__class__, Node) is True

    def test_should_add_underscore_before_python_keywords(self):
        config_dict1 = {'from': 'value1', 'None': 'value2'}
        config_dict2 = {'some': {'while': 'value1', 'with': 'value2'}}
        Config1 = YAMLObject('Config', (object,), {'source': config_dict1})
        Config2 = YAMLObject('Config', (object,), {'source': config_dict2})

        assert Config1._from == 'value1'
        assert Config1._None == 'value2'
        assert Config2.some._while == 'value1'
        assert Config2.some._with == 'value2'

    def test_should_load_data_from_test_yml(self):
        yaml_file = f"{dirname(__file__)}/test.yml"

        class Config(metaclass=YAMLObject):
            source = yaml_file

        DefaultConfig = YAMLObject('DefaultConfig', (object,),
                                   {'source': yaml_file, 'namespace': 'defaults'})

        assert DefaultConfig.database.adapter == 'postgresql'
        assert DefaultConfig.port == 8000
        assert DefaultConfig.nested_param.param1.sub_param1 == 'sub_param1 value'
        assert DefaultConfig.nested_param.param1.sub_param2 == 'sub_param2 value'
        assert DefaultConfig.array_param == ['param1', 'param2', ANY]
        assert DefaultConfig.array_param[2].param3 == 'a'
        assert DefaultConfig.array_param[2].type == 'x'
        assert DefaultConfig.key_word_params._while == 'while'
        assert DefaultConfig.key_word_params._with == 'with'
        assert hasattr(Config, 'defaults') is True
        assert hasattr(Config, 'development') is True
        assert hasattr(Config, 'test') is True
