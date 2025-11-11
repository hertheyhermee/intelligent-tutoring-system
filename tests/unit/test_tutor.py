"""Unit tests for Tutor model."""

import pytest
from intelligent_tutoring_system.core.tutor import Tutor
from intelligent_tutoring_system.core.student import Student


def test_tutor_creation():
    """Test creating a new tutor."""
    tutor = Tutor(name="Dr. Smith", specialization=["mathematics", "physics"])
    assert tutor.name == "Dr. Smith"
    assert "mathematics" in tutor.specialization
    assert tutor.teaching_strategy == "adaptive"


def test_assess_student():
    """Test student assessment."""
    tutor = Tutor(name="Prof. Jones", specialization=["programming"])
    student = Student(name="Alice")
    student.update_knowledge("programming", 0.6)
    
    score = tutor.assess_student(student, "programming")
    assert score == 0.6


def test_generate_content_introductory():
    """Test content generation for beginner level."""
    tutor = Tutor(name="Dr. Lee", specialization=["physics"])
    student = Student(name="Bob")
    student.update_knowledge("physics", 0.2)
    
    content = tutor.generate_content(student, "physics")
    assert "Introductory" in content


def test_generate_content_intermediate():
    """Test content generation for intermediate level."""
    tutor = Tutor(name="Dr. Lee", specialization=["physics"])
    student = Student(name="Carol")
    student.update_knowledge("physics", 0.5)
    
    content = tutor.generate_content(student, "physics")
    assert "Intermediate" in content


def test_generate_content_advanced():
    """Test content generation for advanced level."""
    tutor = Tutor(name="Dr. Lee", specialization=["physics"])
    student = Student(name="Dave")
    student.update_knowledge("physics", 0.9)
    
    content = tutor.generate_content(student, "physics")
    assert "Advanced" in content


def test_provide_feedback_correct():
    """Test positive feedback for correct answer."""
    tutor = Tutor(name="Mrs. Wilson", specialization=["mathematics"])
    student = Student(name="Emma")
    
    feedback = tutor.provide_feedback(student, "42", correct=True)
    assert "Great" in feedback or "job" in feedback


def test_provide_feedback_incorrect():
    """Test corrective feedback for incorrect answer."""
    tutor = Tutor(name="Mrs. Wilson", specialization=["mathematics"])
    student = Student(name="Frank")
    
    feedback = tutor.provide_feedback(student, "wrong", correct=False)
    assert "review" in feedback or "Not quite" in feedback


def test_recommend_next_topic():
    """Test topic recommendation."""
    tutor = Tutor(name="Dr. Brown", specialization=["math", "science", "history"])
    student = Student(name="Grace")
    student.update_knowledge("math", 0.8)
    student.update_knowledge("science", 0.3)
    student.update_knowledge("history", 0.6)
    
    recommended = tutor.recommend_next_topic(student)
    assert recommended == "science"
