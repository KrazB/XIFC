#!/usr/bin/env python3
"""
Example usage of the IFC Fragments Converter from another Python script
"""

import sys
import subprocess
import os
from pathlib import Path

def convert_ifc_files(source_dir, target_dir=None, single_file=None, auto=False):
    """
    Convert IFC files using the portable converter
    
    Args:
        source_dir: Directory containing IFC files
        target_dir: Output directory for fragments (optional)
        single_file: Specific file to convert (optional)
        auto: Non-interactive mode (optional)
    
    Returns:
        bool: True if conversion successful, False otherwise
    """
    
    # Path to the converter
    converter_path = Path(r"D:\XQG4\frag_convert\ifc_fragments_converter.py")
    
    if not converter_path.exists():
        print(f"Error: Converter not found at {converter_path}")
        return False
    
    # Build command
    cmd = [sys.executable, str(converter_path), source_dir]
    
    if target_dir:
        cmd.append(target_dir)
    
    if single_file:
        cmd.extend(["--single", single_file])
    
    if auto:
        cmd.append("--auto")
    
    print(f"Executing: {' '.join(cmd)}")
    
    try:
        # Run the converter
        result = subprocess.run(cmd, 
                              capture_output=False,  # Show output in real-time
                              text=True)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running converter: {e}")
        return False

def main():
    """Example usage"""
    
    print("IFC Fragments Converter - Example Usage")
    print("=" * 50)
    
    # Example 1: Convert all IFC files in a directory
    print("\nExample 1: Convert all IFC files")
    success = convert_ifc_files(
        source_dir=r"C:\MyProject\IFC_Files",
        target_dir=r"C:\MyProject\Fragments",
        auto=True  # Non-interactive
    )
    print(f"Result: {'SUCCESS' if success else 'FAILED'}")
    
    # Example 2: Convert single file
    print("\nExample 2: Convert single file")
    success = convert_ifc_files(
        source_dir=r"C:\MyProject\IFC_Files",
        target_dir=r"C:\MyProject\Fragments", 
        single_file="model.ifc",
        auto=True
    )
    print(f"Result: {'SUCCESS' if success else 'FAILED'}")
    
    # Example 3: Interactive mode (prompts for overwrites)
    print("\nExample 3: Interactive mode")
    success = convert_ifc_files(
        source_dir=r"C:\MyProject\IFC_Files"
        # target_dir will default to source_dir
        # auto=False is default (interactive)
    )
    print(f"Result: {'SUCCESS' if success else 'FAILED'}")

if __name__ == "__main__":
    main()
