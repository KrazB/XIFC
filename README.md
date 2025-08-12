# XIFC - IFC to Fragments Converter

🚀 **Professional IFC to Fragments converter with organized directory structure and Docker support.**

## � Quick Start for Windows Users

### Prerequisites
- **Git**: [Download Git for Windows](https://git-scm.com/download/win)
- **Docker Desktop**: [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)

### 🔄 Clone and Run (3 simple steps)

```cmd
# 1. Clone the repository
git clone https://github.com/KrazB/XIFC.git
cd XIFC

# 2. Place your IFC files
copy "your_model.ifc" "data\ifc\"

# 3. Run with Docker
docker-compose up ifc-converter
```

**That's it!** Your converted fragments will appear in `data\fragments\`

## 🐳 Docker Options

### Option 1: Docker Compose (Recommended)
```cmd
# Convert files
docker-compose up ifc-converter

# With database support
docker-compose --profile database up

# Rebuild and run
docker-compose up --build
```

### Option 2: Docker Build & Run
```cmd
# Build the image
docker build -t xifc-converter .

# Run conversion
docker run -v "%cd%\data:/app/data" xifc-converter
```

### Option 3: Interactive Mode
```cmd
# Run interactively for debugging
docker run -it -v "%cd%\data:/app/data" xifc-converter bash
```

## 📁 Directory Structure

```
XIFC/
├── 📥 data/
│   ├── ifc/                       # Place your IFC files here
│   └── fragments/                 # Converted fragments appear here
├── 📊 logs/                       # Conversion logs
├── 📈 reports/                    # JSON conversion reports
├──  frag_convert/               # Converter engine
├── 🐳 Dockerfile                  # Docker configuration
├── 🐳 docker-compose.yml          # Docker orchestration
└── 📄 convert_ifc_to_fragments.py # Main script
```

## ✨ Features

- **🗂️ Organized Structure**: Clean separation of input/output files
- **⏭️ Smart Skipping**: Automatically skips already converted files
- **📊 Detailed Logging**: Comprehensive logs and JSON reports
- **🐳 Docker Ready**: No local Python setup required
- **🔄 Progress Tracking**: Real-time conversion progress
- **❌ Error Handling**: Graceful error recovery
- **📈 Statistics**: Compression ratios and performance metrics

## � Local Development (Optional)

If you prefer local Python development:

### Windows Setup
```cmd
# 1. Clone repository
git clone https://github.com/KrazB/XIFC.git
cd XIFC

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements-minimal.txt

# 4. Run converter
python convert_ifc_to_fragments.py
```

### Linux/Mac Setup
```bash
# 1. Clone repository
git clone https://github.com/KrazB/XIFC.git
cd XIFC

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements-minimal.txt

# 4. Run converter
python convert_ifc_to_fragments.py
```

## 📊 Example Output

```
🚀 IFC to Fragments Converter - Organized Directory Structure
============================================================
� Source: /app/data/ifc
� Output: /app/data/fragments
📋 Found 3 IFC file(s):
   1. Building_Model.ifc (245.67 MB)
   2. Structure_Model.ifc (156.23 MB)
   3. MEP_Model.ifc (89.45 MB)

🔄 Processing 3 file(s)...
✅ Successfully converted: Building_Model.ifc
   📊 Size: 245.67 MB → 24.12 MB
   📈 Compression: 90.2%
   ⏱️  Time: 2.8 seconds

📊 CONVERSION COMPLETE - FINAL SUMMARY
✅ Successful: 3
⏭️  Skipped: 0
❌ Failed: 0
📉 Overall Compression: 91.5%
```

## 🛠️ Configuration

### Environment Variables
Copy `.env.example` to `.env` for custom configuration:
```bash
# Database (optional)
DB_HOST=localhost
DB_PORT=5432

# Converter settings
CONVERTER_LOG_LEVEL=INFO
CONVERTER_TIMEOUT=300
```

### Docker Environment Variables
```cmd
# Custom log level
docker run -e CONVERTER_LOG_LEVEL=DEBUG -v "%cd%\data:/app/data" xifc-converter

# Custom timeout
docker run -e CONVERTER_TIMEOUT=600 -v "%cd%\data:/app/data" xifc-converter
```

## 🔍 File Types

| Extension | Description | Location |
|-----------|-------------|----------|
| `.ifc` | Industry Foundation Classes files | `data/ifc/` |
| `.frag` | Compressed fragment files | `data/fragments/` |
| `.log` | Conversion logs | `logs/` |
| `.json` | Conversion reports | `reports/` |

## 🛠️ Troubleshooting

### Common Issues

#### 1. No IFC files found
```cmd
# Make sure files are in the right place:
dir data\ifc\*.ifc
```

#### 2. Docker permission issues
```cmd
# Make sure Docker Desktop is running
# Try running as administrator if needed
```

#### 3. Large file conversion timeout
```cmd
# Increase timeout for large files
docker run -e CONVERTER_TIMEOUT=1200 -v "%cd%\data:/app/data" xifc-converter
```

#### 4. Out of disk space
```cmd
# Clean up Docker images if needed
docker system prune

# Check available space
docker system df
```

### Windows-Specific Notes

- Use `"%cd%\data:/app/data"` for volume mounting in cmd
- Use `"${PWD}/data:/app/data"` for volume mounting in PowerShell
- Ensure Docker Desktop is running before executing commands
- Windows Defender might scan large IFC files - add data folder to exclusions for better performance

## 📚 Documentation

- [`SETUP.md`](SETUP.md) - Detailed setup instructions
- [`ENVIRONMENT_SUMMARY.md`](ENVIRONMENT_SUMMARY.md) - Environment overview
- [`frag_convert/README.md`](frag_convert/README.md) - Converter package documentation

## � Performance

- **Compression**: Typically 85-95% size reduction
- **Speed**: ~1-2 seconds per MB of IFC data
- **Memory**: Efficient streaming for large files
- **Supported**: Files up to several GB

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- **Repository**: https://github.com/KrazB/XIFC
- **Issues**: https://github.com/KrazB/XIFC/issues
- **ThatOpen Components**: https://github.com/ThatOpen/engine_components

---

**Ready to convert your IFC files? Just clone, add files to `data/ifc/`, and run!** 🚀
