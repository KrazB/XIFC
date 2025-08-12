#!/usr/bin/env python3
r"""
IFC to Fragments Converter - Portable Application
=================================================

A portable, reusable IFC to Fragments converter using ThatOpen Components.
This tool can be used from any project to convert IFC files to compressed Fragment format.

Features:
- Portable: Can be called from any directory/project
- Batch processing: Handles multiple IFC files automatically
- Command line interface: Flexible source/target directory specification
- Progress tracking: Real-time conversion progress and statistics
- Error handling: Graceful error recovery and detailed logging
- Performance stats: Compression ratios and conversion times
- JSON reports: Detailed conversion reports for tracking

Usage:
    # Convert all IFC files in a directory
    python D:\XQG4\frag_convert\ifc_fragments_converter.py <source_dir>
    
    # Convert with specific target directory
    python D:\XQG4\frag_convert\ifc_fragments_converter.py <source_dir> <target_dir>
    
    # Convert single file
    python D:\XQG4\frag_convert\ifc_fragments_converter.py <source_dir> <target_dir> --single <filename>

Examples:
    python D:\XQG4\frag_convert\ifc_fragments_converter.py "C:\MyProject\IFC_Files"
    python D:\XQG4\frag_convert\ifc_fragments_converter.py "C:\MyProject\IFC" "C:\MyProject\Fragments"
    python D:\XQG4\frag_convert\ifc_fragments_converter.py "C:\IFC" "C:\Output" --single "model.ifc"

Dependencies:
- Node.js (>=18.0.0)
- @thatopen/fragments npm package (auto-installed)
- Python standard libraries

Author: IFC Fragments Converter Package
Version: 1.0.0
"""

import os
import sys
import argparse
import subprocess
import logging
import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Get the directory where this script is located (the converter package directory)
CONVERTER_DIR = Path(__file__).parent
NODE_SCRIPT = CONVERTER_DIR / "convert_ifc_to_fragments.js"

