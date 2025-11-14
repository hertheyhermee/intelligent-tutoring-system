# Geometry Tutor - Web Interface

A web-based intelligent tutoring system for teaching geometry area calculations.

## Features

- **Interactive Learning**: Practice calculating areas of squares, rectangles, triangles, and circles
- **Adaptive Difficulty**: Problems automatically adjust to your skill level (beginner, intermediate, advanced)
- **Progress Tracking**: Monitor your learning progress with visual dashboards
- **Instant Feedback**: Get immediate feedback with explanations for each problem
- **Hints System**: Request hints when you need help
- **Performance Analytics**: View detailed statistics and recent activity

## Running the Web Interface

### Option 1: Quick Start (Recommended)
```bash
python run_web.py
```

### Option 2: Using the CLI
```bash
python -m intelligent_tutoring_system --mode server
```

### Option 3: Direct Module Import
```bash
python -c "from src.intelligent_tutoring_system.web.app import run_server; run_server()"
```

Then open your browser and navigate to: **http://127.0.0.1:5000**

## How to Use

1. **Start Learning**: Enter your name on the welcome page
2. **Choose a Shape**: Select a shape to practice from the dashboard
3. **Solve Problems**: Calculate the area and submit your answer
4. **Get Feedback**: See if you're correct with detailed explanations
5. **Track Progress**: View your knowledge levels and statistics

## Educational Approach

The system uses adaptive learning principles:

- **Knowledge Tracking**: Maintains a 0-100% mastery level for each shape
- **Difficulty Progression**: 
  - Beginner (0-39%): Simple whole numbers
  - Intermediate (40-74%): Larger numbers
  - Advanced (75-100%): Decimal values
- **Smart Recommendations**: Suggests practicing shapes with lowest mastery
- **Immediate Reinforcement**: Correct answers increase knowledge, incorrect answers provide learning opportunities

## Shapes Covered

1. **Square**: Area = side × side
2. **Rectangle**: Area = length × width
3. **Triangle**: Area = (base × height) ÷ 2
4. **Circle**: Area = π × radius²

## Technical Details

- **Framework**: Flask 3.0+
- **Frontend**: HTML5, CSS3 (responsive design)
- **Session Management**: Flask sessions for user state
- **Data Storage**: In-memory (for demo; database integration planned)
