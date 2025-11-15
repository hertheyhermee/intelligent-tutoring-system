# Geometry Tutor - Complete Guide

## Overview

The Intelligent Tutoring System has been specialized for teaching **geometry area calculations**. Students learn to calculate areas of four fundamental shapes:

1. **Squares** - Area = side × side
2. **Rectangles** - Area = length × width  
3. **Triangles** - Area = (base × height) ÷ 2
4. **Circles** - Area = π × radius²

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Web Interface
```bash
python run_web.py
```

### 3. Open Your Browser
Navigate to: **http://127.0.0.1:5000**

## How It Works

### Adaptive Learning Algorithm

The system implements intelligent adaptive learning:

**Knowledge Tracking**
- Each shape has a knowledge level from 0.0 to 1.0 (0% to 100%)
- Correct answers increase knowledge by 10%
- Incorrect answers decrease knowledge by 5%
- System recommends practicing shapes with lowest mastery

**Difficulty Progression**
- **Beginner** (0-39% knowledge): Whole numbers, smaller values
  - Square: side 3-10
  - Rectangle: length 4-10, width 3-8
  - Triangle: base 4-10, height 3-8
  - Circle: radius 3-8

- **Intermediate** (40-74% knowledge): Larger whole numbers
  - Square: side 10-25
  - Rectangle: length 10-30, width 8-20
  - Triangle: base 10-25, height 8-20
  - Circle: radius 8-15

- **Advanced** (75-100% knowledge): Decimal values
  - Square: side 5.5-20.5
  - Rectangle: length 8.5-25.5, width 5.5-18.5
  - Triangle: base 8.5-22.5, height 6.5-18.5
  - Circle: radius 5.5-18.5

## User Interface Features

### Welcome Page
- Simple name entry to begin
- Feature overview (shapes, progress tracking, adaptive learning)

### Dashboard
- Overall progress bar showing mastery across all shapes
- Recommended next topic based on lowest knowledge
- Individual shape cards with mastery percentages
- Quick access to practice any shape

### Practice Page
- Clear problem statement with parameters
- Difficulty badge (beginner/intermediate/advanced)
- Answer input with validation
- Hint button for guidance (shows formula)
- Formula reference panel for all shapes

### Result Page
- Visual feedback (✅ correct / ❌ incorrect)
- Comparison of user answer vs. correct answer
- Detailed explanation of the solution
- Updated knowledge level display
- Options to practice again or return to dashboard

### Progress Page
- Statistics dashboard:
  - Total problems solved
  - Number of correct answers
  - Overall accuracy percentage
- Knowledge breakdown by shape with progress bars
- Recent activity feed showing last 10 attempts

## Educational Design

### Learning Principles Applied

1. **Immediate Feedback**: Students receive instant results with explanations
2. **Mastery Learning**: Progress only when demonstrating understanding
3. **Scaffolding**: Hints available when students are stuck
4. **Spaced Practice**: Recommends weaker areas for additional practice
5. **Visual Progress**: Clear visualization motivates continued learning

### Problem Generation

Problems are generated randomly within difficulty-appropriate ranges:
- Ensures unique practice experience
- Prevents memorization
- Maintains engagement through variety
- Adapts to student's current skill level

### Assessment Strategy

The system uses a simple but effective assessment:
- Tolerance of 0.01 for floating-point comparisons
- Circle problems require rounding to 2 decimal places
- Focus on conceptual understanding rather than calculator precision

## Technical Architecture

### Backend Components

**Flask Application** (`web/app.py`)
- Routes for all user interactions
- Session management for state persistence
- In-memory student database (demo mode)

**Geometry Module** (`domains/geometry.py`)
- `GeometryTutor` class: Problem generation and validation
- `GeometryProblem` dataclass: Problem representation
- Difficulty-based problem generators for each shape

**Core Models** (`core/`)
- `Student`: Tracks knowledge, history, learning style
- Knowledge levels stored per shape (0.0-1.0)
- Performance history with timestamps

### Frontend Components

**Templates** (`web/templates/`)
- `base.html`: Common layout with navigation
- `index.html`: Welcome/login page
- `dashboard.html`: Main hub with progress and shape selection
- `practice.html`: Problem-solving interface
- `result.html`: Feedback and explanation page
- `progress.html`: Detailed statistics and history

**Styling** (`web/static/style.css`)
- Responsive design (mobile-friendly)
- Purple gradient theme (#667eea → #764ba2)
- Smooth animations and transitions
- Accessible color contrasts

## Future Enhancements

Planned features for future versions:

1. **Database Persistence**
   - SQLite integration for student data
   - Long-term progress tracking
   - Multiple session support

2. **Extended Content**
   - Complex shapes (trapezoid, parallelogram, ellipse)
   - 3D shapes (volume calculations)
   - Composite shapes

3. **Enhanced Analytics**
   - Learning curve visualization
   - Time-to-solve metrics
   - Common error patterns

4. **Social Features**
   - Leaderboards
   - Challenge friends
   - Share achievements

5. **Accessibility**
   - Screen reader support
   - Keyboard navigation
   - Multiple language support

## Running Tests

```bash
# Test geometry module
pytest tests/unit/ -k geometry

# Test web routes (when tests are added)
pytest tests/integration/ -k web

# Full test suite
pytest
```

## Troubleshooting

**Port Already in Use**
```bash
# Change port in run_web.py or use:
python -c "from src.intelligent_tutoring_system.web.app import run_server; run_server(port=5001)"
```

**Flask Not Installed**
```bash
pip install flask
```

**Import Errors**
```bash
# Make sure you're in the project root
cd /path/to/intelligent-tutoring-system
pip install -e .
```

## Credits

Built using:
- Python 3.8+
- Flask 3.0+
- Modern HTML5/CSS3
- Mathematical formulas from standard geometry curriculum

---

**Happy Learning! 📐**
