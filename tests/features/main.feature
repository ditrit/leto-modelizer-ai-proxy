Feature: Testing main endpoint

Scenario: Testing welcoming endpoint
    When I request "/" with method "GET"
    Then I expect 200 as status code
    And I expect object field "message" is "Hello From Leto-Modelizer-AI-API!"

