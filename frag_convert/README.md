# IFC to Fragments Converter

A portable, reusable IFC to Fragments converter using ThatOpen Components library. This package provides high-performance conversion from IFC files to compressed Fragment format with excellent compression ratios and fast processing times.

## Features

- **Portable**: Can be used from any project directory
- **High Performance**: Typically achieves 90%+ compression ratios
- **Batch Processing**: Handles multiple IFC files automatically  
- **Command Line Interface**: Flexible usage options
- **Progress Tracking**: Real-time conversion progress and statistics
- **Error Handling**: Graceful error recovery and detailed logging
- **JSON Reports**: Detailed conversion reports for tracking
- **Interactive & Automated**: Supports both interactive and batch modes

## Performance

- **Compression**: Typically 90-95% size reduction
- **Speed**: ~1-2 seconds per MB of IFC data
- **Memory Efficient**: Streaming-based processing for large files

## Installation

### Prerequisites

- **Node.js** (>= 18.0.0) - [Download here](https://nodejs.org/)
- **Python** (>= 3.7) - Usually pre-installed on Windows

### Setup

The converter package is self-contained and automatically installs its dependencies when first run.

```cmd
# No installation required - just run the converter!
```

## Usage

### Basic Usage

```cmd
# Convert all IFC files in a directory (interactive mode)
python D:\XQG4\frag_convert\ifc_fragments_converter.py "C:\MyProject\IFC_Files"

# Convert with specific output directory
python D:\XQG4\frag_convert\ifc_fragments_converter.py "C:\MyProject\IFC" "C:\MyProject\Fragments"
```

### Advanced Usage

```cmd
# Convert single file
python D:\XQG4\frag_convert\ifc_fragments_converter.py "C:\IFC" "C:\Output" --single "model.ifc"

# Automated mode (no prompts, overwrites existing files)
python D:\XQG4\frag_convert\ifc_fragments_converter.py "C:\IFC" --auto

# Show help
python D:\XQG4\frag_convert\ifc_fragments_converter.py --help
```

### From Another Python Script

```python
import sys
import subprocess

# Call the converter from your Python script
result = subprocess.run([
    sys.executable, 
    r"D:\XQG4\frag_convert\ifc_fragments_converter.py",
    r"C:\MyProject\IFC_Files",
    r"C:\MyProject\Fragments",
    "--auto"  # Non-interactive
], capture_output=True, text=True)

if result.returncode == 0:
    print("Conversion successful!")
else:
    print(f"Conversion failed: {result.stderr}")
```

## Output

### Fragment Files
- **Input**: `model.ifc` (1.5 MB)
- **Output**: `model.frag` (150 KB, 90% compression)

### Logs
- **Location**: `./logs/ifc_conversion_YYYYMMDD_HHMMSS.log`
- **Content**: Detailed conversion progress and statistics

### Reports
- **Location**: `./reports/conversion_report_YYYYMMDD_HHMMSS.json`
- **Content**: JSON report with detailed statistics and results

## Example Output

```
============================================================
  IFC TO FRAGMENTS CONVERTER
   Portable ThatOpen Components Integration
============================================================
Converter Package: D:\XQG4\frag_convert
Source Directory: C:\MyProject\IFC_Files
Target Directory: C:\MyProject\Fragments
============================================================

2025-06-03 16:45:00,123 - INFO - [INFO] Validating environment...
2025-06-03 16:45:00,234 - INFO - [OK] Node.js found: v22.14.0
2025-06-03 16:45:00,235 - INFO - [OK] Environment validation completed successfully
2025-06-03 16:45:00,235 - INFO - [START] Starting IFC to Fragments conversion process
2025-06-03 16:45:00,236 - INFO - [FOLDER] Found 2 IFC files in C:\MyProject\IFC_Files
2025-06-03 16:45:00,236 - INFO -    • building_model.ifc (2.45 MB)
2025-06-03 16:45:00,236 - INFO -    • site_layout.ifc (0.87 MB)

2025-06-03 16:45:00,237 - INFO - [PROCESS] Processing file 1/2: building_model.ifc
2025-06-03 16:45:00,237 - INFO - [CONVERT] Converting: building_model.ifc
2025-06-03 16:45:02,458 - INFO - [OK] Successfully converted: building_model.ifc
2025-06-03 16:45:02,458 - INFO -    [STATS] 2.45 MB -> 0.23 MB (90.6% compression)
2025-06-03 16:45:02,459 - INFO - [STATS] Progress: 50.0% (1/2)

2025-06-03 16:45:02,459 - INFO - [PROCESS] Processing file 2/2: site_layout.ifc
2025-06-03 16:45:02,459 - INFO - [CONVERT] Converting: site_layout.ifc
2025-06-03 16:45:03,234 - INFO - [OK] Successfully converted: site_layout.ifc
2025-06-03 16:45:03,234 - INFO -    [STATS] 0.87 MB -> 0.09 MB (89.7% compression)
2025-06-03 16:45:03,235 - INFO - [STATS] Progress: 100.0% (2/2)

============================================================
[TARGET] CONVERSION SUMMARY
============================================================
[FOLDER] Source Directory: C:\MyProject\IFC_Files
[FOLDER] Target Directory: C:\MyProject\Fragments
[TIME] Total Time: 3.00 seconds
[STATS] Files Processed: 2
[OK] Successful: 2
[ERROR] Failed: 0
[SKIP] Skipped: 0
[TARGET] Success Rate: 100.0%

[RESULTS] DETAILED RESULTS:
   [OK] building_model.ifc (2.22s)
   [OK] site_layout.ifc (0.78s)

[REPORT] Detailed report saved: .\reports\conversion_report_20250603_164503.json
============================================================
[DONE] Conversion process completed!
```

## Package Structure

```
D:\XQG4\frag_convert\
├── ifc_fragments_converter.py     # Main Python application
├── convert_ifc_to_fragments.js    # Node.js conversion engine
├── package.json                   # NPM dependencies
├── node_modules\                  # NPM packages (auto-installed)
│   ├── @thatopen\fragments        # Core conversion library
│   ├── web-ifc\                   # WASM IFC parser
│   └── ...                        # Other dependencies
└── README.md                      # This file
```

## Dependencies

### Automatic (Installed automatically)
- `@thatopen/fragments` - Core conversion library
- `@thatopen/components` - ThatOpen Components framework
- `web-ifc` - High-performance IFC parser

### System Requirements
- **Node.js** >= 18.0.0
- **Python** >= 3.7
- **Windows** (tested on Windows 10/11)

## Troubleshooting

### Common Issues

1. **"Node.js is not installed"**
   - Download and install Node.js from [nodejs.org](https://nodejs.org/)
   - Restart your command prompt after installation

2. **"npm install failed"**
   - Check your internet connection
   - Try running from an administrator command prompt
   - Ensure you have sufficient disk space

3. **"Source directory not found"**
   - Verify the path exists and is accessible
   - Use absolute paths to avoid confusion
   - Check folder permissions

4. **Very slow conversion**
   - This is normal for large IFC files (>10MB)
   - The converter uses streaming for memory efficiency
   - Monitor the progress logs for updates

### Support

For issues or questions:
1. Check the log files in `./logs/` directory
2. Review the detailed JSON reports in `./reports/` directory
3. Ensure all prerequisites are installed correctly

## Version History

- **1.0.0** - Initial release with full functionality
  - Batch processing support
  - Command line interface
  - Detailed logging and reporting
  - High-performance conversion engine

## License

This package uses ThatOpen Components library. Please refer to their licensing terms.

---

**IFC to Fragments Converter v1.0.0**  
*High-performance IFC conversion using ThatOpen Components*
