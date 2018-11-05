pip install yaml2object

**Usage**
=========

1. Create your YAML settings
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
2. Define your class
```
from yaml2object import YAMLObject

class Config(metaclass=YAMLObject):
    source = 'config.yml'

Warning Log: Missing namespace attribute. Converting 'config.yml' to object.


class Config(metaclass=YAMLObject):
    source = 'config.yml'
    namespace = 'invalid'

Warning Log: Missing 'invalid' param in 'config.yml'. Converting 'config.yml' to object.


class DevelopmentConfig(metaclass=YAMLObject):
    source = 'config.yml'
    namespace = 'development'

class TestConfig(metaclass=YAMLObject):
    source = 'config.yml'
    namespace = 'test'

```

3. Access your YAML as python object
```
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
```
