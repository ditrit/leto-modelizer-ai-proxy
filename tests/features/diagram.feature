Feature: Diagram API Testing

Scenario: Generating code using ollama
    When I request "api/diagram/" with method "POST" with json
        | key         | value                                   | type   |
        | pluginName  | kubernator-plugin                       |        |
        | description | generate me some kubernetes code sample |        |
    Then I expect 200 as status code

Scenario: Wrong end point for diagram
    When I request "api/diagram/nope" with method "GET"
    Then I expect 404 as status code

