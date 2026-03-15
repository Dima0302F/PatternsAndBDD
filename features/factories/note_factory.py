import random
import string
from typing import Dict, Optional

class NoteFactory:
    """Factory pattern for generating test notes"""
    
    @staticmethod
    def create_valid_note(title: Optional[str] = None, 
                          content: Optional[str] = None) -> Dict:
        """Create a valid note with random or specified data"""
        return {
            "title": title or NoteFactory._generate_random_title(),
            "content": content or NoteFactory._generate_random_content()
        }
    
    @staticmethod
    def create_invalid_note(missing_field: Optional[str] = None) -> Dict:
        """Create an invalid note"""
        note = NoteFactory.create_valid_note()
        if missing_field == "title":
            note["title"] = ""
        elif missing_field == "content":
            note["content"] = ""
        elif missing_field == "both":
            note["title"] = ""
            note["content"] = ""
        return note
    
    @staticmethod
    def create_note_with_long_content() -> Dict:
        """Create a note with very long content"""
        return {
            "title": "Long Note",
            "content": "A" * 10000
        }
    
    @staticmethod
    def create_bulk_notes(count: int) -> list:
        """Create multiple notes"""
        return [NoteFactory.create_valid_note() for _ in range(count)]
    
    @staticmethod
    def _generate_random_title(length: int = 10) -> str:
        """Generate random title"""
        words = ["Meeting", "Shopping", "Idea", "Task", "Reminder", 
                "Project", "Goal", "Note", "Thought", "Plan"]
        return random.choice(words) + " " + ''.join(random.choices(string.ascii_uppercase, k=3))
    
    @staticmethod
    def _generate_random_content(length: int = 50) -> str:
        """Generate random content"""
        return ''.join(random.choices(string.ascii_letters + string.digits + " ", k=length))
