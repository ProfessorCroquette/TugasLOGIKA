![Python
Logo](https://www.python.org/static/community_logos/python-logo.png)

#  Indonesian Traffic Violation Simulation System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)
![Python](https://img.shields.io/badge/python-3.8%252B-blue)
![Status](https://img.shields.io/badge/status-complete-brightgreen)
![Docs](https://img.shields.io/badge/documentation-comprehensive-blueviolet)

A project that is intended for the final exam.

This project demonstrates applied logic reasoning, system architecture
design, GUI engineering, data modeling, and simulation principles.

------------------------------------------------------------------------

## 📸 System Preview

<img width="1409" height="865" alt="image" src="https://github.com/user-attachments/assets/fc11d6f7-b7e1-4705-ba11-95300c9f7635" />


    docs/assets/gui_preview.png

------------------------------------------------------------------------

## 🧭 System Architecture


> Add your architecture diagram here:

flowchart TB

%% =========================
%% GUI Layer
%% =========================
GUI["🖥️ GUI Dashboard Layer<br/>
<b>gui_traffic_simulation.py</b> (PyQt5)<br/>
• TrafficSimulationGUI (QMainWindow)<br/>
• ViolationDetailDialog<br/>
• SimulationWorker (QThread)<br/>
• Auto-refresh every 500ms"]

%% =========================
%% Data Files
%% =========================
FILES["📁 Real-Time Data Files (JSON)<br/>
• tickets.json (Violations)<br/>
• traffic_data.json (Vehicles)<br/>
• worker_status.json (Sensors)"]

%% =========================
%% Simulation Engine
%% =========================
ENGINE["⚙️ Simulation Engine (main.py)<br/>
SpeedingTicketSimulator"]

SENSOR["🚦 TrafficSensor<br/>
• Generates vehicles<br/>
• Assigns speeds<br/>
• Detects violations<br/>
• Pushes to queue"]

PROCESSOR["🧵 QueuedCarProcessor<br/>
5 Parallel Workers<br/>
1️⃣ Queue Processing<br/>
2️⃣ Violation Detection<br/>
3️⃣ Write tickets.json<br/>
4️⃣ Update worker_status.json<br/>
5️⃣ Fine Calculation"]

ANALYZER["📊 SpeedAnalyzer<br/>
• Monitors queue<br/>
• Calculates statistics"]

DASHBOARD["🖥️ Console Dashboard<br/>
• Displays violations<br/>
• Shows statistics"]

%% =========================
%% Utilities Layer
%% =========================
GENERATOR["🔁 utils/generators.py<br/>
DataGenerator<br/>
• Random vehicles<br/>
• NIK generation<br/>
• Distribution rules"]

PLATES["🚘 utils/indonesian_plates.py<br/>
Plate Generator<br/>
• 30+ Regions<br/>
• Format: B 1234 ABC"]

FINES["💰 utils/violation_utils.py<br/>
Fine Calculator<br/>
• Base fines<br/>
• Multipliers<br/>
• USD → IDR"]

DATABASES["🗄️ Vehicle Databases<br/>
• car_database.py<br/>
• motorcycle_database.py<br/>
• model datasets"]

%% =========================
%% Connections
%% =========================
GUI --> FILES
FILES --> GUI

FILES --> ENGINE

ENGINE --> SENSOR
ENGINE --> PROCESSOR
ENGINE --> ANALYZER
ENGINE --> DASHBOARD

SENSOR --> PROCESSOR
PROCESSOR --> FILES
ANALYZER --> FILES

PROCESSOR --> FINES
PROCESSOR --> PLATES
SENSOR --> GENERATOR

GENERATOR --> DATABASES
PLATES --> DATABASES
FINES --> DATABASES


Core Components: - Traffic Sensors (5 parallel streams) - Violation
Analyzer Engine - Plate & Regional Decoder - Vehicle Generator - GUI
Dashboard - JSON Databases

------------------------------------------------------------------------

## 🚀 Quick Start

### GUI Mode

``` bash
python gui_traffic_simulation.py
```

### CLI Mode

``` bash
python main.py
```

------------------------------------------------------------------------

## 📚 Documentation Index (Quick Access)

All documentation is located inside the `/docs` directory.

  Document                    Purpose
  --------------------------- --------------------------
  FINAL_SUMMARY.md            Project overview
  ULTIMATE_DOCUMENTATION.md   Full technical reference
  API_DOCUMENTATION.md        Classes and methods
  ARCHITECTURE.md             System design
  DATABASE_SCHEMA.md          JSON structures
  SETUP_GUIDE.md              Installation
  USER_MANUAL.md              User guide

------------------------------------------------------------------------

## 🧠 Academic Framing

This project demonstrates:

-   Logical reasoning using Modus Ponens and Modus Tollens
-   Event-driven simulation design
-   Real-time GUI monitoring
-   Data persistence using JSON
-   Modular software architecture
-   Defensive programming practices
-   Scalable sensor modeling
-   Regional data integration

Suitable for: - Software Engineering coursework - Systems Modeling -
Logic Programming - Simulation Engineering - Human-Computer Interaction

------------------------------------------------------------------------

## 🛠 Technology Stack

-   Python 3.10+
-   PyQt5 / PySide6 (GUI)
-   JSON Data Storage
-   Object-Oriented Architecture
-   Modular Package Design

------------------------------------------------------------------------

## 📦 Installation

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 🧪 Validation

-   GUI stress tested with continuous vehicle generation
-   Regional plate parsing verified against dataset
-   Statistical counters validated
-   Error handling tested

------------------------------------------------------------------------

## 📜 License

Educational Use Only
