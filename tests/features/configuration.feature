Feature: Configuration API Testing

Scenario: Initializing all AI
    When I request "api/configurations/initialize" with method "POST" with json
        | key     | value  | type   |
        | handler | ollama |        |
    Then I expect 200 as status code
    And I expect object field "status" is "ok"

Scenario: Initializing all AI
    When I request "api/configurations" with method "POST" with json
        | key                                                      | value                              | type   |
        | configuration.ollama.default                             | mistral                            |        |
        | configuration.ollama.system.instruction.generate.default | default-mistral-modelfile_generate |        |
    Then I expect 200 as status code
    And I expect the response field "ollama.default" to be "mistral"


Scenario: Get all configurations descriptions
    When I request "api/configurations/descriptions" with method "GET"
    Then I expect 200 as status code
    And I expect the response field "ollama[0].key" to be "base.url"
    And I expect the response field "ollama[2].key" to be "model.files.generate.default"
    And I expect the response field "gemini[0].key" to be "base.url"
    And I expect the response field "gemini[2].key" to be "system.instruction.generate.default"