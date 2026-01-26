# Traffic Simulation Indonesia (traffic-simulation-idn)

A comprehensive traffic simulation system designed to model Indonesian traffic patterns, detect traffic violations, and generate penalty reports. Features both CLI and GUI interfaces.

## Features

- **Traffic Simulation Engine**: Realistic simulation of vehicle movements and traffic patterns
- **Violation Detection**: Automatic detection of speed violations and traffic rule breaches
- **Penalty Calculation**: Indonesian-compliant penalty calculation system
- **Data Management**: SQLAlchemy ORM with MySQL database
- **REST API**: FastAPI/Flask web API for programmatic access
- **GUI Interface**: PyQt5-based desktop application with real-time visualization
- **Report Generation**: Export reports in CSV, PDF, and Excel formats
- **Caching System**: Redis caching for improved performance
- **Database Migrations**: Alembic for schema version management

## Project Structure

```
traffic-simulation-idn/
├── src/                    # Main source code
│   ├── core/              # Application core logic
│   ├── models/            # Data models
│   ├── database/          # Database layer
│   ├── api/               # REST API and external clients
│   ├── services/          # Business logic services
│   ├── gui/               # PyQt5 GUI application
│   ├── utils/             # Utility functions
│   └── cli/               # CLI commands
├── tests/                 # Test suite
├── config/                # Configuration files
├── docs/                  # Documentation
├── data/                  # Static data and migrations
├── scripts/               # Setup and deployment scripts
├── deployment/            # Docker and Kubernetes configs
└── outputs/               # Application outputs (logs, reports)
```

## Requirements

- Python 3.9+
- MySQL 8.0+
- Redis 6.0+
- PyQt5 (for GUI)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/traffic-simulation-idn.git
cd traffic-simulation-idn
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Initialize database
```bash
python scripts/setup/setup_database.sh
alembic upgrade head
```

## Quick Start

### CLI Mode
```bash
python src/main.py simulate --duration 3600 --vehicles 100
```

### GUI Mode
```bash
python src/main_gui.py
```

### Web API
```bash
uvicorn src.api.web.app:app --reload
```

Visit `http://localhost:8000/docs` for API documentation.

## Configuration

All configuration is managed through:
- `.env` file for environment variables
- `config/settings.py` for application settings
- `config/database.py` for database configuration
- `config/gui_config.py` for GUI settings

## Database

The system uses MySQL with the following main tables:
- `vehicles`: Vehicle information
- `owners`: Vehicle owners
- `violations`: Traffic violations detected
- `sensor_logs`: Sensor data logs
- `locations`: Traffic monitoring locations

Run migrations with:
```bash
alembic upgrade head
```

## API Endpoints

### Vehicles
- `GET /api/vehicles` - List all vehicles
- `GET /api/vehicles/{id}` - Get vehicle details
- `POST /api/vehicles` - Create new vehicle

### Violations
- `GET /api/violations` - List violations
- `GET /api/violations/{id}` - Get violation details
- `POST /api/violations` - Record new violation

### Reports
- `GET /api/reports/daily` - Daily report
- `GET /api/reports/monthly` - Monthly report
- `GET /api/reports/export` - Export data

## Testing

Run tests with pytest:
```bash
pytest                          # Run all tests
pytest tests/test_models.py     # Run specific test file
pytest --cov                    # Generate coverage report
```

## Documentation

See the `docs/` directory for detailed documentation:
- [API Documentation](docs/API_DOCUMENTATION.md)
- [Database Schema](docs/DATABASE_SCHEMA.md)
- [Setup Guide](docs/SETUP_GUIDE.md)
- [User Manual](docs/USER_MANUAL.md)
- [Architecture](docs/ARCHITECTURE.md)

## Docker

Build and run with Docker:
```bash
docker-compose up -d
```

The compose file includes:
- Application container
- MySQL database
- Redis cache

## Deployment

### Production Deployment
```bash
./scripts/deployment/build.sh
./scripts/deployment/deploy.sh
```

### Kubernetes
```bash
kubectl apply -f deployment/kubernetes/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please create an issue in the GitHub repository.

## Authors

- Traffic Simulation Team

## Changelog

### Version 1.0.0 (2024-01-26)
- Initial release
- Core simulation engine
- Database layer implementation
- REST API endpoints
- PyQt5 GUI application
- Report generation system
