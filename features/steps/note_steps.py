from behave import given, when, then
from hamcrest import assert_that, equal_to, is_not, none
from factories.note_factory import NoteFactory
from pages.note_page import NotePage
import logging

# Create note steps
@given('the notes API is available')
def step_check_api_available(context):
    """Check if API is available"""
    if not hasattr(context, 'client'):
        from steps.api_client import APIClient
        context.client = APIClient()
    context.client.reset()

@given('I have valid note data with title "{title}" and content "{content}"')
def step_create_valid_note_data(context, title, content):
    """Create valid note data"""
    context.client.current_note_data = context.client.factory.create_valid_note(
        title=title, content=content
    )

@given('I have note data with title "{title}" and content "{content}"')
def step_create_note_data(context, title, content):
    """Create note data (could be invalid)"""
    context.client.current_note_data = {
        "title": title,
        "content": content
    }

@given('I have incomplete note data')
def step_create_incomplete_note_data(context):
    """Create incomplete note data"""
    context.client.current_note_data = context.client.factory.create_invalid_note("both")

@when('I send a request to create the note')
def step_send_create_request(context):
    """Send create note request"""
    context.client.response = context.client.note_page.create_note(
        context.client.current_note_data
    )
    if context.client.response.status_code == 201:
        note_data = context.client.response.json()
        context.client.current_note_id = note_data.get('id')
        context.client.created_notes.append(context.client.current_note_id)

# Get all notes steps
@given('there are no notes in the system')
def step_ensure_no_notes(context):
    """Ensure no notes exist"""
    context.client.note_page.cleanup_notes()

@given('there are {count:d} existing notes in the system')
def step_create_multiple_notes(context, count):
    """Create multiple notes"""
    notes = context.client.factory.create_bulk_notes(count)
    for note in notes:
        response = context.client.note_page.create_note(note)
        if response.status_code == 201:
            context.client.created_notes.append(response.json()['id'])

@when('I send a request to get all notes')
def step_get_all_notes(context):
    """Get all notes request"""
    context.client.response = context.client.note_page.get_all_notes()

# Get note by ID steps
@given('an existing note with title "{title}" and content "{content}"')
def step_create_existing_note(context, title, content):
    """Create a note that will be used for retrieval"""
    note_data = context.client.factory.create_valid_note(title, content)
    response = context.client.note_page.create_note(note_data)
    
    # Добавим отладку
    print(f"\nResponse status: {response.status_code}")
    print(f"Response body: {response.text}")
    
    assert response.status_code == 200 or response.status_code == 201, \
           f"Expected 200/201 but got {response.status_code}"
    
    context.client.current_note_data = response.json()
    context.client.current_note_id = context.client.current_note_data['id']
    context.client.created_notes.append(context.client.current_note_id)

@given('I have the note ID')
def step_get_note_id(context):
    """Store note ID from created note"""
    assert context.client.current_note_id is not None

@given('a non-existent note ID "{note_id}"')
def step_set_nonexistent_id(context, note_id):
    """Set a non-existent note ID"""
    context.client.current_note_id = int(note_id) if note_id.isdigit() else note_id

@given('an invalid note ID format "{note_id}"')
def step_set_invalid_id_format(context, note_id):
    """Set an invalid note ID format"""
    context.client.current_note_id = note_id

@when('I send a request to get the note by ID')
def step_get_note_by_id(context):
    """Get note by ID request"""
    context.client.response = context.client.note_page.get_note_by_id(
        context.client.current_note_id
    )

# Update note steps
@when('I update the note with title "{title}" and content "{content}"')
def step_update_note(context, title, content):
    """Update note request"""
    update_data = context.client.factory.create_valid_note(title, content)
    context.client.response = context.client.note_page.update_note(
        context.client.current_note_id, update_data
    )

# Delete note steps
@when('I send a request to delete the note')
def step_delete_note(context):
    """Delete note request"""
    context.client.response = context.client.note_page.delete_note(
        context.client.current_note_id
    )
    if context.client.current_note_id in context.client.created_notes:
        context.client.created_notes.remove(context.client.current_note_id)

# Then steps - assertions
@then('the response status code should be {code:d}')
def step_check_status_code(context, code):
    """Check response status code"""
    assert_that(context.client.response.status_code, equal_to(code))

