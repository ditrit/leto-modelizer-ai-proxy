# leto-modelizer-ai-proxy

## Description
Leto-Modelizer AI Proxy is a Python-based proxy API which interfaces with several AI models in order to generate infrastructure code for Leto-Modelizer.
The purpose of this API is to facilitate the automation and customization of infrastructure code generation for various use cases.

Linked to Leto-Modelizer, the API provides a seamless integration with the powerful infrastructure generation capabilities of the Leto-Modelizer framework. Whether you need to generate code for cloud infrastructure, or any other domain-specific infrastructure, our API leverages the advanced modeling capabilities of Leto-Modelizer to automate and optimize the code generation process.

Built on top of Python's robust web framework, the Leto-Modelizer Proxy API offers a flexible and extensible architecture for integrating various AI models. Whether you prefer using pre-trained models or training your own custom models, our API seamlessly handles the code generation process. By leveraging the power of AI and Leto-Modelizer, our API simplifies the task of infrastructure code generation, saving you time.


## Setup

Currently this project use Ollama or Gemini in order to generate code.

## Configuration

To configure the API, you need to edit the `configuration/configuration.json` file (default location).
Or you can set the environment variables `API_CONFIGURATION` and put the `configuration.json` file in that path`.

Currently the configuration has the following settings:

| Setting            | Description                                                                                     |
|--------------------|-------------------------------------------------------------------------------------------------|
| pluginPreferences  | A dictionary containing the plugin preferences, which are the AI models to use for what plugin. |
| ollama             | A dictionary containing the ollama configuration (cf: next section).                            |
| Gemini             | A dictionary containing the Gemini configuration (cf: next section).                            |

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
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent",
        "key": "YOUR-KEY",
        "system_instruction": {
            "generate": {
                "default": "default-generate.json",
                "@ditrit/kubernator-plugin": "default-kubernetes.json",
                "@ditrit/githubator-plugin": "default-githubactions.json"
            },
            "message": {
                "default": "default-message.json",
                "@ditrit/kubernator-plugin": "default-kubernetes.json",
                "@ditrit/githubator-plugin": "default-githubactions.json"
            }
        }
    }
}
```

The mandatory `default` key is used to specify which AI model to use by default for every plugin.
Moreover, the AI precised for each plugin in the `pluginPreferences` key must exist in the `configuration.json`.

### Ollama

Ollama can be found here: https://github.com/ollama/ollama
Ollama has the following settings:

| Setting       | Description                                                                                            |
|---------------|--------------------------------------------------------------------------------------------------------|
| base_url      | The base URL of the Ollama API.                                                                        |
| models        | A list of models to use.                                                                               |
| defaultModel  | The default model to use.                                                                              |
| modelFiles    | The Ollama model files to use. They are seperate by purpose, one for generate and one for message mode |

Currently only the default model is used. But later, we will be able to handle more smoothly the rest of the models to use, depending on the usage.

### Gemini

Gemini can be found here: https://github.com/google-gemini/
**Don't forget to set the `key` in the `configuration.json` by creating an account and getting an API key.**
Gemini has the following settings:

| Setting            | Description                                                                                              |
|--------------------|----------------------------------------------------------------------------------------------------------|
| base_url           | The base URL of the Gemini API.                                                                          |
| key                | The API key to use.                                                                                      |
| system_instruction | Json file used to generate the response according to the methodology we need. (same as Ollama modelfiles)|

**NOTE**: Currently Gemini does not handle the message mode (conversation with a context) correctly due to the way the API works with context.

### Other AI models

Currently the API only supports the Ollama and Gemini.
In the near future, we will be able to have more AI models.
Moreover, you can add your own AI models, to do so see [here](CONTRIBUTING.md#how-to-add-a-new-ai).


## Installing Ollama (if you want to use Ollama locally)
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

### Gemini API

For Gemini, you need to create an account and get an API key, on this website: https://ai.google.dev/
Then you just need to add it in the `configuration.json` file, in the `ai-models` section.


## How to launch the API using hypercorn

First install pipenv and create a virtual environment with the needed packages:

* pipenv

    On modern Linux distributions, you can install pipenv using the following command:

        * ``` sudo apt install pipenv ```

        * ``` sudo apt install pipx && pipx install pipenv && pipx ensurepath ```

    **NOTE**: After PEP668, all python packages should be installed in a virtual environment (recommanded to use pipx) or using the debian package manager.

    Create virtual environment and install dependencies from your repo: ``` pipenv install ```

    Install dev dependencies: ``` pipenv install --dev ```

    Activate virtual environment: ``` pipenv shell ```

    To deactivate your virtual environment: ``` deactivate ```

Then launch the API using hypercorn (from the root folder):

```sh
hypercorn src.main:app --reload --bind 127.0.0.1:8585
```

Once it is running, you can request it on this url: ```http://localhost:8585/```

And the Swagger UI is available on this url: ```http://localhost:8585/docs```

## How to launch the API using docker 

### With NVIDIA GPU

You need to run the following commands to launch the API.

First install NVIDIA Container Toolkit:
```
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Configure NVIDIA Container Toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Test GPU integration
docker run --gpus all nvidia/cuda:11.5.2-base-ubuntu20.04 nvidia-smi
```

then build the docker image using the following command:

```sh
docker build -t leto-modelizer-ai-proxy .
```

Then run the image:

```sh
docker compose up -f docker-compose-nvidia.yaml
```

### Without NVIDIA GPU

Build the docker image using the following command:

```sh
docker build -t leto-modelizer-ai-proxy .
```

Then run the image:

```sh
docker compose up -f docker-compose.yaml
```

Once your docker is running, you can request it on this url: ```http://localhost:8585/```

## Endpoint

Currently the API only supports these enpoints:

|  Method | Enpoint       | Description                                                             |
|---------|---------------|-------------------------------------------------------------------------|
| GET     | /             | Returning a welcome message                                             |
| POST    | /api/diagram  | Generating diagram code                                                 |
| POST    | /api/message  | Send a message to the AI and get a response with the associated context |

