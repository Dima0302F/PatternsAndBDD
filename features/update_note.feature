Feature: Update Note
  As a user
  I want to update existing notes
  So that I can correct or improve my notes

  Background:
    Given the notes API is available

  Scenario: Successfully update note with valid ID
    Given an existing note with title "Original" and content "Original content"
    And I have the note ID
    When I update the note with title "Updated" and content "Updated content"
    Then the response status code should be 200
    And the note should be updated with the new values

  Scenario: Fail to update note with invalid ID
    Given a non-existent note ID "99999"
    When I update the note with title "Updated" and content "Updated content"
    Then the response status code should be 404
    And the error message should indicate "Note not found"

  Scenario: Fail to update note with invalid data
    Given an existing note with title "Original" and content "Original content"
    And I have the note ID
    When I update the note with title "" and content "Updated content"
    Then the response status code should be 400
