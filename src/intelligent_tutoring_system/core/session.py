"""Tutoring session management."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from .student import Student
from .tutor import Tutor


@dataclass
class TutoringSession:
    """Represents a tutoring session between a student and tutor."""
    
    id: UUID = field(default_factory=uuid4)
    student: Optional[Student] = None
    tutor: Optional[Tutor] = None
    topic: str = ""
    started_at: datetime = field(default_factory=datetime.now)
    ended_at: Optional[datetime] = None
    interactions: List[dict] = field(default_factory=list)
    
    def start(self, student: Student, tutor: Tutor, topic: str):
        """Start a tutoring session.
        
        Args:
            student: Student participating
            tutor: Tutor conducting the session
            topic: Topic to cover
        """
        self.student = student
        self.tutor = tutor
        self.topic = topic
        self.started_at = datetime.now()
        
        self.add_interaction({
            "type": "session_start",
            "topic": topic,
            "initial_level": student.get_knowledge(topic)
        })
    
    def add_interaction(self, interaction: dict):
        """Add an interaction to the session.
        
        Args:
            interaction: Interaction data
        """
        interaction["timestamp"] = datetime.now()
        self.interactions.append(interaction)
    
    def end(self):
        """End the tutoring session."""
        self.ended_at = datetime.now()
        
        if self.student and self.topic:
            self.add_interaction({
                "type": "session_end",
                "final_level": self.student.get_knowledge(self.topic),
                "duration": (self.ended_at - self.started_at).total_seconds()
            })
    
    def get_duration(self) -> float:
        """Get session duration in seconds.
        
        Returns:
            Duration in seconds
        """
        end_time = self.ended_at or datetime.now()
        return (end_time - self.started_at).total_seconds()
