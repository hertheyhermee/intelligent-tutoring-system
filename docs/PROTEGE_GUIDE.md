# Protégé Ontology Development Guide

## Introduction

This guide explains how the OWL ontology for the Geometry Intelligent Tutoring System was created using Protégé, and how to extend or modify it.

## What is Protégé?

Protégé is a free, open-source ontology editor developed by Stanford University. It provides a graphical interface for creating and editing OWL (Web Ontology Language) ontologies.

**Download**: https://protege.stanford.edu/

## Opening the Ontology

1. **Launch Protégé**
2. **File → Open** 
3. Navigate to: `intelligent-tutoring-system/ontology/geometry_tutor_ontology.owl`
4. The ontology will load with all classes, properties, and individuals visible

## Ontology Structure Overview

### Classes Tab

The Classes tab shows the hierarchy of concepts:

```
Thing
├── Shape
│   └── TwoDimensionalShape
│       ├── Polygon
│       │   ├── Quadrilateral (Square, Rectangle)
│       │   └── Triangle
│       └── Circle
├── Formula
│   └── AreaFormula
├── Problem
│   └── AreaProblem
├── DifficultyLevel
│   ├── Beginner
│   ├── Intermediate
│   └── Advanced
└── Student
```

### Object Properties

Object properties define relationships between classes:

| Property | Domain | Range | Purpose |
|----------|--------|-------|---------|
| hasFormula | Shape | AreaFormula | Links shapes to formulas |
| hasDifficulty | Problem | DifficultyLevel | Assigns difficulty |
| aboutShape | Problem | Shape | Problem's subject |
| solves | Student | Problem | Tracks attempts |
| hasKnowledgeOf | Student | Shape | Student knowledge |

### Data Properties

Data properties define attributes:

| Property | Domain | Range | Purpose |
|----------|--------|-------|---------|
| formulaExpression | AreaFormula | string | Math expression |
| formulaDescription | AreaFormula | string | Natural language |
| numberOfSides | Polygon | integer | Polygon sides |
| knowledgeLevel | Student | float | Mastery (0.0-1.0) |
| studentName | Student | string | Student ID |
| problemText | Problem | string | Question |
| correctAnswer | Problem | float | Solution |
| hintText | Problem | string | Help text |

### Individuals

Individuals are specific instances:

**Shapes**:
- SquareShape
- RectangleShape
- TriangleShape
- CircleShape

**Formulas**:
- SquareAreaFormula
- RectangleAreaFormula
- TriangleAreaFormula
- CircleAreaFormula

**Difficulty Levels**:
- BeginnerLevel
- IntermediateLevel
- AdvancedLevel

## How to Edit the Ontology

### Adding a New Shape Class

1. **Select Classes Tab**
2. **Click on "TwoDimensionalShape"**
3. **Click the "Add subclass" button** (looks like a plus icon)
4. **Enter class name** (e.g., "Pentagon")
5. **Add annotations**:
   - Click "+" next to Annotations
   - Select "rdfs:comment"
   - Enter description: "A polygon with five sides"
6. **Click OK**

### Adding a New Shape Instance

1. **Select Individuals Tab**
2. **Click the class** (e.g., "Pentagon")
3. **Click "Add individual"**
4. **Name it** (e.g., "PentagonShape")
5. **Add properties**:
   - In Property assertions section
   - Click "+" next to Object property assertions
   - Select "hasFormula"
   - Click "..." and select or create formula individual

### Creating a New Formula Individual

1. **Individuals Tab**
2. **Select "AreaFormula" class**
3. **Add individual** named "PentagonAreaFormula"
4. **Add data properties**:
   - Click "+" in Data property assertions
   - Select "formulaExpression"
   - Enter: "0.25 * numberOfSides * sideLength^2 * cot(pi/numberOfSides)"
   - Click "+" again for "formulaDescription"
   - Enter: "Area of regular pentagon using side length"

### Adding Object Properties

1. **Object Properties Tab**
2. **Click "Add property" button**
3. **Enter property name** (e.g., "hasPrerequisite")
4. **Set domain**: Select applicable class
5. **Set range**: Select target class
6. **Add annotations** for documentation

### Adding Data Properties

1. **Data Properties Tab**
2. **Click "Add property"**
3. **Enter name** (e.g., "difficultyScore")
4. **Set domain**: DifficultyLevel
5. **Set range**: xsd:integer
6. **Add functional characteristic** if property has single value

## Running the Reasoner