class IfcFragmentsConverter:
    """
    Portable IFC to Fragments converter that can be used from any project
    """
    
    def __init__(self, source_dir: str, target_dir: str = None, single_file: str = None):
        """
        Initialize the converter
        
        Args:
            source_dir: Directory containing IFC files (or parent dir if single_file specified)
            target_dir: Directory for output fragment files (default: same as source_dir)
            single_file: Specific IFC file to convert (optional)
        """
        self.source_dir = Path(source_dir).resolve()
        self.target_dir = Path(target_dir).resolve() if target_dir else self.source_dir
        self.single_file = single_file
        self.converter_dir = CONVERTER_DIR
        self.node_script = NODE_SCRIPT
        
        # Ensure target directory exists
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # Conversion statistics
        self.stats = {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'start_time': None,
            'end_time': None,
            'total_time': 0,
            'results': []
        }
    
    def setup_logging(self):
        """Configure logging for the conversion process"""
        # Create logs directory in the working directory (not converter directory)
        log_dir = Path.cwd() / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"ifc_conversion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"[INFO] Log file: {log_file}")
    
    def validate_environment(self) -> bool:
        """Validate that all required dependencies are available"""
        self.logger.info("[INFO] Validating environment...")
        
        # Check Node.js installation
        try:
            result = subprocess.run(['node', '--version'], 
                                 capture_output=True, text=True, shell=False)
            if result.returncode != 0:
                self.logger.error("[ERROR] Node.js is not installed or not in PATH")
                return False
            
            node_version = result.stdout.strip()
            self.logger.info(f"[OK] Node.js found: {node_version}")
            
            # Check if version is >= 18
            version_num = node_version.lstrip('v').split('.')[0]
            if int(version_num) < 18:
                self.logger.error(f"[ERROR] Node.js version {node_version} is too old. Requires >= 18.0.0")
                return False
                
        except Exception as e:
            self.logger.error(f"[ERROR] Failed to check Node.js: {e}")
            return False
        
        # Check converter package components
        if not self.converter_dir.exists():
            self.logger.error(f"[ERROR] Converter directory not found: {self.converter_dir}")
            return False
        
        if not self.node_script.exists():
            self.logger.error(f"[ERROR] Node.js converter script not found: {self.node_script}")
            return False
        
        package_json = self.converter_dir / "package.json"
        if not package_json.exists():
            self.logger.error(f"[ERROR] package.json not found: {package_json}")
            return False
        
        node_modules = self.converter_dir / "node_modules"
        if not node_modules.exists():
            self.logger.warning(f"[WARN] node_modules not found at {node_modules}")
            self.logger.info("[INFO] Attempting to install dependencies...")
            if not self.install_dependencies():
                return False
        
        # Check source directory
        if not self.source_dir.exists():
            self.logger.error(f"[ERROR] Source directory not found: {self.source_dir}")
            return False
        
        self.logger.info("[OK] Environment validation completed successfully")
        return True
    
    def install_dependencies(self) -> bool:
        """Install required npm dependencies"""
        self.logger.info("[INSTALL] Installing npm dependencies...")
        
        try:
            original_cwd = os.getcwd()
            os.chdir(self.converter_dir)
            
            result = subprocess.run(['npm', 'install'], 
                                 capture_output=True, text=True, shell=False)
            
            os.chdir(original_cwd)
            
            if result.returncode != 0:
                self.logger.error(f"[ERROR] npm install failed: {result.stderr}")
                return False
            
            self.logger.info("[OK] npm dependencies installed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"[ERROR] Failed to install npm dependencies: {e}")
            return False
    
    def find_ifc_files(self) -> List[Path]:
        """Find IFC files to convert"""
        ifc_files = []
        
        if self.single_file:
            # Convert single file
            single_path = self.source_dir / self.single_file
            if single_path.exists() and single_path.suffix.lower() == '.ifc':
                ifc_files = [single_path]
            else:
                self.logger.error(f"[ERROR] Single file not found or not IFC: {single_path}")
                return []
        else:
            # Find all IFC files in directory
            for pattern in ['*.ifc', '*.IFC']:
                ifc_files.extend(self.source_dir.glob(pattern))
            
            ifc_files = sorted(set(ifc_files))
        
        self.logger.info(f"[FOLDER] Found {len(ifc_files)} IFC files in {self.source_dir}")
        for ifc_file in ifc_files:
            file_size = ifc_file.stat().st_size / (1024 * 1024)  # MB
            self.logger.info(f"   • {ifc_file.name} ({file_size:.2f} MB)")
        
        return ifc_files
    
    def convert_single_file(self, ifc_file: Path, interactive: bool = True) -> Dict:
        """Convert a single IFC file to fragments"""
        start_time = time.time()
        
        # Generate output path
        output_file = self.target_dir / f"{ifc_file.stem}.frag"
        
        # Check if output already exists
        if output_file.exists() and interactive:
            self.logger.warning(f"[WARN] Output file already exists: {output_file.name}")
            response = input(f"Overwrite {output_file.name}? (y/N): ").strip().lower()
            if response != 'y':
                self.logger.info(f"[SKIP] Skipping {ifc_file.name}")
                return {
                    'file': ifc_file.name,
                    'status': 'skipped',
                    'message': 'File already exists, user chose not to overwrite'
                }
        
        self.logger.info(f"[CONVERT] Converting: {ifc_file.name}")
        
        try:
            # Execute Node.js converter
            cmd = ['node', str(self.node_script), str(ifc_file), str(output_file)]
            
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  shell=False,
                                  encoding='utf-8',
                                  errors='replace',
                                  cwd=self.converter_dir)
            
            conversion_time = time.time() - start_time
            
            # Parse the result
            if result.returncode == 0:
                # Look for JSON result in stdout
                json_result = None
                if result.stdout:
                    for line in result.stdout.split('\n'):
                        if line.startswith('CONVERSION_RESULT_JSON:'):
                            try:
                                json_result = json.loads(line.split(':', 1)[1].strip())
                                break
                            except json.JSONDecodeError:
                                pass
                
                if json_result and json_result.get('success'):
                    self.logger.info(f"[OK] Successfully converted: {ifc_file.name}")
                    if 'stats' in json_result:
                        stats = json_result['stats']
                        self.logger.info(f"   [STATS] {stats.get('inputSizeMB', 'N/A')} MB -> "
                                       f"{stats.get('outputSizeMB', 'N/A')} MB "
                                       f"({stats.get('compressionRatio', 'N/A')} compression)")
                    
                    return {
                        'file': ifc_file.name,
                        'status': 'success',
                        'message': json_result.get('message', 'Conversion successful'),
                        'conversion_time': conversion_time,
                        'stats': json_result.get('stats', {})
                    }
                else:
                    error_msg = json_result.get('message', 'Unknown error') if json_result else 'No result data'
                    raise Exception(error_msg)
            else:
                raise Exception(f"Node.js script failed with code {result.returncode}: {result.stderr}")
                
        except Exception as e:
            self.logger.error(f"[ERROR] Failed to convert {ifc_file.name}: {e}")
            return {
                'file': ifc_file.name,
                'status': 'failed',
                'message': str(e),
                'conversion_time': time.time() - start_time
            }
    
    def convert_all_files(self, interactive: bool = True):
        """Convert all found IFC files"""
        self.logger.info("[START] Starting IFC to Fragments conversion process")
        self.stats['start_time'] = datetime.now()
        
        # Find IFC files
        ifc_files = self.find_ifc_files()
        self.stats['total_files'] = len(ifc_files)
        
        if not ifc_files:
            self.logger.warning("[WARN] No IFC files found")
            return
        
        # Process each file
        for i, ifc_file in enumerate(ifc_files, 1):
            self.logger.info(f"[PROCESS] Processing file {i}/{len(ifc_files)}: {ifc_file.name}")
            
            result = self.convert_single_file(ifc_file, interactive)
            self.stats['results'].append(result)
            
            # Update counters
            if result['status'] == 'success':
                self.stats['successful'] += 1
            elif result['status'] == 'failed':
                self.stats['failed'] += 1
            elif result['status'] == 'skipped':
                self.stats['skipped'] += 1
            
            # Progress update
            progress = (i / len(ifc_files)) * 100
            self.logger.info(f"[STATS] Progress: {progress:.1f}% ({i}/{len(ifc_files)})")
        
        # Finalize statistics
        self.stats['end_time'] = datetime.now()
        self.stats['total_time'] = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        
        self.print_summary()
    
    def print_summary(self):
        """Print conversion summary and statistics"""
        self.logger.info("\n" + "="*60)
        self.logger.info("[TARGET] CONVERSION SUMMARY")
        self.logger.info("="*60)
        
        self.logger.info(f"[FOLDER] Source Directory: {self.source_dir}")
        self.logger.info(f"[FOLDER] Target Directory: {self.target_dir}")
        self.logger.info(f"[TIME] Total Time: {self.stats['total_time']:.2f} seconds")
        self.logger.info(f"[STATS] Files Processed: {self.stats['total_files']}")
        self.logger.info(f"[OK] Successful: {self.stats['successful']}")
        self.logger.info(f"[ERROR] Failed: {self.stats['failed']}")
        self.logger.info(f"[SKIP] Skipped: {self.stats['skipped']}")
        
        if self.stats['successful'] > 0:
            success_rate = (self.stats['successful'] / self.stats['total_files']) * 100
            self.logger.info(f"[TARGET] Success Rate: {success_rate:.1f}%")
        
        # Detailed results
        if self.stats['results']:
            self.logger.info("\n[RESULTS] DETAILED RESULTS:")
            for result in self.stats['results']:
                status_icon = {"success": "[OK]", "failed": "[ERROR]", "skipped": "[SKIP]"}.get(result['status'], "[?]")
                time_info = f" ({result.get('conversion_time', 0):.2f}s)" if 'conversion_time' in result else ""
                self.logger.info(f"   {status_icon} {result['file']}{time_info}")
                if result['status'] != 'success' and 'message' in result:
                    self.logger.info(f"      -> {result['message']}")
        
        # Save detailed report
        self.save_report()
        
        self.logger.info("="*60)
        self.logger.info("[DONE] Conversion process completed!")
    
    def save_report(self):
        """Save detailed conversion report to JSON file"""
        reports_dir = Path.cwd() / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        report_file = reports_dir / f"conversion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report_data = {
            'conversion_summary': self.stats,
            'environment': {
                'source_directory': str(self.source_dir),
                'target_directory': str(self.target_dir),
                'converter_directory': str(self.converter_dir),
                'working_directory': str(Path.cwd())
            },
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, default=str)
            
            self.logger.info(f"[REPORT] Detailed report saved: {report_file}")
        except Exception as e:
            self.logger.warning(f"[WARN] Could not save report: {e}")
    
    def run(self, interactive: bool = True):
        """Main execution method"""
        try:
            print("\n" + "="*60)
            print("  IFC TO FRAGMENTS CONVERTER")
            print("   Portable ThatOpen Components Integration")
            print("="*60)
            print(f"Converter Package: {self.converter_dir}")
            print(f"Source Directory: {self.source_dir}")
            print(f"Target Directory: {self.target_dir}")
            if self.single_file:
                print(f"Single File: {self.single_file}")
            print("="*60)
            
            # Environment validation
            if not self.validate_environment():
                self.logger.error("[ERROR] Environment validation failed. Please fix the issues above.")
                return False
            
            # Start conversion process
            self.convert_all_files(interactive)
            return True
            
        except KeyboardInterrupt:
            self.logger.warning("\n[WARN] Conversion interrupted by user")
            return False
        except Exception as e:
            self.logger.error(f"[ERROR] Unexpected error: {e}")
            return False

