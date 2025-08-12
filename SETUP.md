# IFC to Fragments Converter - Environment Setup

## 🚀 Quick Start

### Windows Environment Setup

1. **Virtual Environment is Ready**
   ```cmd
   # The virtual environment has been created at D:\XIFC\venv\
   # To activate it manually:
   cd D:\XIFC
   venv\Scripts\activate
   
   # Or use the convenience script:
   activate_venv.bat
   ```

2. **Dependencies Installed**
   - Python 3.12.7 ✅
   - psycopg2-binary 2.9.9 ✅ (for database support)
   - tqdm 4.66.1 ✅ (for progress bars)
   - python-decouple 3.8 ✅ (for environment variables)

3. **Directory Structure**
   ```
   D:\XIFC\
   ├── data\
   │   ├── ifc\                   # Place your IFC files here
   │   └── fragments\             # Converted fragment files appear here
   ├── logs\                      # Conversion logs
   └── reports\                   # JSON conversion reports
   ```

4. **Run the Converter**
   ```cmd
   # Place IFC files in data\ifc\ directory
   # With virtual environment activated:
   python convert_ifc_to_fragments.py
   
   # Or directly:
   venv\Scripts\python.exe convert_ifc_to_fragments.py
   ```

## 📦 Docker Setup (for Containerization)

### Build and Run with Docker

```bash
# Build the Docker image
docker build -t ifc-converter .

# Run the converter (mounts data directory)
docker run -v ./data:/app/data ifc-converter

# Or use Docker Compose
docker-compose up ifc-converter
```

### With Database Support

```bash
# Start with PostgreSQL database
docker-compose --profile database up
```

## 🔧 Development Environment

### File Structure
```
D:\XIFC\
├── convert_ifc_to_fragments.py    # Main converter script
├── venv/                          # Python virtual environment
├── frag_convert/                  # Portable converter package
├── data/                          # Data directory
│   ├── ifc/                       # IFC source files
│   └── fragments/                 # Fragment output files
├── logs/                          # Conversion logs
├── reports/                       # JSON reports
├── requirements.txt               # Full dependencies
├── requirements-minimal.txt       # Essential dependencies only
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Docker Compose setup
├── .env.example                   # Environment variables template
├── activate_venv.bat              # Windows activation script
└── activate_venv.sh               # Linux/Mac activation script
```

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
# Database (optional)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ifc_fragments

# Converter settings
CONVERTER_LOG_LEVEL=INFO
CONVERTER_TIMEOUT=300
AUTO_SKIP_EXISTING=true

# Paths
SOURCE_DIRECTORY=./data/ifc
OUTPUT_DIRECTORY=./data/fragments
```

## 📁 Usage Workflow

1. **Place IFC files** in `data/ifc/` directory
2. **Run converter**: `python convert_ifc_to_fragments.py`
3. **Find output** in `data/fragments/` directory
4. **Check logs** in `logs/` directory
5. **Review reports** in `reports/` directory

## 🐳 Dockerization Features

### Volume Mounts
- `./data` → `/app/data` (for IFC files and fragments)
- `./logs` → `/app/logs` (for logs)
- `./reports` → `/app/reports` (for reports)

### Environment Variables
- `PYTHONUNBUFFERED=1`: Real-time output
- `CONVERTER_LOG_LEVEL=INFO`: Logging level
- `PYTHONPATH=/app`: Python path configuration

## 🚀 Usage Examples

### Local Development
```cmd
# 1. Activate environment
activate_venv.bat

# 2. Place IFC files in data\ifc\

# 3. Run converter
python convert_ifc_to_fragments.py

# 4. Check results in data\fragments\
```

### Docker
```bash
# Quick run
docker run -v ./data:/app/data ifc-converter

# With custom settings
docker run -e CONVERTER_LOG_LEVEL=DEBUG -v ./data:/app/data ifc-converter

# Interactive mode
docker run -it -v ./data:/app/data ifc-converter bash
```

### Docker Compose
```bash
# Convert files only
docker-compose up ifc-converter

# With database
docker-compose --profile database up

# Rebuild and run
docker-compose up --build
```

## 🔍 Verification

### Check Virtual Environment
```cmd
venv\Scripts\python.exe --version
venv\Scripts\pip list
```

### Test Converter
```cmd
# 1. Place an IFC file in data\ifc\
# 2. Run:
venv\Scripts\python.exe convert_ifc_to_fragments.py
# 3. Check data\fragments\ for output
```

### Check Docker
```bash
docker build -t ifc-converter .
docker run --rm ifc-converter python --version
```

## �️ Troubleshooting

### Common Issues

1. **No IFC files found**
   ```cmd
   # Solution: Place IFC files in data/ifc/ directory
   copy "C:\path\to\your\file.ifc" "data\ifc\"
   ```

2. **Virtual Environment not activated**
   ```cmd
   # Solution:
   cd D:\XIFC
   venv\Scripts\activate
   ```

3. **Missing directories**
   ```cmd
   # Solution: The script creates them automatically, or:
   mkdir data\ifc
   mkdir data\fragments
   ```

4. **Permission issues in Docker**
   ```bash
   # Solution: Use non-root user (already configured)
   docker run --user 1000:1000 -v ./data:/app/data ifc-converter
   ```

## ✅ Ready to Use!

The environment is now fully configured with organized directory structure:
- ✅ **data/ifc/** - Source IFC files
- ✅ **data/fragments/** - Output fragment files  
- ✅ **logs/** - Conversion logs
- ✅ **reports/** - JSON reports
- ✅ Local development and testing
- ✅ Docker containerization
- ✅ Production deployment
- ✅ Database integration (when needed)
- ✅ CI/CD pipeline integration
