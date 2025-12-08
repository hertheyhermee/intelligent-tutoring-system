"""Flask web application for Intelligent Tutoring System."""

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from datetime import datetime
import secrets
from pathlib import Path

from ..core.student import Student
from ..domains.geometry import GeometryTutor, GeometryProblem
from ..utils.ontology_manager import get_ontology_manager


app = Flask(__name__, 
            template_folder=str(Path(__file__).parent / 'templates'),
            static_folder=str(Path(__file__).parent / 'static'))
app.secret_key = secrets.token_hex(16)

# Global storage for demo purposes (in production, use a database)
students_db = {}
geometry_tutor = GeometryTutor()
ontology_manager = get_ontology_manager()


@app.route('/')
def index():
    """Home page - student login/registration."""
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    """Register a new student."""
    student_name = request.form.get('name', '').strip()
    
    if not student_name:
        return render_template('index.html', error="Please enter your name")
    
    # Create new student
    student = Student(name=student_name)
    
    # Initialize geometry knowledge for all shapes
    for shape in GeometryTutor.SHAPES:
        student.knowledge_level[shape] = 0.0
    
    students_db[str(student.id)] = student
    session['student_id'] = str(student.id)
    
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    """Student dashboard showing progress and options."""
    student_id = session.get('student_id')
    
    if not student_id or student_id not in students_db:
        return redirect(url_for('index'))
    
    student = students_db[student_id]
    
    # Calculate overall progress
    if student.knowledge_level:
        avg_knowledge = sum(student.knowledge_level.values()) / len(student.knowledge_level)
        progress_percentage = int(avg_knowledge * 100)
    else:
        progress_percentage = 0
    
    # Get recommended shape
    recommended_shape = geometry_tutor.recommend_next_shape(student.knowledge_level)
    
    # Get ontology stats
    ontology_stats = ontology_manager.get_ontology_stats()
    
    return render_template('dashboard.html', 
                         student=student, 
                         progress_percentage=progress_percentage,
                         recommended_shape=recommended_shape,
                         shapes=GeometryTutor.SHAPES,
                         ontology_stats=ontology_stats)


@app.route('/practice/<shape>')
@app.route('/practice/<shape>/<mode>')
def practice(shape, mode='calculate'):
    """Start practicing a specific shape with chosen mode.
    
    Modes:
    - calculate: Standard problem (given dimensions, calculate area)
    - multiple_choice: Choose correct answer from options
    - custom_input: Enter your own dimensions
    """
    student_id = session.get('student_id')
    
    if not student_id or student_id not in students_db:
        return redirect(url_for('index'))
    
    if shape not in GeometryTutor.SHAPES:
        return redirect(url_for('dashboard'))
    
    student = students_db[student_id]
    
    # Get student's knowledge level for this shape
    knowledge_level = student.knowledge_level.get(shape, 0.0)
    difficulty = geometry_tutor.get_difficulty_for_knowledge_level(knowledge_level)
    
    # Generate problem with specified mode
    problem = geometry_tutor.generate_problem_with_mode(shape, difficulty, mode)
    
    # Store problem in session with enhanced data
    session['current_problem'] = {
        'shape': problem.shape,
        'parameters': problem.parameters,
        'question': problem.question,
        'correct_answer': problem.correct_answer,
        'difficulty': problem.difficulty,
        'hint': problem.hint,
        'explanation': problem.explanation,
        'problem_type': problem.problem_type,
        'choices': problem.choices,
        'step_by_step': problem.step_by_step,
        'learning_tips': problem.learning_tips,
        'formula_breakdown': problem.formula_breakdown
    }
    
    return render_template('practice.html', 
                         student=student,
                         problem=problem,
                         show_hint=False,
                         mode=mode)


