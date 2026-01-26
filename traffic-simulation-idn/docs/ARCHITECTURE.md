# System Architecture

## Overview

Traffic Simulation Indonesia is a layered architecture application with three main interfaces:

1. **CLI Interface** - Command-line tool for batch operations
2. **GUI Interface** - PyQt5 desktop application for interactive use
3. **REST API** - FastAPI/Flask for programmatic access

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interfaces Layer                     │
├──────────────────┬──────────────────┬──────────────────────┤
│   CLI Commands   │   PyQt5 GUI      │   REST API (FastAPI) │
│   (main.py)      │   (main_gui.py)  │   (app.py)           │
└────────┬─────────┴────────┬─────────┴──────────┬────────────┘
         │                  │                     │
         └──────────────────┼─────────────────────┘
                            │
         ┌──────────────────▼─────────────────────┐
         │      Application Core Layer            │
         ├──────────────────────────────────────┤
         │ Application Controller (core/)        │
         │ Simulation Engine                    │
         │ Event Bus                            │
         │ Config Manager                       │
         └──────────────┬───────────────────────┘
                        │
         ┌──────────────▼───────────────────────┐
         │      Services Layer                   │
         ├──────────────────────────────────────┤
         │ Generators    Analyzers              │
         │ Notifiers     Exporters              │
         └──────────────┬───────────────────────┘
                        │
         ┌──────────────▼───────────────────────┐
         │      Data Access Layer               │
         ├──────────────────────────────────────┤
         │ Repositories (CRUD Operations)       │
         │ Database Models (SQLAlchemy ORM)     │
         │ Session Management                   │
         └──────────────┬───────────────────────┘
                        │
         ┌──────────────▼───────────────────────┐
         │    Database & Cache Layer            │
         ├──────────────────────────────────────┤
         │ MySQL Database                       │
         │ Redis Cache                          │
         │ External APIs (RapidAPI, Twilio)     │
         └──────────────────────────────────────┘
```

## Component Details

### 1. User Interface Layer

#### CLI (src/main.py)
- Command-line interface using argparse
- Suitable for batch operations and automation
- Supports scripting and cron jobs

#### GUI (src/main_gui.py)
- PyQt5-based desktop application
- Responsive UI with real-time updates
- Dashboard, simulation control, reports generation

#### REST API (src/api/web/app.py)
- FastAPI server on port 8000
- Automatic API documentation (Swagger/OpenAPI)
- Authentication middleware
- CORS support for web clients

### 2. Core Application Layer

**src/core/application.py**
- Main application controller
- Orchestrates components
- Lifecycle management

**src/core/simulation_engine.py**
- Traffic simulation logic
- Vehicle movement calculations
- Violation detection

**src/core/event_bus.py**
- Event-driven communication
- Publish/subscribe pattern
- Decouples components

**src/core/config_manager.py**
- Configuration loading
- Environment variables
- Settings validation

### 3. Services Layer

#### Generators (src/services/generators/)
- **vehicle_generator.py**: Creates synthetic vehicle data
- **owner_generator.py**: Indonesian owner information
- **violation_generator.py**: Simulates violations
- **plate_generator.py**: Realistic license plates

#### Analyzers (src/services/analyzers/)
- **speed_analyzer.py**: Detects speed violations
- **penalty_calculator.py**: Calculates fines
- **document_validator.py**: Validates STNK/SIM

#### Notifiers (src/services/notifiers/)
- **email_notifier.py**: Send email alerts
- **sms_notifier.py**: SMS via Twilio
- **console_notifier.py**: Console output

#### Exporters (src/services/exporters/)
- **csv_exporter.py**: CSV format
- **pdf_exporter.py**: PDF reports
- **excel_exporter.py**: Excel spreadsheets

### 4. Data Access Layer

**src/database/repositories/**
- Base repository pattern (CRUD)
- Vehicle, Owner, Violation repositories
- Sensor data repository
- Query optimization

**src/models/**
- SQLAlchemy ORM models
- Relationships definition
- Enumerations for types

**src/database/session.py**
- Session factory
- Connection pooling
- Transaction management

### 5. Database & Cache Layer

**MySQL Database**
- Primary data store
- Tables: vehicles, owners, violations, sensors, locations
- Indexes for performance
- Referential integrity

**Redis Cache**
- Session caching
- API response caching
- Real-time data buffering

**External APIs**
- RapidAPI for car data
- Geolocation services
- Email/SMS providers

## Data Flow

### Simulation Flow
```
User Input
    ↓
CLI/GUI Handler
    ↓
Simulation Engine
    ├→ Vehicle Generator
    ├→ Movement Calculator
    ├→ Sensor Logs
    └→ Violation Detector
         ├→ Speed Analyzer
         ├→ Penalty Calculator
         └→ Notifier
             └→ Database Storage
```

### Report Generation Flow
```
User Request
    ↓
Report Handler
    ├→ Query Database
    ├→ Analyzer (calculations)
    ├→ Formatter
    └→ Exporter
        └→ Output File
```

## Design Patterns Used

1. **Repository Pattern**: Data access abstraction
2. **Service Layer**: Business logic separation
3. **Event Bus**: Loose coupling between components
4. **Factory Pattern**: Object creation
5. **Singleton**: Config manager, database connection
6. **Observer**: GUI updates from model changes

## Scalability Considerations

- **Horizontal Scaling**: Multiple API instances with load balancer
- **Database Replication**: MySQL master-slave setup
- **Caching**: Redis for frequently accessed data
- **Async Processing**: Celery for long-running tasks
- **Message Queue**: RabbitMQ for event handling

## Security Features

- Environment variable configuration
- Password hashing for sensitive data
- API token authentication
- SQL injection prevention via ORM
- CORS configuration
- Input validation and sanitization

## Performance Optimizations

- Database indexes on frequently queried columns
- Redis caching for API responses
- Connection pooling
- Lazy loading in ORM
- Pagination for large result sets
- Query optimization

## Testing Architecture

```
tests/
├── test_models.py          # Unit tests for models
├── test_services.py        # Service layer tests
├── test_database.py        # Repository tests
├── test_api.py             # API endpoint tests
├── test_gui.py             # GUI component tests
└── integration/
    ├── test_simulation_flow.py
    └── test_database_integration.py
```

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│          Load Balancer (Nginx)          │
└────────────────────┬────────────────────┘
                     │
     ┌───────────────┼───────────────┐
     ▼               ▼               ▼
┌─────────┐    ┌─────────┐    ┌─────────┐
│ App 1   │    │ App 2   │    │ App 3   │
│(Docker) │    │(Docker) │    │(Docker) │
└────┬────┘    └────┬────┘    └────┬────┘
     │              │              │
     └──────────────┼──────────────┘
                    │
            ┌───────┴────────┐
            ▼                ▼
        ┌────────┐      ┌────────┐
        │ MySQL  │      │ Redis  │
        │Cluster │      │Cluster │
        └────────┘      └────────┘
```

## Technologies Used

- **Language**: Python 3.9+
- **Web Frameworks**: FastAPI, Flask
- **GUI**: PyQt5
- **ORM**: SQLAlchemy
- **Database**: MySQL 8.0
- **Cache**: Redis
- **Testing**: pytest
- **Deployment**: Docker, Kubernetes, Nginx
