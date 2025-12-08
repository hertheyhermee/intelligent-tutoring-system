# Ontology Integration Guide

## Overview

The Intelligent Tutoring System now uses an **OWL (Web Ontology Language) ontology** to structure geometric knowledge and validate learning content. The ontology provides a formal representation of shapes, formulas, difficulty levels, and their relationships.

## What is the Ontology?

The ontology file (`ontology/geometry_tutor_ontology.owl`) defines:

- **Classes**: Shape hierarchies (Shape → TwoDimensionalShape → Square, Rectangle, Triangle, Circle)
- **Individuals**: Specific instances (SquareShape, BeginnerLevel, SquareAreaFormula, etc.)
- **Properties**: Relationships (hasFormula, hasDifficulty, aboutShape, solves)
- **Data Properties**: Attributes (formulaExpression, formulaDescription, numberOfSides, etc.)

## How It Works

### 1. Ontology Structure

```
Shape (Abstract)
├── TwoDimensionalShape
    ├── Polygon
    │   ├── Quadrilateral
    │   │   ├── Square
    │   │   └── Rectangle
    │   └── Triangle
    └── Circle

DifficultyLevel
├── Beginner
├── Intermediate
└── Advanced

Formula
└── AreaFormula (for each shape)
```

### 2. Integration Points

#### a) **GeometryTutor** (`domains/geometry.py`)

```python
from ..utils.ontology_manager import get_ontology_manager

class GeometryTutor:
    def __init__(self):
        self.ontology_manager = get_ontology_manager()
        
        # Validates shapes against ontology
        ontology_shapes = self.ontology_manager.get_all_shapes()
        
    def generate_problem(self, shape, difficulty):
        # Validates problem configuration
        self.ontology_manager.validate_problem(shape, difficulty)
        
        # Can fetch formulas from ontology
        formula_info = self.ontology_manager.get_shape_formula(shape)
```

#### b) **Web Application** (`web/app.py`)

```python
from ..utils.ontology_manager import get_ontology_manager

ontology_manager = get_ontology_manager()

@app.route('/dashboard')
def dashboard():
    # Provides ontology stats to dashboard
    ontology_stats = ontology_manager.get_ontology_stats()
    return render_template('dashboard.html', ontology_stats=ontology_stats)
```

#### c) **Dashboard UI** (`web/templates/dashboard.html`)

Displays:
- Number of ontology classes
- Number of individuals
- Number of properties
- Description of ontology usage

### 3. Available Features

#### OntologyManager Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `get_all_shapes()` | Retrieves all shape names | `List[str]` |
| `get_difficulty_levels()` | Retrieves all difficulty levels | `List[str]` |
| `get_shape_formula(shape)` | Gets formula for a shape | `Dict` with 'expression' and 'description' |
| `get_shape_properties(shape)` | Gets properties of a shape | `Dict` with shape metadata |
| `validate_problem(shape, difficulty)` | Validates problem configuration | `bool` |
| `get_ontology_stats()` | Gets ontology statistics | `Dict` with counts |

## Current Effects on the System

### ✅ Active Features

1. **Validation**: Every problem generation validates shapes and difficulties against the ontology
2. **Formula Access**: Formulas can be queried from ontology (expressions and descriptions)
3. **Dashboard Display**: Ontology statistics shown on student dashboard
4. **Logging**: System logs ontology loading status and validation results
5. **Graceful Fallback**: If ontology fails to load, system continues with hardcoded defaults

### 🔄 What Happens at Runtime

When you start the application:

1. **Startup**: OntologyManager loads the OWL file
2. **GeometryTutor Init**: Fetches shapes from ontology, logs success/failure
3. **Problem Generation**: Validates shape+difficulty combinations
4. **Dashboard Load**: Queries ontology stats (classes, individuals, properties)
5. **Formula Queries**: Can fetch formula expressions from ontology

### 📊 Visible Evidence

1. **Console Logs**: 
   ```
   INFO: Ontology loaded successfully with shapes: ['square', 'rectangle', 'triangle', 'circle']
   ```

2. **Dashboard UI**: 
   - New "🧠 Knowledge Base (Ontology)" section
   - Shows: 17 Classes, 11 Individuals, 13 Properties

3. **Problem Validation**:
   ```
   WARNING: Problem configuration (hexagon, beginner) not validated by ontology
   ```

## Testing the Integration

Run the test script:

```bash
python test_ontology_integration.py
```

This will show:
- Ontology loading status
- Available shapes and difficulties
- Formulas for each shape
- Shape properties
- Validation results
- Sample problem generation

## Editing the Ontology

### Using Protégé

1. Download [Protégé](https://protege.stanford.edu/) (ontology editor)
2. Open `ontology/geometry_tutor_ontology.owl`
3. Edit classes, individuals, or properties
4. Save the file
5. Restart the application - changes are automatically loaded

### Adding a New Shape

1. In Protégé, create a new **Individual** under the appropriate class
2. Add a **hasFormula** relationship to an AreaFormula individual
3. Set **formulaExpression** and **formulaDescription** data properties
4. Save the ontology
5. Update `GeometryTutor.SHAPES` list in code

## Future Enhancements

Potential expansions of ontology usage:

- **Dynamic Hint Generation**: Use formula descriptions from ontology in hints
- **Adaptive Content**: Query difficulty thresholds from ontology
- **Learning Paths**: Define prerequisite relationships between shapes
- **Problem Templates**: Store problem patterns in ontology
- **Student Modeling**: Use ontology to classify student knowledge states
- **Reasoning**: Enable ontology reasoning to infer relationships

## Troubleshooting

### Ontology Not Loading

Check logs for:
```
WARNING: Ontology not available or empty, using default configuration
```

**Solutions:**
- Verify `ontology/geometry_tutor_ontology.owl` exists
- Ensure `owlready2` is installed: `pip install owlready2`
- Check file permissions

### SQLite Warning

If you see:
```
Warning: SQLite3 version 3.40.0 and 3.41.2 have huge performance regressions
```

This is a warning from owlready2 about SQLite versions. It doesn't affect functionality, but you can upgrade SQLite to 3.42+ to remove it.

## Dependencies

- **owlready2** (>=0.41): Python library for OWL ontology manipulation
- **rdflib**: RDF graph library (dependency of owlready2)

Install with:
```bash
pip install -r requirements.txt
```

## Architecture Diagram

```
┌─────────────────────────────────────────┐
│   Geometry Tutor Web Application        │
├─────────────────────────────────────────┤
│  Flask Routes (app.py)                  │
│    ↓ uses                               │
│  GeometryTutor (domains/geometry.py)    │
│    ↓ uses                               │
│  OntologyManager (utils/ontology_       │
│                   manager.py)           │
│    ↓ loads                              │
│  geometry_tutor_ontology.owl            │
│    (OWL/RDF ontology file)              │
└─────────────────────────────────────────┘
```

## Summary

The OWL ontology now serves as the **semantic foundation** of your tutoring system:

- ✅ Structures geometric knowledge formally
- ✅ Validates shapes and difficulty levels  
- ✅ Provides formula definitions
- ✅ Enables knowledge queries
- ✅ Visible in dashboard UI
- ✅ Graceful fallback if unavailable

The system is **production-ready** with full ontology integration!
