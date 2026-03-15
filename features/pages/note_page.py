import requests
from typing import Dict, List, Optional, Any

class NotePage:
    """Page Object pattern for Notes API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def create_note(self, note_data: Dict) -> requests.Response:
        """Create a new note"""
        response = self.session.post(
            f"{self.base_url}/notes",
            json=note_data
        )
        return response
    
    def get_all_notes(self) -> requests.Response:
        """Get all notes"""
        response = self.session.get(f"{self.base_url}/notes")
        return response
    
    def get_note_by_id(self, note_id: int) -> requests.Response:
        """Get a specific note by ID"""
        response = self.session.get(f"{self.base_url}/notes/{note_id}")
        return response
    
    def update_note(self, note_id: int, note_data: Dict) -> requests.Response:
        """Update a note"""
        response = self.session.put(
            f"{self.base_url}/notes/{note_id}",
            json=note_data
        )
        return response
    
    def delete_note(self, note_id: int) -> requests.Response:
        """Delete a note"""
        response = self.session.delete(f"{self.base_url}/notes/{note_id}")
        return response
    
    def verify_note_exists(self, note_id: int) -> bool:
        """Check if a note exists"""
        response = self.get_note_by_id(note_id)
        return response.status_code == 200
    
    def cleanup_notes(self) -> None:
        """Delete all notes (cleanup after tests)"""
        response = self.get_all_notes()
        if response.status_code == 200:
            notes = response.json()
            for note in notes:
                self.delete_note(note['id'])
