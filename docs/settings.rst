Settings
========

Project global settings.


Global variables
----------------

**DEBUG**: True for development settings and False for production.

**SETTINGS_DIR**: Settings directory absolute path.

**ROOT_DIR**: Project directory absolute path.

**YAML_TO_DICT**: Referentiel dict to map yaml files to python dict as key: yaml name, value: python dict to store file content.


Yaml global informations dictionaries
-------------------------------------

All informations are found in .yml file in settings directory.

Yaml file are formated by section.
*prod* for production settings, *dev* for development settings by default, see YamlParser documentation for customisation.


**DATABASE**: Databases info with following format

Yaml: database.yml


**LOGGING**: Logging configuration. Refer to python logging module for file format.

Yaml: logging.yml


**DIRECTORY**: Project directories path as key: directory reference, value: directory path.

Yaml: directory.yml


**VIEWS**: Views urls for REST API as key: url path, value: view class.

Yaml: rest_views.yml


**SWAGGER**: Swagger configuration.

yaml: swagger.yml


Utils function
--------------

**setup_logging**: Setup logging configuration using LOGGING global.

**create_directory**: Automaticaly create all directory found in DIRECTORY global if they does not exists.
