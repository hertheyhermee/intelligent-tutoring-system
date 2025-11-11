"""
Intelligent Tutoring System

An adaptive learning platform that personalizes educational content
and provides intelligent feedback to students.
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .core.tutor import Tutor
from .core.student import Student
from .core.session import TutoringSession

__all__ = ["Tutor", "Student", "TutoringSession"]
