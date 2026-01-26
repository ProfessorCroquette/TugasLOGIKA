# Setup Guide

## System Requirements

- Python 3.9 or higher
- MySQL 8.0 or higher
- Redis 6.0 or higher
- 4GB RAM minimum
- 10GB disk space

## Installation Steps

### 1. Prerequisites

#### Windows
```powershell
# Install Python 3.11
# Download from https://www.python.org/downloads/

# Install MySQL
# Download from https://dev.mysql.com/downloads/mysql/

# Install Redis (using WSL or Docker)
# Or download from https://github.com/microsoftarchive/redis/releases
```

#### Linux/Mac
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.11 python3-pip mysql-server redis-server

# macOS
brew install python@3.11 mysql redis
```

### 2. Clone Repository
```bash
git clone https://github.com/ProfessorCroquette/TugasLOGIKA.git
cd TugasLOGIKA/traffic-simulation-idn
```

### 3. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3.11 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor
```

Key settings to configure:
- `DB_HOST`, `DB_USER`, `DB_PASSWORD`
- `REDIS_HOST`, `REDIS_PORT`
- `SMTP_` settings for email
- `TWILIO_` settings for SMS

### 6. Database Setup

#### Create Database and User
```bash
mysql -u root -p

CREATE DATABASE traffic_simulation;
CREATE USER 'traffic_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON traffic_simulation.* TO 'traffic_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### Run Migrations
```bash
alembic upgrade head
```

#### Seed Initial Data
```bash
python scripts/setup/setup_database.sh
```

### 7. Verify Installation

```bash
# Test GUI launch
python gui_traffic_simulation.py

# Test CLI (main simulation)
python main.py &

# Run tests (if available)
pytest tests/ -v
```

## Running the Application

### GUI Mode (Recommended)
```bash
python gui_traffic_simulation.py
```
Launches the PyQt5 GUI application with real-time traffic simulation display.

### CLI Mode (Background Simulation)
```bash
python main.py
```
Runs the core simulation engine in the background, continuously updating JSON data files (traffic_data.json, tickets.json).

## Docker Setup

### Using Docker Compose
```bash
docker-compose up -d
```

This will start:
- MySQL database (port 3306)
- Application services (traffic simulation)

Check logs:
```bash
docker-compose logs -f
```

## Troubleshooting

### Database Connection Error
- Verify MySQL is running: `mysql -u root -p -e "SELECT 1"`
- Check credentials in `.env`
- Ensure database exists: `mysql -u root -p -e "SHOW DATABASES"`

### Redis Connection Error
- Verify Redis is running: `redis-cli ping`
- Check host and port in `.env`
- On Windows, consider using WSL or Docker

### Port Already in Use
```bash
# Find and kill process using port
# Linux/Mac: lsof -i :8000
# Windows: netstat -ano | findstr :8000
```

### Import Errors
```bash
# Reinstall in development mode
pip install -e .
# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

## Log Cleanup

The application automatically manages log files:
- **Location**: `logs/` directory
- **Cleanup Trigger**: Automatic on every application startup
- **Max Files Kept**: 10 (oldest logs deleted when exceeded)
- **Log Names**: `simulation_YYYYMMDD_HHMMSS.log`

This prevents unlimited disk space usage during long-running simulations.

## Next Steps

1. Read the [User Manual](USER_MANUAL.md)
2. Review [Architecture](ARCHITECTURE.md)
3. See [Database Schema](DATABASE_SCHEMA.md)
