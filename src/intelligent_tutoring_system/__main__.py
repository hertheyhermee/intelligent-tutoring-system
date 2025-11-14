"""Main entry point for the Intelligent Tutoring System."""

import argparse
import sys
from pathlib import Path

from .core.application import Application


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Intelligent Tutoring System - Adaptive Learning Platform"
    )
    parser.add_argument(
        "--config",
        type=Path,
        default="config/config.yaml",
        help="Path to configuration file",
    )
    parser.add_argument(
        "--mode",
        choices=["interactive", "batch", "server"],
        default="server",
        help="Operation mode (default: server for web interface)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )
    return parser.parse_args()


def main():
    """Main application entry point."""
    args = parse_args()
    
    try:
        app = Application(config_path=args.config, debug=args.debug)
        app.run(mode=args.mode)
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.debug:
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()
