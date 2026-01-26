# API Documentation

## Overview

The Traffic Simulation Indonesia API provides REST endpoints for accessing vehicle data, violations, and generating reports.

## Base URL

```
http://localhost:8000/api
```

## Authentication

Currently, basic authentication is used. All requests must include:
```
Authorization: Bearer <token>
```

## Endpoints

### Vehicles

#### List Vehicles
```
GET /vehicles
```

Query Parameters:
- `limit`: Number of results (default: 100)
- `offset`: Result offset (default: 0)
- `status`: Filter by status (active, inactive)

Response:
```json
{
  "data": [
    {
      "id": 1,
      "plate": "B 1234 ABC",
      "type": "sedan",
      "owner_id": 1,
      "status": "active"
    }
  ],
  "total": 150,
  "limit": 100,
  "offset": 0
}
```

#### Get Vehicle Details
```
GET /vehicles/{id}
```

#### Create Vehicle
```
POST /vehicles
Content-Type: application/json

{
  "plate": "B 1234 ABC",
  "type": "sedan",
  "owner_id": 1
}
```

### Violations

#### List Violations
```
GET /violations
```

Query Parameters:
- `vehicle_id`: Filter by vehicle
- `violation_type`: speed, parking, red_light, etc.
- `start_date`: Filter from date (ISO 8601)
- `end_date`: Filter to date (ISO 8601)

#### Record Violation
```
POST /violations
Content-Type: application/json

{
  "vehicle_id": 1,
  "type": "speed",
  "speed": 75,
  "speed_limit": 60,
  "location": "Jalan Sudirman",
  "timestamp": "2024-01-26T10:30:00Z"
}
```

### Reports

#### Daily Report
```
GET /reports/daily?date=2024-01-26
```

#### Monthly Report
```
GET /reports/monthly?year=2024&month=1
```

#### Export Data
```
GET /reports/export?format=csv&type=violations
```

Formats: csv, pdf, excel

## Error Responses

All errors follow this format:
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Description of the error",
    "details": {}
  }
}
```

## Rate Limiting

API is rate limited to 1000 requests per hour per IP address.

## Pagination

Responses use limit/offset pagination:
- `limit`: Items per page
- `offset`: Number of items to skip
- `total`: Total number of items available
