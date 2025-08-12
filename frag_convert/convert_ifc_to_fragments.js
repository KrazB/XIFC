/**
 * IFC to Fragments Converter - Node.js Implementation
 * Based on ThatOpen Components official examples
 * Repository: https://github.com/ThatOpen/engine_fragment
 * Tutorial: https://docs.thatopen.com/Tutorials/Fragments/Fragments/IfcImporter
 */

import * as fs from 'fs';
import * as path from 'path';
import pkg from '@thatopen/fragments';
const { IfcImporter } = pkg;

class IfcFragmentsConverter {  constructor() {
    this.serializer = new IfcImporter();
    
    // Configure WASM path for Node.js environment using absolute path
    const currentDir = process.cwd();
    this.serializer.wasm.path = `${currentDir}/node_modules/web-ifc/`;
    this.serializer.wasm.absolute = true;
  }

  /**
   * Convert IFC file to Fragments format
   * @param {string} ifcPath - Path to input IFC file
   * @param {string} outputPath - Path for output fragment file
   * @returns {Promise<{success: boolean, message: string, stats?: object}>}
   */
  async convertIfcToFragments(ifcPath, outputPath) {
    let input = null;
    const startTime = Date.now();
    
    try {      console.log(`[START] Starting conversion: ${path.basename(ifcPath)}`);
      
      // Validate input file
      if (!fs.existsSync(ifcPath)) {
        throw new Error(`IFC file not found: ${ifcPath}`);
      }
      
      const stats = fs.statSync(ifcPath);
      const fileSizeMB = (stats.size / (1024 * 1024)).toFixed(2);
      console.log(`[INFO] File size: ${fileSizeMB} MB`);
      
      // Setup streaming read callback for efficient memory usage
      input = fs.openSync(ifcPath, 'r');
      let fileFinishedReading = false;
      let previousOffset = -1;
      
      const readCallback = (offset, size) => {
        if (!fileFinishedReading) {          if (offset < previousOffset) {
            fileFinishedReading = true;
            console.log(`[INFO] File reading completed, starting conversion...`);
          }
          previousOffset = offset;
        }
        
        const data = new Uint8Array(size);
        const bytesRead = fs.readSync(input, data, 0, size, offset);
        
        if (bytesRead <= 0) {
          return new Uint8Array(0);
        }
        
        return data;
      };
        // Process IFC to fragments using streaming approach
      console.log(`[PROCESS] Processing IFC geometry and properties...`);
      const fragmentData = await this.serializer.process({
        readFromCallback: true,
        readCallback,
        raw: false // Use compression for smaller output files
      });
      
      // Write fragments file
      console.log(`[SAVE] Writing fragments file: ${path.basename(outputPath)}`);
      fs.writeFileSync(outputPath, fragmentData);
      
      // Calculate conversion stats
      const endTime = Date.now();
      const conversionTime = ((endTime - startTime) / 1000).toFixed(2);
      const outputStats = fs.statSync(outputPath);
      const outputSizeMB = (outputStats.size / (1024 * 1024)).toFixed(2);
      const compressionRatio = ((1 - outputStats.size / stats.size) * 100).toFixed(1);
      
      const conversionStats = {
        inputSizeMB: fileSizeMB,
        outputSizeMB: outputSizeMB,
        compressionRatio: `${compressionRatio}%`,
        conversionTimeSeconds: conversionTime,
        success: true
      };
        console.log(`[OK] Conversion completed successfully`);
      console.log(`   [STATS] Input: ${fileSizeMB} MB -> Output: ${outputSizeMB} MB`);
      console.log(`   [COMPRESS] Compression: ${compressionRatio}%`);
      console.log(`   [TIME] Time: ${conversionTime}s`);
      
      return {
        success: true,
        message: `Successfully converted ${path.basename(ifcPath)} to fragments`,
        stats: conversionStats
      };
        } catch (error) {
      const errorMessage = `Failed to convert ${path.basename(ifcPath)}: ${error.message}`;
      console.error(`[ERROR] ${errorMessage}`);
      console.error(`   Error details:`, error);
      
      return {
        success: false,
        message: errorMessage,
        error: error.message
      };
      
    } finally {
      // Clean up file handle
      if (input !== null) {
        try {
          fs.closeSync(input);        } catch (closeError) {
          console.warn(`[WARN] Warning: Could not close file handle: ${closeError.message}`);
        }
      }
    }
  }
}

/**
 * Command line interface
 * Usage: node convert_ifc_to_fragments.js <ifcFilePath> [outputPath]
 */
async function main() {
  const args = process.argv.slice(2);
    if (args.length === 0) {
    console.log(`
[INFO] IFC to Fragments Converter
Usage: node convert_ifc_to_fragments.js <ifcFilePath> [outputPath]

Arguments:
  ifcFilePath    Path to the input IFC file
  outputPath     Path for output fragment file (optional)
                 If not specified, uses same directory with .frag extension

Examples:
  node convert_ifc_to_fragments.js ./model.ifc
  node convert_ifc_to_fragments.js ./model.ifc ./output/model.frag
`);
    process.exit(1);
  }
  
  const ifcPath = path.resolve(args[0]);
  
  // Generate output path if not provided
  let outputPath;
  if (args.length >= 2) {
    outputPath = path.resolve(args[1]);
  } else {
    const baseName = path.basename(ifcPath, path.extname(ifcPath));
    outputPath = path.join(path.dirname(ifcPath), `${baseName}.frag`);
  }
  
  // Ensure output directory exists
  const outputDir = path.dirname(outputPath);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  const converter = new IfcFragmentsConverter();
  const result = await converter.convertIfcToFragments(ifcPath, outputPath);
  
  // Output result as JSON for Python script consumption
  console.log('CONVERSION_RESULT_JSON:', JSON.stringify(result));
  
  process.exit(result.success ? 0 : 1);
}

// Run main function if script is executed directly
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const isMainModule = process.argv[1] === __filename;

if (isMainModule) {
  main().catch(error => {
    console.error('[ERROR] Unexpected error:', error);
    process.exit(1);
  });
}

export { IfcFragmentsConverter };
