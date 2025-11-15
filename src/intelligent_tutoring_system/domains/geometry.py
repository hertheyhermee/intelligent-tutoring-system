"""Geometry domain module for teaching area calculations."""

import random
import math
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class GeometryProblem:
    """Represents a geometry problem for calculating areas."""
    
    shape: str
    parameters: Dict[str, float]
    question: str
    correct_answer: float
    difficulty: str  # 'beginner', 'intermediate', 'advanced'
    hint: str
    explanation: str


class GeometryTutor:
    """Specialized tutor for teaching geometry area calculations."""
    
    SHAPES = ['square', 'rectangle', 'triangle', 'circle']
    
    def __init__(self):
        """Initialize the geometry tutor."""
        self.current_problem: Optional[GeometryProblem] = None
    
    def generate_problem(self, shape: str, difficulty: str = 'beginner') -> GeometryProblem:
        """Generate a geometry problem based on shape and difficulty.
        
        Args:
            shape: Shape type (square, rectangle, triangle, circle)
            difficulty: Problem difficulty level
            
        Returns:
            GeometryProblem instance
        """
        if shape == 'square':
            return self._generate_square_problem(difficulty)
        elif shape == 'rectangle':
            return self._generate_rectangle_problem(difficulty)
        elif shape == 'triangle':
            return self._generate_triangle_problem(difficulty)
        elif shape == 'circle':
            return self._generate_circle_problem(difficulty)
        else:
            raise ValueError(f"Unknown shape: {shape}")
    
    def _generate_square_problem(self, difficulty: str) -> GeometryProblem:
        """Generate a square area problem."""
        if difficulty == 'beginner':
            side = random.randint(3, 10)
        elif difficulty == 'intermediate':
            side = random.randint(10, 25)
        else:  # advanced
            side = round(random.uniform(5.5, 20.5), 1)
        
        area = side * side
        
        return GeometryProblem(
            shape='square',
            parameters={'side': side},
            question=f"What is the area of a square with side length {side} units?",
            correct_answer=area,
            difficulty=difficulty,
            hint="Remember: Area of a square = side × side",
            explanation=f"The area of a square is calculated by multiplying the side by itself. "
                       f"Area = {side} × {side} = {area} square units."
        )
    
    def _generate_rectangle_problem(self, difficulty: str) -> GeometryProblem:
        """Generate a rectangle area problem."""
        if difficulty == 'beginner':
            length = random.randint(4, 10)
            width = random.randint(3, 8)
        elif difficulty == 'intermediate':
            length = random.randint(10, 30)
            width = random.randint(8, 20)
        else:  # advanced
            length = round(random.uniform(8.5, 25.5), 1)
            width = round(random.uniform(5.5, 18.5), 1)
        
        area = length * width
        
        return GeometryProblem(
            shape='rectangle',
            parameters={'length': length, 'width': width},
            question=f"What is the area of a rectangle with length {length} units and width {width} units?",
            correct_answer=area,
            difficulty=difficulty,
            hint="Remember: Area of a rectangle = length × width",
            explanation=f"The area of a rectangle is calculated by multiplying length by width. "
                       f"Area = {length} × {width} = {area} square units."
        )
    
    def _generate_triangle_problem(self, difficulty: str) -> GeometryProblem:
        """Generate a triangle area problem."""
        if difficulty == 'beginner':
            base = random.randint(4, 10)
            height = random.randint(3, 8)
        elif difficulty == 'intermediate':
            base = random.randint(10, 25)
            height = random.randint(8, 20)
        else:  # advanced
            base = round(random.uniform(8.5, 22.5), 1)
            height = round(random.uniform(6.5, 18.5), 1)
        
        area = 0.5 * base * height
        
        return GeometryProblem(
            shape='triangle',
            parameters={'base': base, 'height': height},
            question=f"What is the area of a triangle with base {base} units and height {height} units?",
            correct_answer=area,
            difficulty=difficulty,
            hint="Remember: Area of a triangle = (base × height) ÷ 2",
            explanation=f"The area of a triangle is calculated as half the product of base and height. "
                       f"Area = (1/2) × {base} × {height} = {area} square units."
        )
    
    def _generate_circle_problem(self, difficulty: str) -> GeometryProblem:
        """Generate a circle area problem."""
        if difficulty == 'beginner':
            radius = random.randint(3, 8)
        elif difficulty == 'intermediate':
            radius = random.randint(8, 15)
        else:  # advanced
            radius = round(random.uniform(5.5, 18.5), 1)
        
        area = round(math.pi * radius * radius, 2)
        
        return GeometryProblem(
            shape='circle',
            parameters={'radius': radius},
            question=f"What is the area of a circle with radius {radius} units? (Round to 2 decimal places)",
            correct_answer=area,
            difficulty=difficulty,
            hint="Remember: Area of a circle = π × radius²  (use π ≈ 3.14159)",
            explanation=f"The area of a circle is calculated using π times radius squared. "
                       f"Area = π × {radius}² = π × {radius * radius} ≈ {area} square units."
        )
    
    def check_answer(self, problem: GeometryProblem, user_answer: float, tolerance: float = 0.01) -> Tuple[bool, str]:
        """Check if the user's answer is correct.
        
        Args:
            problem: The geometry problem
            user_answer: User's submitted answer
            tolerance: Acceptable difference from correct answer
            
        Returns:
            Tuple of (is_correct, feedback_message)
        """
        difference = abs(user_answer - problem.correct_answer)
        is_correct = difference <= tolerance
        
        if is_correct:
            return True, "Excellent! Your answer is correct! 🎉"
        else:
            return False, f"Not quite right. The correct answer is {problem.correct_answer}."
    
    def get_difficulty_for_knowledge_level(self, knowledge_level: float) -> str:
        """Determine problem difficulty based on student's knowledge level.
        
        Args:
            knowledge_level: Student's knowledge level (0.0 to 1.0)
            
        Returns:
            Difficulty level string
        """
        if knowledge_level < 0.4:
            return 'beginner'
        elif knowledge_level < 0.75:
            return 'intermediate'
        else:
            return 'advanced'
    
    def recommend_next_shape(self, student_knowledge: Dict[str, float]) -> str:
        """Recommend the next shape to practice based on student's knowledge.
        
        Args:
            student_knowledge: Dictionary of shape -> knowledge level
            
        Returns:
            Recommended shape name
        """
        # Find shape with lowest knowledge level
        if not student_knowledge:
            return 'square'  # Start with squares
        
        sorted_shapes = sorted(student_knowledge.items(), key=lambda x: x[1])
        return sorted_shapes[0][0]
