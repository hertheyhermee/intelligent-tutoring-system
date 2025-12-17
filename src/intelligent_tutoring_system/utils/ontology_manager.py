"""Ontology manager for loading and querying the Geometry Tutor OWL ontology."""

from pathlib import Path
from typing import Dict, List, Optional
import logging

try:
    from owlready2 import get_ontology, sync_reasoner_pellet
    OWLREADY_AVAILABLE = True
except ImportError:
    OWLREADY_AVAILABLE = False
    logging.warning("owlready2 not installed. Ontology features will be limited.")


class OntologyManager:
    """Manages the Geometry Tutor ontology and provides query methods."""
    
    def __init__(self, ontology_path: Optional[Path] = None):
        """Initialize the ontology manager.
        
        Args:
            ontology_path: Path to the OWL file. If None, uses default location.
        """
        self.ontology = None
        self.namespace = None
        
        if not OWLREADY_AVAILABLE:
            logging.warning("Ontology features disabled - owlready2 not installed")
            return
        
        if ontology_path is None:
            # Default path relative to project root
            project_root = Path(__file__).parent.parent.parent.parent
            ontology_path = project_root / "ontology" / "its-ontology.owl"
        
        self.ontology_path = Path(ontology_path)
        
        if self.ontology_path.exists():
            self._load_ontology()
        else:
            logging.warning(f"Ontology file not found: {self.ontology_path}")
    
    def _load_ontology(self):
        """Load the ontology from OWL file."""
        try:
            # Load ontology
            self.ontology = get_ontology(f"file://{self.ontology_path}").load()
            
            # Get namespace
            self.namespace = self.ontology.get_namespace(
                "http://www.semanticweb.org/geometry-tutor/ontology#"
            )
            
            logging.info(f"Ontology loaded successfully from {self.ontology_path}")
            
            # Optional: Run reasoner for inference
            # with self.ontology:
            #     sync_reasoner_pellet()
            
        except Exception as e:
            logging.error(f"Error loading ontology: {e}")
            self.ontology = None
            self.namespace = None
    
    def get_shape_formula(self, shape_name: str) -> Optional[Dict[str, str]]:
        """Get the area formula for a shape from the ontology.
        
        Args:
            shape_name: Name of the shape (e.g., 'square', 'rectangle')
            
        Returns:
            Dictionary with 'expression' and 'description' or None
        """
        if not self.namespace:
            return None
        
        try:
            # Map shape names to ontology instances
            shape_map = {
                'square': 'SquareShape',
                'rectangle': 'RectangleShape',
                'triangle': 'TriangleShape',
                'circle': 'CircleShape'
            }
            
            instance_name = shape_map.get(shape_name.lower())
            if not instance_name:
                return None
            
            # Get shape instance
            shape_instance = getattr(self.namespace, instance_name, None)
            if not shape_instance:
                return None
            
            # Get formula through hasFormula relationship
            formulas = shape_instance.hasFormula
            if formulas:
                formula = formulas[0]
                return {
                    'expression': getattr(formula, 'formulaExpression', [''])[0],
                    'description': getattr(formula, 'formulaDescription', [''])[0]
                }
            
        except Exception as e:
            logging.error(f"Error querying shape formula: {e}")
        
        return None
    
    def get_all_shapes(self) -> List[str]:
        """Get list of all shape names from the ontology.
        
        Returns:
            List of shape names
        """
        if not self.namespace:
            return ['square', 'rectangle', 'triangle', 'circle']  # Fallback
        
        try:
            shapes = []
            shape_map = {
                'SquareShape': 'square',
                'RectangleShape': 'rectangle',
                'TriangleShape': 'triangle',
                'CircleShape': 'circle'
            }
            
            for instance_name, shape_name in shape_map.items():
                instance = getattr(self.namespace, instance_name, None)
                if instance:
                    shapes.append(shape_name)
            
            return shapes if shapes else ['square', 'rectangle', 'triangle', 'circle']
            
        except Exception as e:
            logging.error(f"Error querying shapes: {e}")
            return ['square', 'rectangle', 'triangle', 'circle']
    
    def get_difficulty_levels(self) -> List[str]:
        """Get list of all difficulty levels from the ontology.
        
        Returns:
            List of difficulty level names
        """
        if not self.namespace:
            return ['beginner', 'intermediate', 'advanced']  # Fallback
        
        try:
            levels = []
            
            # Check for difficulty level instances
            for level_name in ['BeginnerLevel', 'IntermediateLevel', 'AdvancedLevel']:
                instance = getattr(self.namespace, level_name, None)
                if instance:
                    levels.append(level_name.replace('Level', '').lower())
            
            return levels if levels else ['beginner', 'intermediate', 'advanced']
            
        except Exception as e:
            logging.error(f"Error querying difficulty levels: {e}")
            return ['beginner', 'intermediate', 'advanced']
    
    def get_shape_properties(self, shape_name: str) -> Optional[Dict]:
        """Get properties of a shape from the ontology.
        
        Args:
            shape_name: Name of the shape
            
        Returns:
            Dictionary of shape properties or None
        """
        if not self.namespace:
            return None
        
        try:
            shape_map = {
                'square': 'SquareShape',
                'rectangle': 'RectangleShape',
                'triangle': 'TriangleShape',
                'circle': 'CircleShape'
            }
            
            instance_name = shape_map.get(shape_name.lower())
            if not instance_name:
                return None
            
            shape_instance = getattr(self.namespace, instance_name, None)
            if not shape_instance:
                return None
            
            properties = {
                'name': shape_name,
                'label': str(getattr(shape_instance, 'label', [shape_name])[0]),
            }
            
            # Get number of sides for polygons
            if hasattr(shape_instance, 'numberOfSides'):
                sides = getattr(shape_instance, 'numberOfSides', [])
                if sides:
                    properties['numberOfSides'] = sides[0]
            
            return properties
            
        except Exception as e:
            logging.error(f"Error querying shape properties: {e}")
            return None
    
    def validate_problem(self, shape: str, difficulty: str) -> bool:
        """Validate that a problem configuration is valid according to ontology.
        
        Args:
            shape: Shape name
            difficulty: Difficulty level
            
        Returns:
            True if valid, False otherwise
        """
        if not self.namespace:
            # Fallback validation
            valid_shapes = ['square', 'rectangle', 'triangle', 'circle']
            valid_difficulties = ['beginner', 'intermediate', 'advanced']
            return shape.lower() in valid_shapes and difficulty.lower() in valid_difficulties
        
        shapes = self.get_all_shapes()
        difficulties = self.get_difficulty_levels()
        
        return shape.lower() in shapes and difficulty.lower() in difficulties
    
    def get_ontology_stats(self) -> Dict:
        """Get statistics about the loaded ontology.
        
        Returns:
            Dictionary with ontology statistics
        """
        if not self.ontology:
            return {
                'loaded': False,
                'message': 'Ontology not loaded'
            }
        
        try:
            stats = {
                'loaded': True,
                'path': str(self.ontology_path),
                'classes': len(list(self.ontology.classes())),
                'individuals': len(list(self.ontology.individuals())),
                'object_properties': len(list(self.ontology.object_properties())),
                'data_properties': len(list(self.ontology.data_properties())),
            }
            return stats
            
        except Exception as e:
            return {
                'loaded': True,
                'error': str(e)
            }


# Global ontology manager instance
_ontology_manager = None


def get_ontology_manager() -> OntologyManager:
    """Get the global ontology manager instance.
    
    Returns:
        OntologyManager instance
    """
    global _ontology_manager
    if _ontology_manager is None:
        _ontology_manager = OntologyManager()
    return _ontology_manager
