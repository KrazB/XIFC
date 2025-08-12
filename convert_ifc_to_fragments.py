#!/usr/bin/env python3
r"""
IFC to Fragments Converter - Organized Directory Structure
==========================================================

A clean script that converts IFC files from data/ifc/ directory to fragments 
format in data/fragments/ directory, skipping files where the equivalent 
fragments file already exists.

Uses the portable converter at D:\XIFC\frag_convert\

Features:
- Organized directory structure: data/ifc/ → data/fragments/
- Skips conversion if equivalent .frag file already exists
- Uses the portable frag_convert package
- Detailed logging and progress reporting
- Error handling and recovery

Usage:
    python convert_ifc_to_fragments.py

Dependencies:
- Portable converter package at D:\XIFC\frag_convert\
- Python standard libraries
- Node.js (for the converter package)

Author: IFC Fragments Converter
Version: 2.0.0
"""

import os
import sys
import subprocess
import logging
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional

class SimpleIfcConverter:
    """
    Organized IFC to Fragments converter with clean directory structure
    """
    
    def __init__(self):
        # Define script directory and organized data directories
        self.script_dir = Path(__file__).parent.resolve()
        self.data_dir = self.script_dir / "data"
        self.source_dir = self.data_dir / "ifc"
        self.target_dir = self.data_dir / "fragments"
        
        # Ensure directories exist
        self.source_dir.mkdir(parents=True, exist_ok=True)
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.log_dir = self.script_dir / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.setup_logging()
        
        # Portable converter configuration
        self.converter_package_dir = Path("D:/XIFC/frag_convert")
        self.portable_converter = self.converter_package_dir / "ifc_fragments_converter.py"
        
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
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file_path = self.log_dir / f'ifc_conversion_{timestamp}.log'
        
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        
        # Create handlers with UTF-8 encoding
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        console_handler = logging.StreamHandler(sys.stdout)
        
        # Set encoding for console if possible
        if hasattr(console_handler.stream, 'reconfigure'):
            try:
                console_handler.stream.reconfigure(encoding='utf-8')
            except:
                pass
        
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[file_handler, console_handler]
        )
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("=" * 80)
        self.logger.info("🚀 IFC to Fragments Converter - Organized Directory Structure")
        self.logger.info("=" * 80)
        self.logger.info(f"📂 Script directory: {self.script_dir}")
        self.logger.info(f"📥 Source directory: {self.source_dir}")
        self.logger.info(f"📤 Target directory: {self.target_dir}")
        self.logger.info(f"📄 Log file: {log_file_path}")
    
    def validate_environment(self) -> bool:
        """
        Validate that all required dependencies are available
        """
        self.logger.info("🔍 Validating environment...")
        
        # Check Python installation
        try:
            python_version = sys.version
            self.logger.info(f"✅ Python found: {python_version.split()[0]}")
            self.logger.info(f"✅ Python executable: {sys.executable}")
        except Exception as e:
            self.logger.error(f"❌ Failed to check Python: {e}")
            return False
        
        # Check if portable converter package exists
        if not self.converter_package_dir.exists():
            self.logger.error(f"❌ Portable converter package not found at {self.converter_package_dir}")
            self.logger.error("   Expected path: D:/XIFC/frag_convert/")
            self.logger.error("   Please ensure the portable converter package exists.")
            return False
        
        # Check if portable converter script exists
        if not self.portable_converter.exists():
            self.logger.error(f"❌ Portable converter script not found at {self.portable_converter}")
            return False
        
        self.logger.info(f"✅ Portable converter found: {self.converter_package_dir}")
        
        # Check source directory
        if not self.source_dir.exists():
            self.logger.warning(f"⚠️  Source directory not found, creating: {self.source_dir}")
            try:
                self.source_dir.mkdir(parents=True, exist_ok=True)
                self.logger.info(f"✅ Source directory created: {self.source_dir}")
            except Exception as e:
                self.logger.error(f"❌ Failed to create source directory: {e}")
                return False
        else:
            self.logger.info(f"✅ Source directory found: {self.source_dir}")
        
        # Check target directory (create if doesn't exist)
        if not self.target_dir.exists():
            self.logger.warning(f"⚠️  Target directory not found, creating: {self.target_dir}")
            try:
                self.target_dir.mkdir(parents=True, exist_ok=True)
                self.logger.info(f"✅ Target directory created: {self.target_dir}")
            except Exception as e:
                self.logger.error(f"❌ Failed to create target directory: {e}")
                return False
        else:
            self.logger.info(f"✅ Target directory found: {self.target_dir}")
        
        self.logger.info("✅ Environment validation completed successfully")
        return True
    
    def find_ifc_files(self) -> List[Path]:
        """
        Find all IFC files in the data/ifc directory
        """
        self.logger.info(f"🔍 Searching for IFC files in: {self.source_dir}")
        ifc_files = []
        
        # Search for .ifc files (case insensitive)
        for pattern in ['*.ifc', '*.IFC']:
            found_files = list(self.source_dir.glob(pattern))
            ifc_files.extend(found_files)
        
        ifc_files = sorted(set(ifc_files))  # Remove duplicates and sort
        
        if not ifc_files:
            self.logger.warning(f"⚠️  No IFC files found in {self.source_dir}")
            return []
        
        self.logger.info(f"📋 Found {len(ifc_files)} IFC file(s):")
        total_size = 0
        for i, ifc_file in enumerate(ifc_files, 1):
            file_size = ifc_file.stat().st_size / (1024 * 1024)  # MB
            total_size += file_size
            self.logger.info(f"   {i}. {ifc_file.name} ({file_size:.2f} MB)")
        
        self.logger.info(f"📊 Total size: {total_size:.2f} MB across {len(ifc_files)} file(s)")
        return ifc_files
    
    def check_fragments_exists(self, ifc_file: Path) -> Tuple[bool, Optional[Path]]:
        """
        Check if corresponding fragments file already exists
        
        Args:
            ifc_file: Path to the IFC file
            
        Returns:
            Tuple of (exists, fragments_file_path)
        """
        fragments_file = self.target_dir / f"{ifc_file.stem}.frag"
        exists = fragments_file.exists() and fragments_file.stat().st_size > 0
        return exists, fragments_file
    
    def convert_single_file(self, ifc_file: Path) -> Dict:
        """
        Convert a single IFC file to fragments using the portable converter
        """
        start_time = time.time()
        
        # Generate output path
        output_file = self.target_dir / f"{ifc_file.stem}.frag"
        
        # Check if output already exists - skip if it does
        exists, existing_file = self.check_fragments_exists(ifc_file)
        if exists:
            self.logger.info(f"⏭️  Skipping {ifc_file.name} - fragments file already exists: {existing_file.name}")
            conversion_time = time.time() - start_time
            return {
                'file': ifc_file.name,
                'status': 'skipped',
                'reason': 'Fragments file already exists',
                'output_file': str(existing_file),
                'conversion_time': conversion_time,
                'file_size_mb': ifc_file.stat().st_size / (1024 * 1024),
                'output_size_mb': existing_file.stat().st_size / (1024 * 1024) if existing_file.exists() else 0,
                'compression_ratio': 0
            }
        
        self.logger.info(f"🔄 Converting: {ifc_file.name}")
        
        # Execute portable converter
        try:
            # Use the portable converter with correct arguments
            # source_dir, target_dir, --single filename, --auto
            cmd = [sys.executable, str(self.portable_converter), 
                   str(self.source_dir), str(self.target_dir), 
                   '--single', ifc_file.name, '--auto']
            
            # Log the command being executed for debugging
            self.logger.info(f"🔧 Executing: {' '.join(cmd)}")
            
            # Execute with timeout
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  shell=False,
                                  timeout=300)  # 5 minute timeout
            
            conversion_time = time.time() - start_time
            
            # Parse the result
            if result.returncode == 0:
                # Check if output file was created successfully
                if output_file.exists() and output_file.stat().st_size > 0:
                    self.logger.info(f"✅ Successfully converted: {ifc_file.name}")
                    return self._process_successful_conversion(ifc_file, output_file, conversion_time)
                else:
                    self.logger.error(f"❌ Conversion completed but no output file created: {ifc_file.name}")
                    return self._process_failed_conversion(ifc_file, "No output file created", conversion_time)
            else:
                self.logger.error(f"❌ Conversion failed for {ifc_file.name}")
                self.logger.error(f"   Return code: {result.returncode}")
                if result.stderr:
                    self.logger.error(f"   Error: {result.stderr}")
                if result.stdout:
                    self.logger.info(f"   Output: {result.stdout}")
                return self._process_failed_conversion(ifc_file, f"Converter error: {result.stderr}", conversion_time)
                
        except subprocess.TimeoutExpired:
            conversion_time = time.time() - start_time
            self.logger.error(f"❌ Conversion timeout for {ifc_file.name} (5 minutes)")
            return self._process_failed_conversion(ifc_file, "Conversion timeout", conversion_time)
            
        except Exception as e:
            conversion_time = time.time() - start_time
            self.logger.error(f"❌ Exception during conversion of {ifc_file.name}: {e}")
            return self._process_failed_conversion(ifc_file, f"Exception: {str(e)}", conversion_time)
    
    def _process_successful_conversion(self, ifc_file: Path, output_file: Path, conversion_time: float) -> Dict:
        """Process a successful conversion"""
        input_size = ifc_file.stat().st_size
        output_size = output_file.stat().st_size
        compression_ratio = ((input_size - output_size) / input_size) * 100 if input_size > 0 else 0
        
        self.logger.info(f"   📊 Size: {input_size / (1024*1024):.2f} MB → {output_size / (1024*1024):.2f} MB")
        self.logger.info(f"   📈 Compression: {compression_ratio:.1f}%")
        self.logger.info(f"   ⏱️  Time: {conversion_time:.2f} seconds")
        
        return {
            'file': ifc_file.name,
            'status': 'success',
            'output_file': str(output_file),
            'conversion_time': conversion_time,
            'file_size_mb': input_size / (1024 * 1024),
            'output_size_mb': output_size / (1024 * 1024),
            'compression_ratio': compression_ratio
        }
    
    def _process_failed_conversion(self, ifc_file: Path, error_message: str, conversion_time: float) -> Dict:
        """Process a failed conversion"""
        input_size = ifc_file.stat().st_size
        
        return {
            'file': ifc_file.name,
            'status': 'failed',
            'error': error_message,
            'conversion_time': conversion_time,
            'file_size_mb': input_size / (1024 * 1024),
            'output_size_mb': 0,
            'compression_ratio': 0
        }
    
    def generate_report(self) -> Dict:
        """
        Generate a detailed conversion report
        """
        report = {
            'conversion_summary': {
                'timestamp': datetime.now().isoformat(),
                'source_directory': str(self.source_dir),
                'target_directory': str(self.target_dir),
                'total_files': self.stats['total_files'],
                'successful': self.stats['successful'],
                'failed': self.stats['failed'],
                'skipped': self.stats['skipped'],
                'total_time': self.stats['total_time'],
                'average_time_per_file': self.stats['total_time'] / max(self.stats['total_files'], 1)
            },
            'file_results': self.stats['results']
        }
        
        # Calculate total sizes and compression
        total_input_size = sum(r.get('file_size_mb', 0) for r in self.stats['results'])
        total_output_size = sum(r.get('output_size_mb', 0) for r in self.stats['results'] if r['status'] == 'success')
        overall_compression = ((total_input_size - total_output_size) / total_input_size) * 100 if total_input_size > 0 else 0
        
        report['conversion_summary']['total_input_size_mb'] = total_input_size
        report['conversion_summary']['total_output_size_mb'] = total_output_size
        report['conversion_summary']['overall_compression_ratio'] = overall_compression
        
        return report
    
    def save_report(self, report: Dict):
        """
        Save the conversion report to a JSON file
        """
        reports_dir = self.script_dir / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = reports_dir / f"conversion_report_{timestamp}.json"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            self.logger.info(f"📄 Conversion report saved: {report_file}")
        except Exception as e:
            self.logger.error(f"❌ Failed to save report: {e}")
    
    def run_conversion(self):
        """
        Main conversion process
        """
        try:
            self.logger.info("🚀 Starting IFC to Fragments conversion process...")
            self.stats['start_time'] = time.time()
            
            # Validate environment
            if not self.validate_environment():
                self.logger.error("❌ Environment validation failed. Exiting.")
                return False
            
            # Find IFC files
            ifc_files = self.find_ifc_files()
            if not ifc_files:
                self.logger.warning("⚠️  No IFC files found. Nothing to convert.")
                return True
            
            self.stats['total_files'] = len(ifc_files)
            
            # Process each file
            self.logger.info(f"🔄 Processing {len(ifc_files)} file(s)...")
            
            for i, ifc_file in enumerate(ifc_files, 1):
                self.logger.info(f"\n📁 Processing file {i}/{len(ifc_files)}: {ifc_file.name}")
                
                result = self.convert_single_file(ifc_file)
                self.stats['results'].append(result)
                
                # Update statistics
                if result['status'] == 'success':
                    self.stats['successful'] += 1
                elif result['status'] == 'failed':
                    self.stats['failed'] += 1
                elif result['status'] == 'skipped':
                    self.stats['skipped'] += 1
            
            # Calculate total time
            self.stats['end_time'] = time.time()
            self.stats['total_time'] = self.stats['end_time'] - self.stats['start_time']
            
            # Generate and save report
            report = self.generate_report()
            self.save_report(report)
            
            # Print final summary
            self.print_final_summary()
            
            return True
            
        except KeyboardInterrupt:
            self.logger.warning("\n⚠️  Conversion interrupted by user")
            return False
        except Exception as e:
            self.logger.error(f"❌ Unexpected error during conversion: {e}")
            return False
    
    def print_final_summary(self):
        """
        Print a final summary of the conversion process
        """
        self.logger.info("\n" + "=" * 80)
        self.logger.info("📊 CONVERSION COMPLETE - FINAL SUMMARY")
        self.logger.info("=" * 80)
        self.logger.info(f"📂 Source Directory: {self.source_dir}")
        self.logger.info(f"📁 Target Directory: {self.target_dir}")
        self.logger.info(f"📈 Files Processed: {self.stats['total_files']}")
        self.logger.info(f"✅ Successful: {self.stats['successful']}")
        self.logger.info(f"⏭️  Skipped: {self.stats['skipped']}")
        self.logger.info(f"❌ Failed: {self.stats['failed']}")
        self.logger.info(f"⏱️  Total Time: {self.stats['total_time']:.2f} seconds")
        
        if self.stats['successful'] > 0:
            avg_time = self.stats['total_time'] / self.stats['total_files']
            self.logger.info(f"⚡ Average Time per File: {avg_time:.2f} seconds")
            
            # Calculate compression statistics
            successful_results = [r for r in self.stats['results'] if r['status'] == 'success']
            if successful_results:
                total_input = sum(r['file_size_mb'] for r in successful_results)
                total_output = sum(r['output_size_mb'] for r in successful_results)
                overall_compression = ((total_input - total_output) / total_input) * 100 if total_input > 0 else 0
                
                self.logger.info(f"💾 Total Input Size: {total_input:.2f} MB")
                self.logger.info(f"🗜️  Total Output Size: {total_output:.2f} MB")
                self.logger.info(f"📉 Overall Compression: {overall_compression:.1f}%")
        
        self.logger.info("=" * 80)

def main():
    """
    Main entry point for the converter
    """
    print("🚀 IFC to Fragments Converter - Organized Directory Structure")
    print("=" * 60)
    
    converter = SimpleIfcConverter()
    success = converter.run_conversion()
    
    if success:
        print("\n✅ Conversion process completed successfully!")
        print(f"📥 Source: {converter.source_dir}")
        print(f"📤 Output: {converter.target_dir}")
        return 0
    else:
        print("\n❌ Conversion process failed or was interrupted.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
