# leto-modelizer-ai-proxy

## Description

This file describes how to contribute and develop for this open-source project.

### Requirements

* pipenv

    On modern Linux distributions, you can install pipenv using the following command:
        * ``` sudo apt install pipenv ```
        * ``` sudo apt install pipx && pipx install pipenv && pipx ensurepath ```
    **NOTE**: After PEP668, all python packages should be installed in a virtual environment (recommanded to use pipx) or using the debian package manager.

    Create virtual environment and install dependencies from your repo: ``` pipenv install ```

    Install dev dependencies: ``` pipenv install --dev ```

    Activate virtual environment: ``` pipenv shell ```

    To deactivate your virtual environment: ``` deactivate ```

## How to launch

### Local launch

In order to launch the API locally, you need to activate your virtual environment using pipenv.

Then, you just need to launch the following command from the root folder:

```shell
hypercorn src.main:app --reload --bind 127.0.0.1:8585
```

## Docker

You need to run the following commands to launch the API.

First build the docker image using the following command:

```sh
docker build -t leto-modelizer-ai-proxy .
```

Then run the image:

```sh
docker run -p 8585:8585 --net=host leto-modelizer-ai-proxy
```

Once your docker is running, you can request it on this url: ```http://localhost:8585/```

## Checkstyle

Before pushing your branch and open/synchronize a pull-request, you have to verify the checkstyle of your application. Here is the command to do so (on the root folder):

```shell
black .
```

## Dependencies update

You can check update of your code dependencies by running this command:

```shell
pipenv check
```

## How to launch unit tests

In order to launch the tests, you must be in the root folder and from it, you have to launch the following command:
```sh
pytest
```

To launch it with the coverage:
```sh
pytest --cov=. --cov-report term-missing
```

To launch it with the coverage and generate an HTML report:
```sh
pytest --cov=. --cov-report term-missing --cov-report html
firefox htmlcov/index.html
```

## How to add a new AI

In order to handle a new AI, you need to add it to:
- Create a new handler in `handlers` folder and in the new handler class should inherit from `BaseHandler`.
  - Currently you need to implement the `generate` method.
- Add the new handler in the factory `handlers/Factory.py`.
- Add a file called `configuration_description.json` that will describe the new AI settings and how to configure it.

### Example of Handler

```python
from src.handlers.BaseHandler import BaseHandler
from src.models.Diagram import Diagram
from src.models.Message import Message

class MyAIHandler(BaseHandler):

    def initialize(self):
        pass
    def generate(self, diagram: Diagram) -> str:
        pass
    def message(self, message: Message) -> str:
```

### Example of updating the factory

Once you have your handler, you need to add it in the factory.

```python
from src.configuration.configurationManager import ConfigurationManager
from src.handlers.OllamaHandler import OllamaHandler


class Factory:
    @staticmethod
    def get_handler(plugin_name: str):
       ## previous code for other handlers

       if plugin_name == "MyAI":
           return MyAIHandler()
```

### Example of configuration

Finally, you will have a `configuration` similar to:

```json
{
    "pluginPreferences":{
        "default": "ollama"
    },
    "ollama":
    {
        "base_url": "http://localhost:11434/api",
        "models": ["mistral"],
        "defaultModel": "mistral",
        "modelFiles": {
            "generate": {
                "default": "default-mistral-modelfile_generate",
                "@ditrit/kubernator-plugin": "default-kubernetes-mistral-modelfile_generate",
                "@ditrit/githubator-plugin": "default-githubactions-mistral-modelfile_generate"
            },
            "message": {
                "default": "default-mistral-modelfile_message",
                "@ditrit/kubernator-plugin": "default-kubernetes-mistral-modelfile_message",
                "@ditrit/githubator-plugin": "default-githubactions-mistral-modelfile_message"
            }
        }
    },
    "MyAI": {
        "base_url": "http://localhost:8080/api",
        "otherSetting": "value"
    }
}
```

