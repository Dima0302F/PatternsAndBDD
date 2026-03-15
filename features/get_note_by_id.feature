Feature: Get Note by ID
  As a user
  I want to retrieve a specific note by its ID
  So that I can view its details

  Background:
    Given the notes API is available

  Scenario: Get note by valid ID
    Given an existing note with title "Meeting Notes" and content "Discuss project timeline"
    And I have the note ID
    When I send a request to get the note by ID
    Then the response status code should be 200
    And the response should contain the correct note details

  Scenario: Get note by invalid ID (non-existent)
    Given a non-existent note ID "99999"
    When I send a request to get the note by ID
    Then the response status code should be 404
    And the error message should indicate "Note not found"

  Scenario: Get note by invalid ID (malformed)
    Given an invalid note ID format "abc123"
    When I send a request to get the note by ID
    Then the response status code should be 400
