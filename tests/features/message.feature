Feature: Message API Testing

Background: Initialize configuration
    When I set Ollama modelFiles in the context
    When I encrypt the configuration with secret decryption key (from env) and save it in the context
        | key                                        | value                                                                                            | type |
        | plugin.preferences.default                 | ollama                                                                                           |      |
        | ollama.base_url                            | http://ollama:11434/api                                                                          |      |
        | ollama.defaultModel                        | mistral                                                                                          |      |
        | ollama.allowRawResults                     | true                                                                                             |      |
        | ollama.modelFiles.generate.default         | FROM mistral                                                                                     |      |
        | ollama.modelFiles.message.default          | FROM mistral                                                                                     |      |
        | gemini.base_url                            | https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent  |      |
        | gemini.key                                 | MySecretKeyToBeReplaced                                                                          |      |
        | gemini.system_instruction.generate.default | {\"system_instruction\": {\"parts\": {\"text\": \"You are an experienced Devops engineer\"}}}    |      |
        | gemini.system_instruction.message.default  | {\"system_instruction\": {\"parts\": {\"text\": \"You are an experienced Devops engineer\"}}}    |      |
    And I request "api/configurations" with method "POST" with encrypted configuration
    Then I expect 201 as status code
    And I expect object field "status" is "success"
    When I request "api/configurations/initialize" with method "POST"
    Then I expect 201 as status code
    And I expect object field "status" is "success"

Scenario: Simulating a conversation using ollama
    When I request "api/message/" with method "POST" with json
        | key        | value                                   | type   |
        | pluginName | @ditrit/kubernator-plugin               |        |
        | message    | explain me the code of test.yml         |        |
        | files      | [{"path": "test.yml", "content": "apiVersion: v1\nkind: Pod\nmetadata:\n  name: nginx\nspec:\n  containers:\n    - name: nginx\n      image: nginx:latest\n      ports:\n        - containerPort: 80"}] | json |
    Then I expect 200 as status code
    And  I save the field "context" of the response in the context

    When I request "api/message/" with method "POST" with json
        | key        | value                                         | type   |
        | pluginName | @ditrit/kubernator-plugin                     |        |
        | message    | Add a java application in the kubernetes code |        |
        | context    | $context                                      |        |
    Then I expect 200 as status code
