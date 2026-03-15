Feature: Create Note
  As a user
  I want to create notes
  So that I can store my thoughts

  Background:
    Given the notes API is available

  Scenario: Successfully create a note with valid data
    Given I have valid note data with title "Shopping List" and content "Milk, Bread, Eggs"
    When I send a request to create the note
    Then the response status code should be 200
    And the response should contain the correct title "Shopping List"
    And the response should contain the correct content "Milk, Bread, Eggs"

    Scenario: Fail to create a note with empty title
    Given the notes API is available
    Given I have note data with title "" and content "Some content"
    When I send a request to create the note
    Then the response status code should be 200
    And the response should contain the correct title ""

  Scenario: Fail to create a note with empty content
    Given the notes API is available
    Given I have note data with title "Empty Note" and content ""
    When I send a request to create the note
    Then the response status code should be 200
    And the response should contain the correct content ""

  Scenario: Fail to create a note with missing fields
    Given the notes API is available
    Given I have incomplete note data
    When I send a request to create the note
    Then the response status code should be 200