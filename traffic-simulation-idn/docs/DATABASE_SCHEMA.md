# Database Schema

## Tables

### vehicles
Stores information about vehicles in the system.

| Column | Type | Key | Description |
|--------|------|-----|-------------|
| id | INT | PK | Vehicle ID |
| plate | VARCHAR(20) | UNIQUE | License plate number |
| type | VARCHAR(50) | | Vehicle type (sedan, truck, etc) |
| owner_id | INT | FK | Reference to owner |
| brand | VARCHAR(50) | | Vehicle brand |
| model | VARCHAR(50) | | Vehicle model |
| year | INT | | Year of manufacture |
| status | ENUM | | active, inactive |
| created_at | DATETIME | | Creation timestamp |
| updated_at | DATETIME | | Last update timestamp |

### owners
Stores vehicle owner information.

| Column | Type | Key | Description |
|--------|------|-----|-------------|
| id | INT | PK | Owner ID |
| name | VARCHAR(255) | | Owner name |
| email | VARCHAR(255) | | Email address |
| phone | VARCHAR(20) | | Phone number |
| address | TEXT | | Physical address |
| nik | VARCHAR(20) | UNIQUE | National ID number |
| created_at | DATETIME | | Creation timestamp |

### violations
Records traffic violations.

| Column | Type | Key | Description |
|--------|------|-----|-------------|
| id | INT | PK | Violation ID |
| vehicle_id | INT | FK | Reference to vehicle |
| type | VARCHAR(50) | | Violation type |
| speed | INT | | Speed recorded |
| speed_limit | INT | | Speed limit |
| location | VARCHAR(255) | | Violation location |
| timestamp | DATETIME | | When violation occurred |
| penalty | DECIMAL | | Fine amount |
| status | ENUM | | pending, paid, disputed |
| created_at | DATETIME | | Creation timestamp |

### sensor_logs
Stores sensor data readings.

| Column | Type | Key | Description |
|--------|------|-----|-------------|
| id | INT | PK | Log ID |
| location_id | INT | FK | Location reference |
| vehicle_id | INT | FK | Vehicle reference |
| speed | INT | | Speed reading |
| timestamp | DATETIME | | Reading timestamp |

### locations
Traffic monitoring locations.

| Column | Type | Key | Description |
|--------|------|-----|-------------|
| id | INT | PK | Location ID |
| name | VARCHAR(255) | | Location name |
| latitude | DECIMAL | | GPS latitude |
| longitude | DECIMAL | | GPS longitude |
| speed_limit | INT | | Speed limit |
| city | VARCHAR(100) | | City name |

## Indexes

Performance indexes are created on:
- violations.vehicle_id
- violations.timestamp
- sensor_logs.location_id
- sensor_logs.timestamp
- vehicles.status

## Relationships

```
vehicles (1) --- (*) violations
owners (1) --- (*) vehicles
locations (1) --- (*) sensor_logs
vehicles (1) --- (*) sensor_logs
```
