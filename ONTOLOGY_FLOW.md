# Ontology Integration Flow Diagram

## System Architecture with Ontology

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERACTION                              │
│                   (Web Browser)                                  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ HTTP Request
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FLASK WEB APPLICATION                          │
│                    (web/app.py)                                  │
│                                                                  │
│  @app.route('/dashboard')                                        │
│  def dashboard():                                                │
│      ontology_stats = ontology_manager.get_ontology_stats() ◄──┐│
│      return render_template(..., ontology_stats=ontology_stats)││
│                                                                  ││
│  @app.route('/practice/<shape>')                                ││
│  def practice(shape):                                           ││
│      problem = geometry_tutor.generate_problem(shape, diff) ◄──┐││
│      return render_template('practice.html', problem=problem)  │││
└──────────────────────────────────────────────────────────────┬─┘││
                                                                │  ││
                    ┌───────────────────────────────────────────┘  ││
                    │                                               ││
                    ▼                                               ││
┌─────────────────────────────────────────────────────────────┐   ││
│              GEOMETRY TUTOR                                  │   ││
│           (domains/geometry.py)                              │   ││
│                                                              │   ││
│  class GeometryTutor:                                        │   ││
│      def __init__(self):                                     │   ││
│          self.ontology_manager = get_ontology_manager() ────────┘│
│                                                              │    │
│      def generate_problem(self, shape, difficulty):         │    │
│          # Validate against ontology                        │    │
│          if not self.ontology_manager.validate_problem(): ──────┐│
│              log warning                                    │    ││
│                                                             │    ││
│          # Optionally get formula from ontology            │    ││
│          formula = self.ontology_manager.get_shape_formula()────┤│
│                                                             │    ││
│          return GeometryProblem(...)                        │    ││
└─────────────────────────────────────────────────────────────┘    ││
                                                                    ││
                    ┌───────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                 ONTOLOGY MANAGER                                 │
│            (utils/ontology_manager.py)                           │
│                                                                  │
│  class OntologyManager:                                          │
│      def __init__(self, ontology_path):                          │
│          self.ontology = get_ontology(path).load() ───────┐     │
│          self.namespace = ontology.get_namespace()        │     │
│                                                           │     │
│      def get_all_shapes(self) -> List[str]:              │     │
│          # Query shape individuals from ontology         │     │
│          return ['square', 'rectangle', 'triangle', ...]  │     │
│                                                           │     │
│      def get_shape_formula(self, shape) -> Dict:         │     │
│          # Query hasFormula relationships                │     │
│          return {'expression': '...', 'description': ...} │     │
│                                                           │     │
│      def validate_problem(self, shape, difficulty):      │     │
│          # Check if shape and difficulty exist           │     │
│          return shape in shapes and diff in difficulties  │     │
│                                                           │     │
│      def get_ontology_stats(self) -> Dict:               │     │
│          # Count classes, individuals, properties        │     │
│          return {'classes': 17, 'individuals': 11, ...}   │     │
└───────────────────────────────────────────────────────────┬─────┘
                                                            │
                                                            │ loads
                                                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OWL ONTOLOGY FILE                             │
│          (ontology/geometry_tutor_ontology.owl)                  │
│                                                                  │
│  <?xml version="1.0"?>                                           │
│  <rdf:RDF xmlns:owl="http://www.w3.org/2002/07/owl#">          │
│                                                                  │
│  Classes:                                                        │
│    - Shape (abstract)                                            │
│    - TwoDimensionalShape                                         │
│    - Square, Rectangle, Triangle, Circle                         │
│    - DifficultyLevel (Beginner, Intermediate, Advanced)          │
│    - AreaFormula                                                 │
│                                                                  │
│  Individuals:                                                    │
│    - SquareShape (type: Square)                                  │
│    - RectangleShape (type: Rectangle)                            │
│    - TriangleShape (type: Triangle)                              │
│    - CircleShape (type: Circle)                                  │
│    - SquareAreaFormula (type: AreaFormula)                       │
│    - BeginnerLevel, IntermediateLevel, AdvancedLevel             │
│                                                                  │
│  Object Properties:                                              │
│    - hasFormula (Shape → AreaFormula)                            │
│    - hasDifficulty (Problem → DifficultyLevel)                   │
│    - aboutShape (Problem → Shape)                                │
│                                                                  │
│  Data Properties:                                                │
│    - formulaExpression (string)                                  │
│    - formulaDescription (string)                                 │
│    - numberOfSides (integer)                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Example: Student Practices Circle

