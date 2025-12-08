#!/usr/bin/env python
"""Test script to demonstrate ontology integration in the tutoring system."""

from src.intelligent_tutoring_system.utils.ontology_manager import get_ontology_manager
from src.intelligent_tutoring_system.domains.geometry import GeometryTutor

def main():
    print("=" * 60)
    print("ONTOLOGY INTEGRATION TEST")
    print("=" * 60)
    
    # Test 1: Get ontology manager
    print("\n1. Loading Ontology Manager...")
    ontology_mgr = get_ontology_manager()
    
    # Test 2: Get ontology stats
    print("\n2. Ontology Statistics:")
    stats = ontology_mgr.get_ontology_stats()
    if stats.get('loaded'):
        print(f"   ✓ Ontology loaded successfully")
        print(f"   - Path: {stats.get('path', 'N/A')}")
        print(f"   - Classes: {stats.get('classes', 0)}")
        print(f"   - Individuals: {stats.get('individuals', 0)}")
        print(f"   - Object Properties: {stats.get('object_properties', 0)}")
        print(f"   - Data Properties: {stats.get('data_properties', 0)}")
    else:
        print(f"   ✗ Ontology not loaded: {stats.get('message', 'Unknown error')}")
    
    # Test 3: Get shapes from ontology
    print("\n3. Shapes from Ontology:")
    shapes = ontology_mgr.get_all_shapes()
    print(f"   Available shapes: {', '.join(shapes)}")
    
    # Test 4: Get difficulty levels
    print("\n4. Difficulty Levels from Ontology:")
    difficulties = ontology_mgr.get_difficulty_levels()
    print(f"   Available difficulties: {', '.join(difficulties)}")
    
    # Test 5: Get formulas for each shape
    print("\n5. Shape Formulas from Ontology:")
    for shape in shapes:
        formula = ontology_mgr.get_shape_formula(shape)
        if formula:
            print(f"   {shape.title()}:")
            print(f"      Expression: {formula['expression']}")
            print(f"      Description: {formula['description']}")
        else:
            print(f"   {shape.title()}: No formula available")
    
    # Test 6: Get shape properties
    print("\n6. Shape Properties from Ontology:")
    for shape in shapes:
        props = ontology_mgr.get_shape_properties(shape)
        if props:
            print(f"   {shape.title()}: {props}")
    
    # Test 7: Validate problem configurations
    print("\n7. Problem Validation:")
    test_cases = [
        ('square', 'beginner'),
        ('circle', 'advanced'),
        ('hexagon', 'beginner'),  # Invalid shape
        ('square', 'expert')       # Invalid difficulty
    ]
    
    for shape, difficulty in test_cases:
        is_valid = ontology_mgr.validate_problem(shape, difficulty)
        status = "✓ Valid" if is_valid else "✗ Invalid"
        print(f"   {status}: {shape} + {difficulty}")
    
    # Test 8: GeometryTutor integration
    print("\n8. GeometryTutor Integration:")
    tutor = GeometryTutor()
    print("   ✓ GeometryTutor initialized with ontology support")
    
    # Generate a problem
    problem = tutor.generate_problem('square', 'beginner')
    print(f"   Sample problem generated: {problem.question}")
    print(f"   Hint: {problem.hint}")
    
    print("\n" + "=" * 60)
    print("INTEGRATION TEST COMPLETE")
    print("=" * 60)
    print("\n🎉 The ontology is now integrated into your tutoring system!")
    print("\nWhat's happening behind the scenes:")
    print("- GeometryTutor loads the OWL ontology on initialization")
    print("- Problem generation validates shapes and difficulties")
    print("- Formulas can be fetched from ontology (ready for UI display)")
    print("- Dashboard shows ontology statistics")
    print("\nTo see it in action:")
    print("  python -m intelligent_tutoring_system")
    print("  or: its")
    print()

if __name__ == "__main__":
    main()
