# leto-modelizer-ai-proxy

## Description

This file describes how to contribute and develop for this open-source project.

### Requirements

* pipenv

    Install pipenv:  ``` pip install pipenv ```

    Create virtual environment and install dependencies from your repo: ``` pipenv install ```

    Install dev dependencies: ``` pipenv install --dev ```

    Activate virtual environment: ``` pipenv shell ```

    To deactivate your virtual environment: ``` deactivate ```

## How to launch

### Local launch

In order to launch the API locally, you need to activate your virtual environment using pipenv.

Then, you just need to launch the following command from the root folder:

```shell
uvicorn src.main:app --reload
```

## Docker

You need to run the following commands to launch the API.

First build the docker image using the following command:

```sh
docker build -t leto-modelizer-ai-proxy .
```

Then run the image:

```sh
docker run -p 8000:8000 --net=host leto-modelizer-ai-proxy
```

Once your docker is running, you can request it on this url: ```http://localhost:8000/```

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
- Add a section in `configuration/configurationManager.py` with the name of the new AI and its settings.

### Example of Handler

```python
from src.handlers.BaseHandler import BaseHandler

class MyAIHandler(BaseHandler):

    def initialize(self):
        pass
    def generate(self, question: str) -> str:
        pass
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

Finally, you need to add the new AI in the `configuration.json` file.

```json
{
    "pluginPreferences":{
        "default": "ollama"
    },
    "ai-models":{
        "ollama":
        {
            "base_url": "http://localhost:11434/api",
            "models": ["mistral"],
            "defaultModel": "mistral",
            "modelFiles": ["default-mistral-modelfile"]
        },
        "MyAI": {
            "base_url": "http://localhost:8080/api",
            "otherSetting": "value"
        }    
    }
}
```

### Adding a new Ollama model file

First add your modelfile in the `src/handlers/Ollama/ModelFiles` folder.
You can find how to create your model file [here](https://github.com/ollama/ollama/blob/main/docs/modelfile.md)

Then add your model file in the `configuration.json` file, in the `ai-models.ollama.modelFiles` section.

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
