"""Geometry domain module for teaching area calculations."""

import random
import math
import logging
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass, field

from ..utils.ontology_manager import get_ontology_manager


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
    problem_type: str = 'calculate'  # 'calculate', 'multiple_choice', 'custom_input'
    choices: Optional[List[Dict]] = None  # For multiple choice: [{'text': '...', 'value': ..., 'is_correct': bool}]
    step_by_step: Optional[List[str]] = None  # Detailed solution steps
    learning_tips: Optional[List[str]] = None  # Additional learning tips
    formula_breakdown: Optional[Dict[str, str]] = None  # Formula components explained


class GeometryTutor:
    """Specialized tutor for teaching geometry area calculations."""
    
    SHAPES = ['square', 'rectangle', 'triangle', 'circle']
    
    def __init__(self):
        """Initialize the geometry tutor with ontology support."""
        self.current_problem: Optional[GeometryProblem] = None
        self.ontology_manager = get_ontology_manager()
        
        # Try to load shapes from ontology
        ontology_shapes = self.ontology_manager.get_all_shapes()
        if ontology_shapes and len(ontology_shapes) > 0:
            logging.info(f"Ontology loaded successfully with shapes: {ontology_shapes}")
        else:
            logging.warning("Ontology not available or empty, using default configuration")
    
    def generate_problem(self, shape: str, difficulty: str = 'beginner') -> GeometryProblem:
        """Generate a geometry problem based on shape and difficulty.
        
        Args:
            shape: Shape type (square, rectangle, triangle, circle)
            difficulty: Problem difficulty level
            
        Returns:
            GeometryProblem instance
        """
        # Validate problem configuration against ontology
        if not self.ontology_manager.validate_problem(shape, difficulty):
            logging.warning(f"Problem configuration ({shape}, {difficulty}) not validated by ontology")
        
        # Try to get formula from ontology
        formula_info = self.ontology_manager.get_shape_formula(shape)
        if formula_info:
            logging.debug(f"Using ontology formula for {shape}: {formula_info['expression']}")
        
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
    
    def generate_problem_with_mode(self, shape: str, difficulty: str, problem_type: str = 'calculate') -> GeometryProblem:
        """Generate a problem with specified interaction mode.
        
        Args:
            shape: Shape type
            difficulty: Difficulty level
            problem_type: 'calculate', 'multiple_choice', or 'custom_input'
            
        Returns:
            Enhanced GeometryProblem with mode-specific features
        """
        # Generate base problem
        base_problem = self.generate_problem(shape, difficulty)
        
        # Add enhanced tutoring content
        base_problem = self._add_enhanced_tutoring(base_problem)
        
        # Modify based on problem type
        if problem_type == 'multiple_choice':
            return self._convert_to_multiple_choice(base_problem)
        elif problem_type == 'custom_input':
            return self._prepare_custom_input_mode(base_problem)
        else:
            base_problem.problem_type = 'calculate'
            return base_problem
    
    def _add_enhanced_tutoring(self, problem: GeometryProblem) -> GeometryProblem:
        """Add detailed tutoring content to a problem."""
        # Generate step-by-step solution
        problem.step_by_step = self._generate_solution_steps(problem)
        
        # Add learning tips
        problem.learning_tips = self._generate_learning_tips(problem)
        
        # Add formula breakdown
        problem.formula_breakdown = self._generate_formula_breakdown(problem)
        
        return problem
    
    def _generate_solution_steps(self, problem: GeometryProblem) -> List[str]:
        """Generate step-by-step solution for a problem."""
        steps = []
        shape = problem.shape
        params = problem.parameters
        
        if shape == 'square':
            side = params['side']
            steps = [
                f"Step 1: Identify the given information - Side length = {side} units",
                f"Step 2: Recall the formula - Area = side × side (or side²)",
                f"Step 3: Substitute the values - Area = {side} × {side}",
                f"Step 4: Calculate - Area = {problem.correct_answer} square units"
            ]
        elif shape == 'rectangle':
            length = params['length']
            width = params['width']
            steps = [
                f"Step 1: Identify the given information - Length = {length} units, Width = {width} units",
                f"Step 2: Recall the formula - Area = length × width",
                f"Step 3: Substitute the values - Area = {length} × {width}",
                f"Step 4: Calculate - Area = {problem.correct_answer} square units"
            ]
        elif shape == 'triangle':
            base = params['base']
            height = params['height']
            steps = [
                f"Step 1: Identify the given information - Base = {base} units, Height = {height} units",
                f"Step 2: Recall the formula - Area = (base × height) ÷ 2",
                f"Step 3: Calculate base × height - {base} × {height} = {base * height}",
                f"Step 4: Divide by 2 - {base * height} ÷ 2 = {problem.correct_answer} square units"
            ]
        elif shape == 'circle':
            radius = params['radius']
            steps = [
                f"Step 1: Identify the given information - Radius = {radius} units",
                f"Step 2: Recall the formula - Area = π × radius²",
                f"Step 3: Calculate radius² - {radius}² = {radius * radius}",
                f"Step 4: Multiply by π - {radius * radius} × π ≈ {problem.correct_answer} square units"
            ]
        
        return steps
    
    def _generate_learning_tips(self, problem: GeometryProblem) -> List[str]:
        """Generate helpful learning tips for a shape."""
        tips = []
        shape = problem.shape
        
        if shape == 'square':
            tips = [
                "💡 A square has all four sides equal, so you only need one measurement",
                "📐 The area represents how many unit squares fit inside the shape",
                "✏️ Remember: Area is always in square units (units²)",
                "🎯 Quick check: The area should be larger than the side length (unless side < 1)"
            ]
        elif shape == 'rectangle':
            tips = [
                "💡 A rectangle has two pairs of equal sides - length and width",
                "📐 Think of area as rows times columns in a grid",
                "✏️ Length × Width works regardless of orientation",
                "🎯 A square is a special rectangle where length = width"
            ]
        elif shape == 'triangle':
            tips = [
                "💡 The base can be any side, but height must be perpendicular to it",
                "📐 Triangles have half the area of a rectangle with same base and height",
                "✏️ The ÷ 2 in the formula accounts for the triangular shape",
                "🎯 Height is measured at a right angle (90°) to the base"
            ]
        elif shape == 'circle':
            tips = [
                "💡 π (pi) is approximately 3.14159 - it's the ratio of circumference to diameter",
                "📐 Radius is half the diameter (distance across the circle)",
                "✏️ Squaring the radius (r²) means multiplying it by itself",
                "🎯 Circle areas grow quickly - double the radius means 4× the area!"
            ]
        
        return tips
    
    def _generate_formula_breakdown(self, problem: GeometryProblem) -> Dict[str, str]:
        """Generate detailed formula breakdown."""
        shape = problem.shape
        
        if shape == 'square':
            return {
                'formula': 'Area = side × side',
                'alternative': 'Area = side² (side squared)',
                'why': 'A square has equal sides, so we multiply the side by itself',
                'units': 'square units (units²)'
            }
        elif shape == 'rectangle':
            return {
                'formula': 'Area = length × width',
                'alternative': 'Area = base × height',
                'why': 'Area equals the number of unit squares that fit inside',
                'units': 'square units (units²)'
            }
        elif shape == 'triangle':
            return {
                'formula': 'Area = (base × height) ÷ 2',
                'alternative': 'Area = ½ × base × height',
                'why': 'A triangle is half of a rectangle with the same base and height',
                'units': 'square units (units²)'
            }
        elif shape == 'circle':
            return {
                'formula': 'Area = π × radius²',
                'alternative': 'Area = π × r × r',
                'why': 'π relates the radius to the area of a circle',
                'units': 'square units (units²)'
            }
        return {}
    
    def _convert_to_multiple_choice(self, problem: GeometryProblem) -> GeometryProblem:
        """Convert problem to multiple choice format."""
        problem.problem_type = 'multiple_choice'
        correct = problem.correct_answer
        
        # Generate distractors (wrong answers)
        distractors = self._generate_distractors(correct, problem.shape)
        
        # Create choices
        choices = [{'text': f"{correct}", 'value': correct, 'is_correct': True}]
        for dist in distractors:
            choices.append({'text': f"{dist}", 'value': dist, 'is_correct': False})
        
        # Shuffle choices
        random.shuffle(choices)
        problem.choices = choices
        
        # Update question to indicate multiple choice
        problem.question += " (Select the correct answer)"
        
        return problem
    
    def _generate_distractors(self, correct: float, shape: str) -> List[float]:
        """Generate plausible wrong answers for multiple choice."""
        distractors = []
        
        # Common mistakes:
        # 1. Forgot to square/multiply
        # 2. Used wrong formula
        # 3. Calculation error
        
        # Distractor 1: Off by a common factor
        distractors.append(round(correct * 0.5, 2))
        
        # Distractor 2: Off by addition instead of multiplication
        distractors.append(round(correct * 1.5, 2))
        
        # Distractor 3: Close but not exact
        distractors.append(round(correct + correct * 0.1, 2))
        
        return distractors
    
    def _prepare_custom_input_mode(self, problem: GeometryProblem) -> GeometryProblem:
        """Prepare problem for custom input mode."""
        problem.problem_type = 'custom_input'
        problem.question = f"Enter your own dimensions for a {problem.shape} to calculate its area:"
        
        # Clear the specific parameters - user will provide their own
        problem.parameters = {}
        problem.correct_answer = 0  # Will be calculated from user input
        
        return problem
    
    def calculate_custom_area(self, shape: str, user_params: Dict[str, float]) -> Tuple[float, GeometryProblem]:
        """Calculate area from user-provided dimensions.
        
        Args:
            shape: Shape type
            user_params: User-provided dimensions
            
        Returns:
            Tuple of (calculated_area, problem_with_solution)
        """
        area = 0
        difficulty = 'beginner'  # Default for custom
        
        if shape == 'square':
            side = user_params.get('side', 0)
            area = side * side
            problem = GeometryProblem(
                shape='square',
                parameters={'side': side},
                question=f"Calculate the area of a square with side {side} units",
                correct_answer=area,
                difficulty=difficulty,
                hint="Area = side × side",
                explanation=f"Area = {side} × {side} = {area} square units",
                problem_type='custom_input'
            )
        elif shape == 'rectangle':
            length = user_params.get('length', 0)
            width = user_params.get('width', 0)
            area = length * width
            problem = GeometryProblem(
                shape='rectangle',
                parameters={'length': length, 'width': width},
                question=f"Calculate the area of a rectangle with length {length} and width {width}",
                correct_answer=area,
                difficulty=difficulty,
                hint="Area = length × width",
                explanation=f"Area = {length} × {width} = {area} square units",
                problem_type='custom_input'
            )
        elif shape == 'triangle':
            base = user_params.get('base', 0)
            height = user_params.get('height', 0)
            area = 0.5 * base * height
            problem = GeometryProblem(
                shape='triangle',
                parameters={'base': base, 'height': height},
                question=f"Calculate the area of a triangle with base {base} and height {height}",
                correct_answer=area,
                difficulty=difficulty,
                hint="Area = (base × height) ÷ 2",
                explanation=f"Area = (1/2) × {base} × {height} = {area} square units",
                problem_type='custom_input'
            )
        elif shape == 'circle':
            radius = user_params.get('radius', 0)
            area = round(math.pi * radius * radius, 2)
            problem = GeometryProblem(
                shape='circle',
                parameters={'radius': radius},
                question=f"Calculate the area of a circle with radius {radius}",
                correct_answer=area,
                difficulty=difficulty,
                hint="Area = π × radius²",
                explanation=f"Area = π × {radius}² ≈ {area} square units",
                problem_type='custom_input'
            )
        else:
            raise ValueError(f"Unknown shape: {shape}")
        
        # Add enhanced tutoring
        problem = self._add_enhanced_tutoring(problem)
        
        return area, problem
