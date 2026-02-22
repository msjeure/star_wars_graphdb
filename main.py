"""
Main entry point for the Star Wars GraphDB system
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.chat_interface import ChatInterface


def main():
    """Main entry point"""
    current_dir = Path(__file__).parent
    ttl_path = current_dir / "SWAPI-WD-data.ttl"
    
    if not ttl_path.exists():
        print(f"❌ Error: TTL file not found at {ttl_path}")
        print("Please ensure SWAPI-WD-data.ttl is in the project root directory.")
        sys.exit(1)
    
    # Get model configuration
    model = os.getenv("SWAPI_MODEL", "gpt-4")
    
    # Create and run chat interface
    chat = ChatInterface(str(ttl_path), model=model)
    chat.run()


if __name__ == "__main__":
    main()
