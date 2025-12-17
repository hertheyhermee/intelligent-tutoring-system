# ITS Ontology

This directory contains the ontology (knowledge representation) for the Intelligent Tutoring System.

## Files

- **`its-ontology.owl`** - The main ontology file in RDF/XML format
- **`PROTEGE_GUIDE.md`** - Comprehensive guide for working with the ontology in Protégé
- **`README.md`** - This file

## Quick Start

### Opening in Protégé

1. Install Protégé: https://protege.stanford.edu/
2. Launch Protégé
3. Open `its-ontology.owl`

### Using in Python

```python
from intelligent_tutoring_system.utils.ontology_manager import get_ontology_manager

om = get_ontology_manager()
om.load_ontology('ontology/its-ontology.owl')

# Query shapes
shapes = om.get_all_shapes()
```

## Ontology Structure

### Core Classes (23 total)

**Agents**
- `Agent` → `Student`, `Tutor` → `GeometryTutor`

**Sessions**
- `Session` → `TutoringSession`

**Content**
- `Content` → `Problem` → `GeometryProblem`
- `Content` → `Topic`, `Interaction`

**Knowledge**
- `KnowledgeComponent` → `KnowledgeLevel`, `LearningStyle`, `TeachingStrategy`

**Geometry**
- `GeometricEntity` → `Shape` → `Square`, `Rectangle`, `Triangle`, `Circle`
- `Formula` → `AreaFormula`

**Assessment**
- `Assessment` → `PerformanceRecord`, `Answer`

### Key Relationships (14 Object Properties)

- `hasStudent` / `participatesIn` (session ↔ student)
- `hasTutor` / `conductsSession` (session ↔ tutor)
- `focusesOnTopic` (session → topic)
- `hasKnowledge` (student → knowledge level)
- `hasShape` (geometry problem → shape)
- `usesFormula` (problem → formula)
- And more...

### Data Properties (36 total)

Student: `studentID`, `studentName`, `createdAt`, `lastActive`  
Problem: `questionText`, `correctAnswer`, `difficulty`, `hint`  
Shape: `shapeName`, `side`, `length`, `width`, `base`, `height`, `radius`  
Session: `sessionID`, `startTime`, `endTime`, `duration`  
And more...

## Documentation

See **`PROTEGE_GUIDE.md`** for:
- Step-by-step Protégé usage
- Creating individuals
- Running reasoners
- DL and SPARQL queries
- Visualization techniques
- Integration with Python
- Best practices
- Troubleshooting

## IRI

**Ontology IRI**: `http://www.semanticweb.org/its/intelligent-tutoring-system`  
**Version**: 1.0.0

## License

Part of the Intelligent Tutoring System project.
