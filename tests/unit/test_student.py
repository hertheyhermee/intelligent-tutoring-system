"""Unit tests for Student model."""

import pytest
from datetime import datetime
from intelligent_tutoring_system.core.student import Student


def test_student_creation():
    """Test creating a new student."""
    student = Student(name="John Doe")
    assert student.name == "John Doe"
    assert isinstance(student.created_at, datetime)
    assert len(student.knowledge_level) == 0


def test_update_knowledge():
    """Test updating student knowledge level."""
    student = Student(name="Jane Smith")
    student.update_knowledge("mathematics", 0.75)
    assert student.get_knowledge("mathematics") == 0.75


def test_update_knowledge_invalid_level():
    """Test that invalid knowledge levels raise error."""
    student = Student(name="Bob")
    with pytest.raises(ValueError):
        student.update_knowledge("physics", 1.5)
    with pytest.raises(ValueError):
        student.update_knowledge("physics", -0.1)


def test_get_knowledge_nonexistent():
    """Test getting knowledge for topic that hasn't been learned."""
    student = Student(name="Alice")
    assert student.get_knowledge("chemistry") == 0.0


def test_add_performance_record():
    """Test adding performance records."""
    student = Student(name="Charlie")
    record = {"topic": "programming", "score": 0.85}
    student.add_performance_record(record)
    
    assert len(student.performance_history) == 1
    assert "timestamp" in student.performance_history[0]
    assert student.performance_history[0]["topic"] == "programming"
