#!/bin/bash
# Activation script for the Python virtual environment (Linux/Mac)

echo "Activating Python virtual environment for IFC Converter..."
source venv/bin/activate

echo
echo "Virtual environment activated!"
echo "Python executable: $VIRTUAL_ENV/bin/python"
echo
echo "Available commands:"
echo "  python convert_ifc_to_fragments.py    - Run the IFC converter"
echo "  pip list                              - Show installed packages"
echo "  deactivate                            - Exit virtual environment"
echo
echo "Directory structure:"
echo "  data/ifc/                             - Place IFC files here"
echo "  data/fragments/                       - Fragment files output here"
echo "  logs/                                 - Conversion logs"
echo "  reports/                              - JSON reports"
echo
echo "To run the converter: python convert_ifc_to_fragments.py"
echo

# Keep the shell open
exec "$SHELL"
