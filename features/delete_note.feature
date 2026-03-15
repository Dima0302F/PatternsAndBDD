Feature: Delete Note
  As a user
  I want to delete notes
  So that I can remove unwanted content

  Background:
    Given the notes API is available

    Scenario: Successfully delete note with valid ID
    Given the notes API is available
    Given an existing note with title "To Delete" and content "This will be deleted"
    And I have the note ID
    When I send a request to delete the note
    Then the response status code should be 200
    And the note should no longer exist in the system

  Scenario: Fail to delete note with invalid ID (non-existent)
    Given a non-existent note ID "99999"
    When I send a request to delete the note
    Then the response status code should be 404
    And the error message should indicate "Note not found"

  Scenario: Fail to delete note with invalid ID (malformed)
    Given an invalid note ID format "xyz"
    When I send a request to delete the note
    Then the response status code should be 422
