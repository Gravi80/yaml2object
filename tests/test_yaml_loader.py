import pytest
from mock import patch, Mock

from yaml2object import YAMLLoader, MissingSourceError


class TestYAMLLoader(object):

    @patch('yaml2object.yaml_loader.yaml')
    @patch("builtins.open")
    def test_should_load_yaml_content(self, mock_file_open, yaml_mock):
        yaml_file = 'some_file'
        open_mock = Mock(name="open")
        open_mock.__enter__ = lambda *args, **kw: yaml_file
        open_mock.__exit__ = lambda *args, **kw: None
        mock_file_open.return_value = open_mock
        yaml_mock.safe_load.return_value = 'some_content'

        content = YAMLLoader.load(yaml_file)

        mock_file_open.assert_called_once_with(yaml_file)
        yaml_mock.safe_load.assert_called_once_with(yaml_file)
        assert 'some_content' == content

    def test_should_raise_error_for_invalid_file(self):
        with pytest.raises(MissingSourceError) as excinfo:
            YAMLLoader.load('invalid_file_path')

        assert 'Invalid YAML source' in str(excinfo.value)
