"""Configuration management utilities."""

import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config_path: Path):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        
        if self.config_path.exists():
            self.load()
        else:
            self._load_defaults()
    
    def load(self):
        """Load configuration from file."""
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f) or {}
    
    def _load_defaults(self):
        """Load default configuration."""
        self.config = {
            "system": {
                "name": "Intelligent Tutoring System",
                "version": "0.1.0"
            },
            "tutoring": {
                "default_strategy": "adaptive",
                "assessment_threshold": 0.7
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set a configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
