POWERED BY <a href="https://www.python.org" target="_blank">
  <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png" 
       alt="Python Logo" 
       height="60">
</a>


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

## ---System Preview---

<img width="1409" height="865" alt="image" src="https://github.com/user-attachments/assets/fc11d6f7-b7e1-4705-ba11-95300c9f7635" />


    docs/assets/gui_preview.png

------------------------------------------------------------------------

## ---System Architecture---



<img width="2613" height="1530" alt="mermaid-diagram-2026-01-29-062157" src="https://github.com/user-attachments/assets/4a028dbc-b6be-4f41-8269-3cef82ad181f" />




Core Components: - Traffic Sensors (5 parallel streams) - Violation
Analyzer Engine - Plate & Regional Decoder - Vehicle Generator - GUI
Dashboard - JSON Databases

------------------------------------------------------------------------

##  Quick Start

### GUI Mode

``` bash
python gui_traffic_simulation.py
```

### CLI Mode

``` bash
python main.py
```

------------------------------------------------------------------------

## Documentation Index (Quick Access)

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

## WHAT IS THIS PROJECT FOR?

This project demonstrates:

-   Logical reasoning using Modus Ponens and Modus Tollens
-   Event-driven simulation design
-   Real-time GUI monitoring
-   Data persistence using JSON
-   Modular software architecture
-   Defensive programming practices
-   Scalable sensor modeling
-   Regional data integration
-   Demonstrate simple AI logic using near-realistic simulation
------------------------------------------------------------------------

## Technology Stack

-   Python 3.10+
-   PyQt5 / PySide6 (GUI)
-   JSON Data Storage
-   Object-Oriented Architecture
-   Modular Package Design

------------------------------------------------------------------------

## Installation

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## Validation

-   GUI stress tested with continuous vehicle generation
-   Regional plate parsing verified against the dataset
-   Statistical counters validated
-   Error handling tested
-   Log handling

------------------------------------------------------------------------

## License
MIT License

Copyright (c) 2026 ProfessorCroquette / Delfitra Anugerah S

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
Educational Use Only