def main():
    """Main entry point with command line argument parsing"""
    
    parser = argparse.ArgumentParser(
        description='IFC to Fragments Converter - Portable Application',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "C:\\MyProject\\IFC_Files"
  %(prog)s "C:\\MyProject\\IFC" "C:\\MyProject\\Fragments"
  %(prog)s "C:\\IFC" "C:\\Output" --single "model.ifc"
  %(prog)s "C:\\IFC" --auto  # Non-interactive mode
        """
    )
    
    parser.add_argument('source_dir', 
                       help='Directory containing IFC files')
    
    parser.add_argument('target_dir', nargs='?', 
                       help='Directory for output fragment files (default: same as source_dir)')
    
    parser.add_argument('--single', '-s', 
                       help='Convert only this specific IFC file')
    
    parser.add_argument('--auto', '-a', action='store_true',
                       help='Non-interactive mode (overwrite existing files without asking)')
    
    parser.add_argument('--version', '-v', action='version', version='IFC Fragments Converter 1.0.0')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not os.path.exists(args.source_dir):
        print(f"Error: Source directory does not exist: {args.source_dir}")
        sys.exit(1)
    
    if args.single and not os.path.exists(os.path.join(args.source_dir, args.single)):
        print(f"Error: Single file does not exist: {os.path.join(args.source_dir, args.single)}")
        sys.exit(1)
    
    # Create converter and run
    converter = IfcFragmentsConverter(
        source_dir=args.source_dir,
        target_dir=args.target_dir,
        single_file=args.single
    )
    
    success = converter.run(interactive=not args.auto)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
