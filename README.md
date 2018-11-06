### Status
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/yaml2object.svg)](https://pypi.python.org/pypi/yaml2object/)
[![PyPI](https://img.shields.io/pypi/v/yaml2object.svg)](https://pypi.python.org/pypi/yaml2object)
[![Build Status](https://travis-ci.org/imravishar/yaml2object.svg?branch=master)](https://travis-ci.org/imravishar/yaml2object)
[![Coverage Status](https://coveralls.io/repos/github/imravishar/yaml2object/badge.svg)](https://coveralls.io/github/imravishar/yaml2object)
[![last commit](https://img.shields.io/github/last-commit/imravishar/yaml2object.svg?label=last%20commit)](https://github.com/imravishar/yaml2object/commits/master)
[![License](https://img.shields.io/hexpm/l/plug.svg)](https://tldrlegal.com/license/apache-license-2.0-(apache-2.0))
[![PyPI Package monthly downloads](https://img.shields.io/pypi/dm/yaml2object.svg?style=flat)](https://pypi.python.org/pypi/yaml2object)
[![PyPI download week](https://img.shields.io/pypi/dw/yaml2object.svg)](https://pypi.python.org/pypi/yaml2object)

yaml2object is a python library that allows dot notation access for YAML file.

Install
-------
```
pip install yaml2object
```

Usage
------
**1. Create your YAML settings**
```
# config.yml
defaults: &defaults
  database:
    adapter: postgresql
    database: development
  port: 8000
  nested_param:
    param1:
        sub_param1: 'sub_param1 value'
        sub_param2: 'sub_param2 value'

development:
  <<: *defaults

test:
  <<: *defaults
  port: 8001

```
**2. Define your class**

<ol type="a">
  <li>Set <b>yaml2object.YAMLObject</b> as meta-class of your config class.</li>
  <li>Provide <b>source, namespace</b> as class fields.
    <ul>
      <li>scource: YAML file path OR python dictionary</li>
      <li>namespace: param key in YAML file OR python dictionary</li>
    </ul>
  </li>
</ol>

###### When source is a YAML file

```python
from yaml2object import YAMLObject

class Config(metaclass=YAMLObject):
    source = 'config.yml'

> WarningLog: Missing namespace attribute. Converting 'config.yml' to object.
```
```python
from yaml2object import YAMLObject

class Config(metaclass=YAMLObject):
    source = 'config.yml'
    namespace = 'invalid'

> WarningLog: Missing 'invalid' param in 'config.yml'. Converting 'config.yml' to object.
```
```python
from yaml2object import YAMLObject

class DevelopmentConfig(metaclass=YAMLObject):
    source = 'config.yml'
    namespace = 'development'

class TestConfig(metaclass=YAMLObject):
    source = 'config.yml'
    namespace = 'test'

DefaultConfig = YAMLObject('DefaultConfig', (object,), {'source': 'config.yml', 'namespace': 'defaults'})
```

###### Source can also be a python dictionary
```python
from yaml2object import YAMLObject

config = {'defaults': {'database':
                            {'adapter': 'postgresql', 'database': 'development'},
                       'port': 8000,
                       'nested_param':
                            {'param1': {'sub_param1': 'sub_param1 value', 'sub_param2': 'sub_param2 value'}}}}

DefaultConfig = YAMLObject('DefaultConfig', (object,), {'source': config, 'namespace': 'defaults'})
```

**3. Access your YAML as python object**
```python
>>> Config.to_dict()
>>> Config.development.to_dict()
>>> Config.development.database.to_dict()
>>> Config.development.database.adapter
>>> Config.development.nested_param.param1.sub_param1

>>> DevelopmentConfig.to_dict()
>>> DevelopmentConfig.database.to_dict()
>>> DevelopmentConfig.database.adapter
>>> DevelopmentConfig.database.database

>>> TestConfig.to_dict()
>>> TestConfig.port
>>> TestConfig.database.to_dict()
>>> TestConfig.database.adapter
>>> TestConfig.database.database

>>> DefaultConfig.to_dict()
>>> DefaultConfig.database.to_dict()
>>> DefaultConfig.database.adapter
>>> DefaultConfig.nested_param.param1.sub_param1
```