```
1. Student clicks "Practice Circle" button
   └─> HTTP GET /practice/circle

2. Flask route practice(shape='circle')
   └─> Calls: geometry_tutor.generate_problem('circle', 'beginner')

3. GeometryTutor.generate_problem()
   ├─> Validates: ontology_manager.validate_problem('circle', 'beginner')
   │   └─> OntologyManager queries OWL: "Does CircleShape exist?"
   │       └─> Returns: True ✓
   │
   ├─> Gets formula: ontology_manager.get_shape_formula('circle')
   │   └─> OntologyManager queries OWL:
   │       - Find CircleShape individual
   │       - Follow hasFormula relationship
   │       - Get formulaExpression and formulaDescription
   │       └─> Returns: {'expression': 'pi * radius * radius',
   │                      'description': 'Area of a circle equals...'}
   │
   └─> Generates problem with random values
       └─> Returns: GeometryProblem(shape='circle', ...)

4. Flask renders practice.html with problem
   └─> Browser displays problem to student
```

## Dashboard Display Flow

```
1. Student visits Dashboard
   └─> HTTP GET /dashboard

2. Flask route dashboard()
   └─> Calls: ontology_manager.get_ontology_stats()

3. OntologyManager.get_ontology_stats()
   ├─> Counts: list(self.ontology.classes())
   ├─> Counts: list(self.ontology.individuals())
   ├─> Counts: list(self.ontology.object_properties())
   ├─> Counts: list(self.ontology.data_properties())
   └─> Returns: {'loaded': True, 'classes': 17, 'individuals': 11, ...}

4. Flask renders dashboard.html
   └─> Jinja2 template displays:
       ┌──────────────────────────────────┐
       │ 🧠 Knowledge Base (Ontology)     │
       ├──────────────────────────────────┤
       │  Classes: 17                     │
       │  Individuals: 11                 │
       │  Properties: 13                  │
       └──────────────────────────────────┘
```

## Validation Flow

```
When generating a problem:

┌─────────────────────────────────────────────┐
│ generate_problem('hexagon', 'expert')       │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│ validate_problem('hexagon', 'expert')       │
│                                             │
│ 1. Get shapes from ontology:                │
│    ['square', 'rectangle', 'triangle',      │
│     'circle']                               │
│                                             │
│ 2. Check: is 'hexagon' in shapes?          │
│    → NO ✗                                   │
│                                             │
│ 3. Check: is 'expert' in difficulties?     │
│    ['beginner', 'intermediate', 'advanced'] │
│    → NO ✗                                   │
│                                             │
│ 4. Return: False                            │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│ Log warning:                                │
│ "Problem configuration (hexagon, expert)    │
│  not validated by ontology"                 │
└─────────────────────────────────────────────┘
```

## Benefits Visualization

```
WITHOUT Ontology Integration:
─────────────────────────────
GeometryTutor
    ├─ Hardcoded shapes: ['square', 'rectangle', ...]
    ├─ Hardcoded formulas in code
    ├─ No validation
    └─ No extensibility

Problem: "Add hexagon"
    └─> Requires code changes, redeployment


WITH Ontology Integration:
──────────────────────────
GeometryTutor
    ├─ Queries OWL for shapes
    ├─ Queries OWL for formulas
    ├─ Validates against OWL
    └─ Extensible via OWL editing

Problem: "Add hexagon"
    ├─> Open ontology in Protégé
    ├─> Add HexagonShape individual
    ├─> Add HexagonAreaFormula
    ├─> Link with hasFormula property
    ├─> Save OWL file
    └─> Restart app → Hexagon available! ✓
```

## Key Integration Points

1. **Initialization** (when app starts)
   ```
   App Start → Import OntologyManager → Load OWL file → Cache in memory
   ```

2. **Problem Generation** (when student practices)
   ```
   User action → Validate shape/difficulty → Generate problem → Display
   ```

3. **Dashboard Display** (when student views progress)
   ```
   Load dashboard → Query ontology stats → Render with data
   ```

4. **Formula Retrieval** (optional, ready for use)
   ```
   Need formula → Query hasFormula → Get expression/description
   ```

## Summary

The ontology is now the **central knowledge repository** that:
- ✅ Defines valid shapes and difficulties
- ✅ Stores formula expressions and descriptions  
- ✅ Provides validation for problem generation
- ✅ Displays statistics in the UI
- ✅ Enables extensibility without code changes

**All of this happens automatically when you run the application!**