@app.route('/calculate_custom', methods=['POST'])
def calculate_custom():
    """Calculate area from user-provided dimensions."""
    student_id = session.get('student_id')
    
    if not student_id or student_id not in students_db:
        return redirect(url_for('index'))
    
    student = students_db[student_id]
    problem_data = session.get('current_problem')
    
    if not problem_data:
        return redirect(url_for('dashboard'))
    
    shape = problem_data['shape']
    
    # Extract user-provided dimensions
    user_params = {}
    try:
        if shape == 'square':
            user_params['side'] = float(request.form.get('side', 0))
        elif shape == 'rectangle':
            user_params['length'] = float(request.form.get('length', 0))
            user_params['width'] = float(request.form.get('width', 0))
        elif shape == 'triangle':
            user_params['base'] = float(request.form.get('base', 0))
            user_params['height'] = float(request.form.get('height', 0))
        elif shape == 'circle':
            user_params['radius'] = float(request.form.get('radius', 0))
    except ValueError:
        error_msg = "Please enter valid numbers for all dimensions"
        problem = geometry_tutor.generate_problem_with_mode(shape, 'beginner', 'custom_input')
        return render_template('practice.html', student=student, problem=problem, error=error_msg, mode='custom_input')
    
    # Calculate area and get full solution
    area, problem = geometry_tutor.calculate_custom_area(shape, user_params)
    
    # Update session
    session['current_problem'] = {
        'shape': problem.shape,
        'parameters': problem.parameters,
        'question': problem.question,
        'correct_answer': problem.correct_answer,
        'difficulty': problem.difficulty,
        'hint': problem.hint,
        'explanation': problem.explanation,
        'problem_type': problem.problem_type,
        'step_by_step': problem.step_by_step,
        'learning_tips': problem.learning_tips,
        'formula_breakdown': problem.formula_breakdown
    }
    
    # Record this as a practice attempt
    student.add_performance_record({
        'shape': shape,
        'difficulty': 'custom',
        'correct': True,  # Custom input is always "correct" - it's a learning tool
        'answer': area,
        'expected': area,
        'mode': 'custom_input'
    })
    
    # Update knowledge slightly
    current_knowledge = student.knowledge_level.get(shape, 0.0)
    new_knowledge = min(1.0, current_knowledge + 0.05)
    student.update_knowledge(shape, new_knowledge)
    
    return render_template('result.html',
                         student=student,
                         problem=problem,
                         user_answer=area,
                         is_correct=True,
                         feedback="Great! Here's your calculated area with detailed explanation.",
                         show_detailed_solution=True)


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    """Submit an answer to the current problem."""
    student_id = session.get('student_id')
    
    if not student_id or student_id not in students_db:
        return redirect(url_for('index'))
    
    student = students_db[student_id]
    problem_data = session.get('current_problem')
    
    if not problem_data:
        return redirect(url_for('dashboard'))
    
    problem_type = problem_data.get('problem_type', 'calculate')
    
    # Handle multiple choice differently
    if problem_type == 'multiple_choice':
        try:
            user_answer = float(request.form.get('answer', 0))
        except ValueError:
            error_msg = "Please select an answer"
            problem = GeometryProblem(
                shape=problem_data['shape'],
                parameters=problem_data['parameters'],
                question=problem_data['question'],
                correct_answer=problem_data['correct_answer'],
                difficulty=problem_data['difficulty'],
                hint=problem_data['hint'],
                explanation=problem_data['explanation'],
                problem_type=problem_type,
                choices=problem_data['choices']
            )
            return render_template('practice.html', student=student, problem=problem, error=error_msg, mode='multiple_choice')
    else:
        # Standard calculate mode
        try:
            user_answer = float(request.form.get('answer', 0))
        except ValueError:
            error_msg = "Please enter a valid number"
            problem = GeometryProblem(
                shape=problem_data['shape'],
                parameters=problem_data['parameters'],
                question=problem_data['question'],
                correct_answer=problem_data['correct_answer'],
                difficulty=problem_data['difficulty'],
                hint=problem_data['hint'],
                explanation=problem_data['explanation'],
                problem_type=problem_type
            )
            return render_template('practice.html', student=student, problem=problem, error=error_msg, mode='calculate')
    
    # Recreate full problem object with all data
    problem = GeometryProblem(
        shape=problem_data['shape'],
        parameters=problem_data['parameters'],
        question=problem_data['question'],
        correct_answer=problem_data['correct_answer'],
        difficulty=problem_data['difficulty'],
        hint=problem_data['hint'],
        explanation=problem_data['explanation'],
        problem_type=problem_type,
        choices=problem_data.get('choices'),
        step_by_step=problem_data.get('step_by_step'),
        learning_tips=problem_data.get('learning_tips'),
        formula_breakdown=problem_data.get('formula_breakdown')
    )
    
    # Check answer
    is_correct, feedback = geometry_tutor.check_answer(problem, user_answer)
    
    # Update student knowledge
    current_knowledge = student.knowledge_level.get(problem.shape, 0.0)
    
    if is_correct:
        # Increase knowledge
        new_knowledge = min(1.0, current_knowledge + 0.1)
    else:
        # Slightly decrease knowledge
        new_knowledge = max(0.0, current_knowledge - 0.05)
    
    student.update_knowledge(problem.shape, new_knowledge)
    
    # Add performance record
    student.add_performance_record({
        'shape': problem.shape,
        'difficulty': problem.difficulty,
        'correct': is_correct,
        'answer': user_answer,
        'expected': problem.correct_answer
    })
    
    return render_template('result.html',
                         student=student,
                         problem=problem,
                         user_answer=user_answer,
                         is_correct=is_correct,
                         feedback=feedback)


@app.route('/hint')
def hint():
    """Show hint for current problem."""
    student_id = session.get('student_id')
    
    if not student_id or student_id not in students_db:
        return redirect(url_for('index'))
    
    student = students_db[student_id]
    problem_data = session.get('current_problem')
    
    if not problem_data:
        return redirect(url_for('dashboard'))
    
    problem = GeometryProblem(
        shape=problem_data['shape'],
        parameters=problem_data['parameters'],
        question=problem_data['question'],
        correct_answer=problem_data['correct_answer'],
        difficulty=problem_data['difficulty'],
        hint=problem_data['hint'],
        explanation=problem_data['explanation']
    )
    
    return render_template('practice.html', 
                         student=student,
                         problem=problem,
                         show_hint=True)


@app.route('/progress')
def progress():
    """Show detailed progress page."""
    student_id = session.get('student_id')
    
    if not student_id or student_id not in students_db:
        return redirect(url_for('index'))
    
    student = students_db[student_id]
    
    # Calculate statistics
    total_problems = len(student.performance_history)
    correct_problems = sum(1 for record in student.performance_history if record.get('correct', False))
    accuracy = int((correct_problems / total_problems * 100)) if total_problems > 0 else 0
    
    return render_template('progress.html',
                         student=student,
                         total_problems=total_problems,
                         correct_problems=correct_problems,
                         accuracy=accuracy,
                         shapes=GeometryTutor.SHAPES)


@app.route('/logout')
def logout():
    """Logout current student."""
    session.clear()
    return redirect(url_for('index'))


def run_server(host='127.0.0.1', port=5000, debug=True):
    """Run the Flask development server."""
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_server()
