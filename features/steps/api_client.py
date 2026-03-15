from pages.note_page import NotePage
from factories.note_factory import NoteFactory
from behave import fixture
import requests

class APIClient:
    """API Client to manage test state"""
    
    def __init__(self):
        self.note_page = NotePage()
        self.factory = NoteFactory()
        self.response = None
        self.current_note_data = None
        self.current_note_id = None
        self.created_notes = []
    
    def reset(self):
        """Reset client state"""
        self.response = None
        self.current_note_data = None
        self.current_note_id = None
    
    def cleanup(self):
        """Clean up created notes"""
        for note_id in self.created_notes:
            try:
                self.note_page.delete_note(note_id)
            except:
                pass
        self.created_notes.clear()

@fixture
def api_client(context):
    """Fixture to create API client"""
    context.client = APIClient()
    yield context.client
    context.client.cleanup()
