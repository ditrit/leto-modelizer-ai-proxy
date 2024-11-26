Feature: Configuration API Testing

Background: Initialize configuration
    When I set Ollama modelFiles in the context
    And  I encrypt the configuration with secret decryption key (from env) and save it in the context
        | key                                        | value                                                                                            | type |
        | plugin.preferences.default                 | ollama                                                                                           |      |
        | ollama.base_url                            | http://ollama:11434/api                                                                          |      |
        | ollama.allowRawResults                     | true                                                                                             |      |
        | ollama.defaultModel                        | mistral                                                                                          |      |
        | ollama.modelFiles.generate.default         | $default_generate                                                                                |      |
        | ollama.modelFiles.message.default          | $default_message                                                                                 |      |
        | gemini.base_url                            | https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent  |      |
        | gemini.key                                 | MySecretKeyToBeReplaced                                                                          |      |
        | gemini.system_instruction.generate.default | {\"system_instruction\": {\"parts\": {\"text\": \"You are an experienced Devops engineer\"}}}    |      |
        | gemini.system_instruction.message.default  | {\"system_instruction\": {\"parts\": {\"text\": \"You are an experienced Devops engineer\"}}}    |      |
    And I request "api/configurations" with method "POST" with encrypted configuration    
    Then I expect 201 as status code
    And I expect object field "status" is "success"

Scenario: Initializing all AI
    When I request "api/configurations/initialize" with method "POST"
    Then I expect 201 as status code
    And I expect object field "status" is "success"

Scenario: Get all configurations descriptions
    When I request "api/configurations/descriptions" with method "GET"
    Then I expect 200 as status code
    And I expect the response field "ollama[0].key" to be "base_url"
    And I expect the response field "ollama[1].key" to be "defaultModel"
    And I expect the response field "gemini[0].key" to be "base_url"
    And I expect the response field "gemini[1].key" to be "key"
    And I expect the response field "gemini[2].key" to be "system_instruction.generate.default"