Feature: Message API Testing

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