### Purpose
Reasoners check consistency and infer new facts

### Steps
1. **Reasoner → HermiT** (or Pellet)
2. **Start reasoner**
3. **Check for inconsistencies**
   - Red highlighting indicates problems
   - Fix any issues reported
4. **View inferred class hierarchy**
   - Switch between "Asserted" and "Inferred" views

### Common Issues
- **Unsatisfiable classes**: Domain/range conflicts
- **Inconsistent individuals**: Violate class restrictions
- **Property chain issues**: Circular dependencies

## Validation Checklist

Before saving changes:

✓ All classes have rdfs:comment annotations  
✓ All properties have domain and range defined  
✓ All individuals have required properties  
✓ Reasoner completes without errors  
✓ Class hierarchy is logical  
✓ Naming conventions are consistent  

## Exporting the Ontology

### As OWL/XML (Recommended)
1. **File → Save as...**
2. **Select "RDF/XML" format**
3. **Save with .owl extension**

### As Other Formats
- **Turtle (.ttl)**: More readable text format
- **N-Triples (.nt)**: Line-based format
- **JSON-LD**: JSON representation

## Integration with Python Code

After editing the ontology:

1. **Save the OWL file** in `ontology/` directory
2. **Restart the Python application** to reload ontology
3. **Test changes**:
```bash
python -c "from src.intelligent_tutoring_system.utils.ontology_manager import get_ontology_manager; om = get_ontology_manager(); print(om.get_ontology_stats())"
```

## Best Practices

### Naming Conventions
- **Classes**: PascalCase (e.g., TwoDimensionalShape)
- **Individuals**: PascalCase with descriptive suffix (e.g., SquareShape)
- **Properties**: camelCase (e.g., hasFormula, formulaExpression)

### Documentation
- Always add rdfs:comment for classes
- Use rdfs:label for human-readable names
- Document property purposes

### Modularity
- Group related classes
- Use clear hierarchies
- Avoid deep nesting (max 4-5 levels)

### Consistency
- Uniform naming patterns
- Consistent property usage
- Standard data types

## Common Protégé Operations

### Search
- **Ctrl+F** (Cmd+F on Mac): Search entities
- Filter by name, annotation, or type

### Visualization
- **Window → Tabs → OntoGraf**: Visualize ontology
- Drag classes to see relationships
- Export as image

### Metrics
- **Tools → Metrics**: View ontology statistics
- Class count, property count, axiom count

### SPARQL Queries
- **Window → Tabs → SPARQL Query**: Run queries
- Example:
```sparql
SELECT ?shape ?formula
WHERE {
    ?shape rdf:type :Shape .
    ?shape :hasFormula ?formula .
}
```

## Troubleshooting

### Protégé Won't Open File
- **Check file format**: Must be valid OWL/XML
- **Verify namespace**: Ensure IRI is accessible
- **Look for XML syntax errors**

### Reasoner Errors
- **Check domain/range**: Ensure properties have correct types
- **Verify individual types**: Individuals must be instances of declared classes
- **Review restrictions**: Check for contradicting class restrictions

### Changes Not Reflected in Python
- **Restart application**: Ontology is cached
- **Check file path**: Ensure correct file location
- **Verify owlready2**: Confirm library can read OWL file

## Advanced Features

### Restrictions
Define class characteristics:
- **existential**: Must have at least one
- **universal**: All must be of type
- **cardinality**: Exact number required

### Equivalent Classes
Define alternative definitions:
```
Rectangle ≡ Quadrilateral AND hasRightAngles value 4
```

### Disjoint Classes
Classes cannot overlap:
```
Square DisjointWith Circle
```

### Property Chains
Derive new relationships:
```
aboutShape ∘ hasFormula → requiresFormula
```

## Resources

**Official Documentation**:
- https://protege.stanford.edu/doc/users.html
- https://www.w3.org/TR/owl2-overview/

**Tutorials**:
- Pizza Ontology Tutorial (classic introduction)
- Stanford Protégé Wiki
- OWL 2 Web Ontology Language Primer

**Community**:
- Protégé User Mailing List
- Stack Overflow (tag: protege)

## Conclusion

Protégé provides powerful tools for ontology development. This guide covers the essentials for working with the Geometry Tutor ontology. As you become more comfortable, explore advanced features like SWRL rules, ontology versioning, and integration with other semantic web tools.

The key to effective ontology development is iterative refinement: start simple, test frequently, and expand carefully based on system needs.