@then('the response should contain the correct title "{title}"')
def step_check_response_title(context, title):
    """Check response contains correct title"""
    response_data = context.client.response.json()
    assert_that(response_data.get('title'), equal_to(title))

@then('the response should contain the correct content "{content}"')
def step_check_response_content(context, content):
    """Check response contains correct content"""
    response_data = context.client.response.json()
    assert_that(response_data.get('content'), equal_to(content))

@then('the response should contain the correct note details')
def step_check_note_details(context):
    """Check note details match"""
    response_data = context.client.response.json()
    assert_that(response_data.get('id'), equal_to(context.client.current_note_id))
    assert_that(response_data.get('title'), is_not(none()))
    assert_that(response_data.get('content'), is_not(none()))

@then('the response should contain an empty list')
def step_check_empty_list(context):
    """Check response contains empty list"""
    assert_that(context.client.response.json(), equal_to([]))

@then('the response should contain {count:d} notes')
def step_check_notes_count(context, count):
    """Check number of notes in response"""
    assert_that(len(context.client.response.json()), equal_to(count))

@then('each note should have required fields')
def step_check_notes_fields(context):
    """Check each note has required fields"""
    notes = context.client.response.json()
    for note in notes:
        assert_that(note.get('id'), is_not(none()))
        assert_that(note.get('title'), is_not(none()))
        assert_that(note.get('content'), is_not(none()))

@then('the error message should indicate "{message}"')
def step_check_error_message(context, message):
    """Check error message contains expected text"""
    error_data = context.client.response.json()
    
    # FastAPI может возвращать ошибку в разных форматах
    error_msg = ""
    if isinstance(error_data, dict):
        error_msg = error_data.get('message', '') or \
                    error_data.get('detail', '') or \
                    error_data.get('error', '') or \
                    str(error_data)
    else:
        error_msg = str(error_data)
    
    assert message.lower() in error_msg.lower(), \
           f"Expected '{message}' in '{error_msg}'"

@then('the note should be updated with the new values')
def step_check_note_updated(context):
    """Verify note was updated"""
    response_data = context.client.response.json()
    assert_that(response_data.get('title'), is_not(none()))
    assert_that(response_data.get('content'), is_not(none()))

@then('the note should no longer exist in the system')
def step_check_note_deleted(context):
    """Verify note no longer exists"""
    response = context.client.note_page.get_note_by_id(context.client.current_note_id)
    assert_that(response.status_code, equal_to(404))

@then('the note should not be created')
def step_check_note_not_created(context):
    """Verify note was not created"""
    assert_that(context.client.current_note_id, equal_to(None))

@given('I have note data with title "" and content "Some content"')
def step_impl_empty_title(context):
    """Step for empty title"""
    context.client.current_note_data = {
        "title": "",
        "content": "Some content"
    }

@given('I have note data with title "Empty Note" and content ""')
def step_impl_empty_content(context):
    """Step for empty content"""
    context.client.current_note_data = {
        "title": "Empty Note",
        "content": ""
    }

@when('I update the note with title "" and content "Updated content"')
def step_impl_update_empty_title(context):
    """Step for updating with empty title"""
    update_data = {
        "title": "",
        "content": "Updated content"
    }
    context.client.response = context.client.note_page.update_note(
        context.client.current_note_id, update_data
    )
@then('the response should contain a note with id')
def step_check_note_has_id(context):
    """Check that response contains an ID"""
    response_data = context.client.response.json()
    assert 'id' in response_data, f"Response has no 'id' field: {response_data}"
    assert response_data['id'] is not None

@then('the note should have empty title')
def step_check_empty_title(context):
    """Check that note has empty title"""
    response_data = context.client.response.json()
    assert response_data.get('title') == "", f"Expected empty title, got: {response_data.get('title')}"

@then('the response should contain the correct title ""')
def step_check_empty_title_response(context):
    """Check response contains empty title"""
    response_data = context.client.response.json()
    assert_that(response_data.get('title'), equal_to(""))

@then('the response should contain the correct content ""')
def step_check_empty_content_response(context):
    """Check response contains empty content"""
    response_data = context.client.response.json()
    assert_that(response_data.get('content'), equal_to(""))