A configuration_description.json file is essential for integrating any AI system with Leto-Modelizer-Admin, as it defines the fields administrators must fill out to configure the AI properly.

Here are the description of the configuration fields:

- **`handler`**
  - **Purpose**: Identifies the AI system or plugin this configuration belongs to (e.g., "ollama").
  - **Use**: Associates the field with a specific handler or module.

- **`key`**
  - **Purpose**: A unique identifier for the field used internally by the system.
  - **Use**: Represents the configuration parameter (e.g., `base_url`, `defaultModel`).

- **`type`**
  - **Purpose**: Specifies the type of input expected in the UI.
  - **Values**:
    - `"text"`: Single-line text input.
    - `"select"`: To create a dropdown menu.
    - `"textarea"`: Multi-line input for longer text.

- **`values`**
  - **Purpose**: Defines predefined selectable options (e.g., dropdown menu).
  - **Use**: Empty if free-form input is allowed; can be populated for fixed choices.

- **`defaultValue`**
  - **Purpose**: The pre-filled value shown to the user when the field is displayed.
  - **Use**: Ensures default configurations or suggested values are provided (e.g., `http://localhost:11434/api`).

- **`label`**
  - **Purpose**: The user-facing name of the field displayed in the UI.
  - **Use**: Briefly explains what the field represents (e.g., "Ollama server URL").

- **`title`**
  - **Purpose**: A short explanatory tooltip shown when hovering over the field in the UI.
  - **Use**: Provides additional context (e.g., "Define the URL of the Ollama server").

- **`description`**
  - **Purpose**: A detailed explanation of the field's purpose or expected input.
  - **Use**: Guides users on how to fill the field, especially for complex settings.

- **`pluginDependent`**
  - **Purpose**: Indicates whether the field is specific to a plugin.
  - **Values**:
    - `true`: Applies only to a specific plugin (e.g., plugin-specific instructions).
    - `false`: Applies globally.

- **`required`**
  - **Purpose**: Specifies if the field must be completed for the configuration to be valid.
  - **Values**:
    - `true`: Field is mandatory.
    - `false`: Field is optional.


See the `configuration_description.json` of Ollama for an example.

### Adding a new Ollama model file

You can find how to create your model file [here](https://github.com/ollama/ollama/blob/main/docs/modelfile.md)

Then add your model file in the `description_configuration.json` file, then through Leto-Modelizer-Admin you can configure it.

## How to launch e2e tests with Behave

Once you have your API started and running, either locally or using docker, you can just use the command `behave` (from the root folder).

## How to release

We use [Semantic Versioning](https://semver.org/spec/v2.0.0.html) as guideline for the version management.

Steps to release:
- Create a new branch labeled `release/vX.Y.Z` from the latest `main`.
- Improve the version number in `package.json`, `package-lock.json` and `changelog.md`.
- Verify the content of the `changelog.md`.
- Commit the modifications with the label `Release version X.Y.Z`.
- Create a pull request on GitHub for this branch into `main`.
- Once the pull request validated and merged, tag the `main` branch with `vX.Y.Z`.
- After the tag is pushed, make the release on the tag in GitHub.

## Git: Default branch

The default branch is `main`. Direct commit on it is forbidden. The only way to update the application is through pull request.

Release tags are only done on the `main` branch.

## Git: Branch naming policy

`[BRANCH_TYPE]/[BRANCH_NAME]`

* `BRANCH_TYPE` is a prefix to describe the purpose of the branch. Accepted prefixes are:
  * `feature`, used for feature development
  * `bugfix`, used for bug fix
  * `improvement`, used for refacto
  * `library`, used for updating library
  * `prerelease`, used for preparing the branch for the release
  * `release`, used for releasing project
  * `hotfix`, used for applying a hotfix on main
* `BRANCH_NAME` is managed by this regex: `[a-z0-9._-]` (`_` is used as space character).
