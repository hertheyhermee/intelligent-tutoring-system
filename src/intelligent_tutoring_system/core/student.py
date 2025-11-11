"""Student model for tracking learner progress and characteristics."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4


@dataclass
class Student:
    """Represents a student in the tutoring system."""
    
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    knowledge_level: Dict[str, float] = field(default_factory=dict)
    learning_style: Optional[str] = None
    performance_history: List[Dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)
    
    def update_knowledge(self, topic: str, level: float):
        """Update knowledge level for a specific topic.
        
        Args:
            topic: Topic identifier
            level: Knowledge level (0.0 to 1.0)
        """
        if not 0.0 <= level <= 1.0:
            raise ValueError("Knowledge level must be between 0.0 and 1.0")
        
        self.knowledge_level[topic] = level
        self.last_active = datetime.now()
    
    def get_knowledge(self, topic: str) -> float:
        """Get knowledge level for a specific topic.
        
        Args:
            topic: Topic identifier
            
        Returns:
            Knowledge level (0.0 if not found)
        """
        return self.knowledge_level.get(topic, 0.0)
    
    def add_performance_record(self, record: Dict):
        """Add a performance record.
        
        Args:
            record: Performance data dictionary
        """
        record["timestamp"] = datetime.now()
        self.performance_history.append(record)
        self.last_active = datetime.now()
