# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

## [Unreleased]

### Added

 - Configuration is now handle through the Leto-Modelizer-Admin, the user give the configuration for the AIs and not through the file anymore.

## [1.0.0] - 2024/10/15

### Added

 - Setup the project.
 - Create Ollama handler in order to generate code through the /api/diagram route.
 - Handle Modelfiles for Ollama (terraform, kubernetes and github actions).
 - Migrate to python 3.12.
 - Migrate from uvicorn to hypercorn.
 - Add new Ollama model files (for generate and message).
 - Handle new /api/message endpoint for Ollama, that send messages to the Ollama AI and get a response with the associated context.
 - Added new Gemini model files (for generate and message). Conversation with a context is not supported.
 - Added Docker compose (works only with nvidia gpu).
 - The initialize script is now separated from the main script. It can be launched from the root folder, anytime.
 - Add health endpoint.

[1.0.0]: https://github.com/ditrit/leto-modelizer-ai-proxy/blob/main/changelog.md#1.0.0

