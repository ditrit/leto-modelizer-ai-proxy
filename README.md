# leto-modelizer-ia-api

## Description
Leto-Modelizer API is a Python-based API designed to generate infrastructure code using different AI (Artificial Intelligence) models. The purpose of this API is to facilitate the automation and customization of infrastructure code generation for various use cases.

Linked to Leto-Modelizer, the API provides a seamless integration with the powerful infrastructure generation capabilities of the Leto-Modelizer framework. Whether you need to generate code for cloud infrastructure, or any other domain-specific infrastructure, our API leverages the advanced modeling capabilities of Leto-Modelizer to automate and optimize the code generation process.

Built on top of Python's robust web framework, the Leto-Modelizer API offers a flexible and extensible architecture for integrating various AI models. Whether you prefer using pre-trained models or training your own custom models, our API seamlessly handles the code generation process. By leveraging the power of AI and Leto-Modelizer, our API simplifies the task of infrastructure code generation, saving you time.


## Setup

Currently this project use Ollama in order to generate code.
So you need to install Ollama on your local: 

```sh 
curl -fsSL https://ollama.com/install.sh | sh 
```

Then you have to pull a model from Ollama:

```sh 
ollama pull mistral 
```

### Testing Ollama

In order to test Ollama, you can run your model using the following command:

```sh
ollama run mistral
```

Then you can just ask it a question !

**NOTE**: You may need to install NVIDIA Container Toolkit to run Ollama.
cf: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html


## How to launch the API using uvicorn

First install pipenv and create a virtual environment with the needed packages:

* pipenv

    Install pipenv:  ``` pip install pipenv ```

    Create virtual environment and install dependencies from your repo: ``` pipenv install ```

    Install dev dependencies: ``` pipenv install --dev ```

    Activate virtual environment: ``` pipenv shell ```

    To deactivate your virtual environment: ``` deactivate ```

Then launch the API using uvicorn (from the root folder):

```sh
uvicorn src.main:app --reload
```

Once it is running, you can request it on this url: ```http://localhost:8000/```

## How to launch the API using docker

You need to run the following commands to launch the API.

First build the docker image using the following command:

```sh
docker build -t leto-modelizer-ia-api .
```

Then run the image:

```sh
docker run -p 8000:8000 --net=host leto-modelizer-ia-api
```

Once your docker is running, you can request it on this url: ```http://localhost:8000/```

## Configuration

To configure the API, you need to edit the `configuration/configuration.json` file (default location).
Or you can set the environment variables `API_CONFIGURATION` and put the `configuration.json` file in that path`.

Currently the configuration has the following settings:

| Setting            | Description                                                                                     |
|--------------------|-------------------------------------------------------------------------------------------------|
| pluginPreferences  | A dictionary containing the plugin preferences, which are the AI models to use for what plugin. |
| ollama             | A dictionary containing the ollama configuration (cf: next section).                            |

Here is an example of the `configuration.json` file:

```json
{
    "pluginPreferences":{
        "default": "ollama"
    },
    "ollama":
    {
        "base_url": "http://localhost:11434/api",
        "models": ["mistral"],
        "defaultModel": "mistral"
    }
}
```

The mandatory `default` key is used to specify which AI model to use by default for every plugin.
Moreover, the AI precised for each plugin in the `pluginPreferences` key must exist in the `configuration.json`.

### Ollama

Ollama can be found here: https://github.com/ollama/ollama
Ollama has the following settings:

| Setting       | Description                     |
|---------------|---------------------------------|
| base_url      | The base URL of the Ollama API. |
| models        | A list of models to use.        |
| defaultModel | The default model to use.        |

Currently only the default model is used. But later, we will be able to handle more smoothly the rest of the models to use, depending on the usage.

### Other AI models

Currently the API only supports the Ollama.
In the near future, we will be able to have more AI models.
Moreover, you can add your own AI models, to do so see [here](CONTRIBUTING.md#how-to-add-a-new-ai). 


## Endpoint

Currently the API only supports these enpoints:

|  Method | Enpoint       | Description                       |
|---------|---------------|-----------------------------------|
| GET     | /             | Returning a welcome message       |
| POST    | /api/diagram/ | Generating diagram code           |

