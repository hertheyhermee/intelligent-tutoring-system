"""Tutor model for providing intelligent instruction and feedback."""

from dataclasses import dataclass
from typing import List, Optional

from .student import Student


@dataclass
class Tutor:
    """Represents an intelligent tutor in the system."""
    
    name: str
    specialization: List[str]
    teaching_strategy: str = "adaptive"
    
    def assess_student(self, student: Student, topic: str) -> float:
        """Assess a student's knowledge level on a topic.
        
        Args:
            student: Student to assess
            topic: Topic to assess
            
        Returns:
            Assessment score (0.0 to 1.0)
        """
        return student.get_knowledge(topic)
    
    def generate_content(self, student: Student, topic: str) -> str:
        """Generate personalized learning content for a student.
        
        Args:
            student: Student to generate content for
            topic: Topic to teach
            
        Returns:
            Generated content
        """
        level = self.assess_student(student, topic)
        
        if level < 0.3:
            return f"Introductory content for {topic}"
        elif level < 0.7:
            return f"Intermediate content for {topic}"
        else:
            return f"Advanced content for {topic}"
    
    def provide_feedback(self, student: Student, response: str, correct: bool) -> str:
        """Provide feedback on a student's response.
        
        Args:
            student: Student who responded
            response: Student's response
            correct: Whether response was correct
            
        Returns:
            Feedback message
        """
        if correct:
            return "Great job! Your understanding is improving."
        else:
            return "Not quite right. Let's review the concept together."
    
    def recommend_next_topic(self, student: Student) -> Optional[str]:
        """Recommend the next topic for a student to learn.
        
        Args:
            student: Student to recommend for
            
        Returns:
            Recommended topic or None
        """
        if not student.knowledge_level:
            return self.specialization[0] if self.specialization else None
        
        # Find topics with lowest knowledge levels
        sorted_topics = sorted(
            student.knowledge_level.items(),
            key=lambda x: x[1]
        )
        
        return sorted_topics[0][0] if sorted_topics else None
