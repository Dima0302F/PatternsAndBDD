Feature: Get Notes
  As a user
  I want to retrieve all my notes
  So that I can see what I have written

  Background:
    Given the notes API is available

  Scenario: Get notes when there are no notes
    Given there are no notes in the system
    When I send a request to get all notes
    Then the response status code should be 200
    And the response should contain an empty list

  Scenario: Get notes when notes exist
    Given there are 3 existing notes in the system
    When I send a request to get all notes
    Then the response status code should be 200
    And the response should contain 3 notes
    And each note should have required fields
