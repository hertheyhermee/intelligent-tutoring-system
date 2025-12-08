"""Core application class for the Intelligent Tutoring System."""

import logging
from pathlib import Path
from typing import Optional

from ..utils.config import ConfigManager
from ..utils.logger import setup_logger


class Application:
    """Main application class for the Intelligent Tutoring System."""
    
    def __init__(self, config_path: Path, debug: bool = False):
        """Initialize the application.
        
        Args:
            config_path: Path to configuration file
            debug: Enable debug mode
        """
        self.debug = debug
        self.logger = setup_logger(__name__, debug=debug)
        self.config = ConfigManager(config_path)
        
        self.logger.info("Intelligent Tutoring System initialized")
    
    def run(self, mode: str = "interactive"):
        """Run the application.
        
        Args:
            mode: Operation mode (interactive, batch, or server)
        """
        self.logger.info(f"Starting application in {mode} mode")
        
        if mode == "interactive":
            self._run_interactive()
        elif mode == "batch":
            self._run_batch()
        elif mode == "server":
            self._run_server()
        else:
            raise ValueError(f"Unknown mode: {mode}")
    
    def _run_interactive(self):
        """Run in interactive mode."""
        self.logger.info("Interactive mode not yet implemented")
        print("Welcome to the Intelligent Tutoring System!")
        print("Interactive mode coming soon...")
    
    def _run_batch(self):
        """Run in batch mode."""
        self.logger.info("Batch mode not yet implemented")
        print("Batch processing mode coming soon...")
    
    def _run_server(self):
        """Run in server mode."""
        self.logger.info("Starting web server mode")
        try:
            from ..web.app import run_server
            print("🚀 Starting Geometry Tutor Web Server...")
            print("📖 Open your browser and go to: http://127.0.0.1:5000")
            print("Press Ctrl+C to stop the server\n")
            run_server(debug=self.debug)
        except ImportError:
            self.logger.error("Flask not installed. Install with: pip install flask")
            print("Error: Flask is required for web mode. Install with: pip install flask")
