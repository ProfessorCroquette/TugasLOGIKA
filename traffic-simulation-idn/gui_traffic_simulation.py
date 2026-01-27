"""
Qt5 GUI for Indonesian Traffic Violation Simulation
Displays real-time violations with owner information and Rupiah currency
"""

import sys
import json
import subprocess
import time
import os
import signal
from pathlib import Path
from typing import Dict

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSpinBox, QTableWidget, QTableWidgetItem,
    QDialog, QGroupBox, QGridLayout, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QBrush

from config import Config
from utils.logger import logger

# Define currency conversion as a module-level variable
USD_TO_IDR = 15500  # 1 USD = 15,500 IDR


class SignalEmitter(QObject):
    """Emits signals from simulation threads"""
    violation_detected = pyqtSignal(dict)
    simulation_started = pyqtSignal()
    simulation_stopped = pyqtSignal()
    stats_updated = pyqtSignal(dict)
    simulation_finished = pyqtSignal()


class SimulationWorker(QThread):
    """Background thread for running simulation"""
    
    def __init__(self):
        super().__init__()
        self.running = True
        self.emitter = SignalEmitter()
        self.process = None
        
    def run(self):
        """Run the simulation continuously"""
        self.emitter.simulation_started.emit()
        
        try:
            # Run main.py without duration (continuous until stopped)
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.process = subprocess.Popen(
                [sys.executable, "main.py"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=current_dir
            )
            
            # Monitor the process while emitting stats
            while self.running:
                if self.process.poll() is not None:
                    # Process finished
                    break
                stats = self._get_current_stats()
                self.emitter.stats_updated.emit(stats)
                time.sleep(1)  # Check every 1 second
            
            # Wait for process to finish with longer timeout
            if self.process and self.process.poll() is None:
                try:
                    self.process.wait(timeout=30)
                except subprocess.TimeoutExpired:
                    self.process.terminate()
            
            # Final stats
            stats = self._get_current_stats()
            self.emitter.stats_updated.emit(stats)
            
        except Exception as e:
            print(f"Simulation error: {e}")
        finally:
            self.emitter.simulation_finished.emit()
    
    def _get_current_stats(self) -> Dict:
        """Get current simulation statistics"""
        try:
            violations_file = Path("data_files/tickets.json")
            vehicles_file = Path("data_files/traffic_data.json")
            
            violations = []
            vehicles = []
            
            if violations_file.exists():
                try:
                    with open(violations_file, 'r') as f:
                        violations = json.load(f) or []
                except:
                    violations = []
            
            if vehicles_file.exists():
                with open(vehicles_file, 'r') as f:
                    vehicles = json.load(f) or []
            
            total_fines = sum(t.get('fine_amount', 0) for t in violations)
            
            speeds = []
            for v in violations:
                if 'speed' in v:
                    speeds.append(v['speed'])
            
            avg_speed = sum(speeds) / len(speeds) if speeds else 0
            max_speed = max(speeds) if speeds else 0
            
            return {
                'violations_count': len(violations),
                'vehicles_processed': len(vehicles),
                'total_fines_usd': total_fines,
                'total_fines_idr': total_fines * USD_TO_IDR,
                'avg_speed': avg_speed,
                'max_speed': max_speed
            }
        except Exception as e:
            return {
                'violations_count': 0,
                'vehicles_processed': 0,
                'total_fines_usd': 0,
                'total_fines_idr': 0,
                'avg_speed': 0,
                'max_speed': 0
            }
    
    def stop(self):
        """Stop the simulation"""
        self.running = False
        
        if self.process:
            try:
                # Try graceful termination first
                logger.info(f"Terminating subprocess (PID: {self.process.pid})")
                
                if os.name == 'nt':  # Windows
                    # Use taskkill for more reliable Windows termination
                    import subprocess as sp
                    sp.Popen(['taskkill', '/PID', str(self.process.pid), '/T', '/F'],
                            stdout=sp.DEVNULL, stderr=sp.DEVNULL)
                    
                    try:
                        self.process.wait(timeout=2)
                        logger.info("Process terminated on Windows")
                    except subprocess.TimeoutExpired:
                        logger.warning("Process didn't stop on Windows")
                else:  # Linux/Mac
                    self.process.terminate()
                    try:
                        self.process.wait(timeout=3)
                        logger.info("Process terminated gracefully")
                    except subprocess.TimeoutExpired:
                        logger.warning("Process didn't stop gracefully, killing...")
                        os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                        try:
                            self.process.wait(timeout=2)
                        except subprocess.TimeoutExpired:
                            logger.error("Process kill failed")
                            
            except Exception as e:
                logger.error(f"Error stopping process: {e}")
        
        self.emitter.simulation_finished.emit()


class ViolationDetailDialog(QDialog):
    """Dialog showing detailed violation information"""
    
    def __init__(self, violation: Dict, parent=None):
        super().__init__(parent)
        self.violation = violation
        self.setWindowTitle("Detail Pelanggaran")
        self.setGeometry(100, 100, 600, 500)
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()
        
        # Vehicle Information
        vehicle_group = QGroupBox("Informasi Kendaraan")
        vehicle_layout = QGridLayout()
        
        vehicle_layout.addWidget(QLabel("Plat Nomor:"), 0, 0)
        vehicle_layout.addWidget(QLabel(str(self.violation.get('license_plate', '-'))), 0, 1)
        
        vehicle_layout.addWidget(QLabel("Wilayah:"), 1, 0)
        region = self._get_region_from_plate(self.violation.get('license_plate', ''))
        vehicle_layout.addWidget(QLabel(region), 1, 1)
        
        vehicle_layout.addWidget(QLabel("Tipe Kendaraan:"), 2, 0)
        vehicle_layout.addWidget(QLabel(self.violation.get('vehicle_type', '-')), 2, 1)
        
        vehicle_group.setLayout(vehicle_layout)
        layout.addWidget(vehicle_group)
        
        # Owner Information
        owner_group = QGroupBox("Data Pemilik")
        owner_layout = QGridLayout()
        
        owner_name = self.violation.get('owner_name', self.violation.get('owner', {}).get('name', '-'))
        owner_layout.addWidget(QLabel("Nama:"), 0, 0)
        owner_layout.addWidget(QLabel(str(owner_name)), 0, 1)
        
        owner_id = self.violation.get('owner_id', self.violation.get('owner', {}).get('id', '-'))
        owner_layout.addWidget(QLabel("NIK (Nomor Induk Kependudukan):"), 1, 0)
        owner_layout.addWidget(QLabel(str(owner_id)), 1, 1)
        
        owner_region = self.violation.get('owner_region', self.violation.get('owner', {}).get('region', '-'))
        owner_layout.addWidget(QLabel("Tempat Tinggal:"), 2, 0)
        owner_layout.addWidget(QLabel(str(owner_region)), 2, 1)
        
        owner_group.setLayout(owner_layout)
        layout.addWidget(owner_group)
        
        # Registration Status
        reg_group = QGroupBox("Status Registrasi")
        reg_layout = QGridLayout()
        
        stnk_status = self.violation.get('stnk_status', '-')
        sim_status = self.violation.get('sim_status', '-')
        
        reg_layout.addWidget(QLabel("Status STNK:"), 0, 0)
        stnk_label = QLabel(stnk_status)
        if stnk_status == 'Non-Active':
            stnk_label.setStyleSheet("color: red; font-weight: bold;")
        reg_layout.addWidget(stnk_label, 0, 1)
        
        reg_layout.addWidget(QLabel("Status SIM:"), 1, 0)
        sim_label = QLabel(sim_status)
        if sim_status == 'Expired':
            sim_label.setStyleSheet("color: red; font-weight: bold;")
        reg_layout.addWidget(sim_label, 1, 1)
        
        reg_group.setLayout(reg_layout)
        layout.addWidget(reg_group)
        
        # Violation Details
        viol_group = QGroupBox("Detail Pelanggaran")
        viol_layout = QGridLayout()
        
        viol_layout.addWidget(QLabel("Kecepatan Terdeteksi:"), 0, 0)
        viol_layout.addWidget(QLabel(f"{self.violation.get('speed', 0):.1f} km/h"), 0, 1)
        
        viol_layout.addWidget(QLabel("Batas Kecepatan:"), 1, 0)
        viol_layout.addWidget(QLabel(f"{Config.SPEED_LIMIT} km/h"), 1, 1)
        
        viol_layout.addWidget(QLabel("Kelebihan Kecepatan:"), 2, 0)
        excess = self.violation.get('speed', 0) - Config.SPEED_LIMIT
        viol_layout.addWidget(QLabel(f"+{excess:.1f} km/h"), 2, 1)
        
        viol_layout.addWidget(QLabel("Waktu Terdeteksi:"), 3, 0)
        viol_layout.addWidget(QLabel(self.violation.get('timestamp', '-')), 3, 1)
        
        viol_group.setLayout(viol_layout)
        layout.addWidget(viol_group)
        
        # Fine Calculation
        fine_group = QGroupBox("Perhitungan Denda")
        fine_layout = QGridLayout()
        
        base_fine_usd = self.violation.get('fine_amount', 0)
        base_fine_idr = base_fine_usd * USD_TO_IDR
        multiplier = self.violation.get('penalty_multiplier', 1.0)
        total_fine_usd = self.violation.get('fine_amount', 0)
        total_fine_idr = total_fine_usd * USD_TO_IDR
        
        fine_layout.addWidget(QLabel("Denda Dasar:"), 0, 0)
        fine_layout.addWidget(QLabel(f"${base_fine_usd:.2f} / Rp {base_fine_idr:,.0f}"), 0, 1)
        
        fine_layout.addWidget(QLabel("Pengali Penalti:"), 1, 0)
        multiplier_label = QLabel(f"{multiplier}x")
        if multiplier > 1.0:
            multiplier_label.setStyleSheet("color: red; font-weight: bold;")
            reason = []
            stnk_status = self.violation.get('stnk_status', '')
            sim_status = self.violation.get('sim_status', '')
            
            if stnk_status == 'Non-Active':
                reason.append("STNK Tidak Aktif +20%")
            if sim_status == 'Expired':
                reason.append("SIM Kadaluarsa +20%")
            
            if reason:
                # Calculate base (1.0) and additions
                reason_text = " | ".join(reason)
                detail_text = multiplier_label.text() + f" ({reason_text})"
                fine_layout.addWidget(QLabel(detail_text), 1, 1)
            else:
                fine_layout.addWidget(multiplier_label, 1, 1)
        else:
            fine_layout.addWidget(multiplier_label, 1, 1)
        
        fine_layout.addWidget(QLabel("Total Denda:"), 2, 0)
        total_label = QLabel(f"${total_fine_usd:.2f} / Rp {total_fine_idr:,.0f}")
        total_label.setStyleSheet("color: darkred; font-weight: bold; font-size: 12pt;")
        fine_layout.addWidget(total_label, 2, 1)
        
        fine_group.setLayout(fine_layout)
        layout.addWidget(fine_group)
        
        # Close button
        close_btn = QPushButton("Tutup")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
    
    def _get_region_from_plate(self, plate: str) -> str:
        """Get region from license plate"""
        regions = {
            'B': 'Jakarta (DKI)', 'D': 'Bandung (Jawa Barat)', 'H': 'Semarang (Jawa Tengah)',
            'AB': 'Yogyakarta', 'L': 'Surabaya (Jawa Timur)', 'N': 'Madura',
            'AA': 'Medan (Sumatera Utara)', 'BK': 'Aceh', 'BA': 'Palembang (Sumatera Selatan)',
            'BL': 'Bengkulu', 'BP': 'Lampung', 'KB': 'Bandar Lampung',
            'AG': 'Pekanbaru (Riau)', 'AM': 'Jambi', 'AE': 'Pontianak (Kalimantan Barat)',
            'AH': 'Banjarmasin (Kalimantan Selatan)', 'DK': 'Denpasar (Bali)',
            'DL': 'Mataram (NTB)', 'EA': 'Kupang (NTT)', 'EB': 'Manado (Sulawesi Utara)',
            'ED': 'Gorontalo', 'EE': 'Palu (Sulawesi Tengah)', 'DR': 'Makassar (Sulawesi Selatan)',
            'DM': 'Kendari (Sulawesi Tenggara)', 'DS': 'Ternate (Maluku Utara)',
            'DB': 'Ambon (Maluku)', 'PA': 'Jayapura (Papua)', 'PB': 'Manokwari (Papua Barat)'
        }
        
        if not plate:
            return 'Tidak Diketahui'
        
        parts = plate.split()
        if parts:
            code = parts[0]
            return regions.get(code, f'Kode: {code}')
        return 'Tidak Diketahui'


class TrafficSimulationGUI(QMainWindow):
    """Main GUI application"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistem Monitoring Pelanggaran Lalu Lintas Indonesia")
        self.setGeometry(100, 100, 1400, 800)
        self.simulation_worker = None
        self.violations = []
        self.last_violation_count = 0
        self.last_vehicle_count = 0
        
        # Auto-refresh timer for real-time updates
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.auto_refresh)
        self.refresh_timer.setInterval(500)  # Refresh every 500ms
        
        self.init_ui()
        self.load_violations()
    
    def closeEvent(self, event):
        """Handle window close event - stop simulation and threads"""
        self.cleanup()
        event.accept()
    
    def cleanup(self):
        """Clean up resources before closing"""
        # Stop the refresh timer
        self.refresh_timer.stop()
        
        # Stop the simulation if running
        if self.simulation_worker:
            self.simulation_worker.stop()
            # Wait for worker thread to finish
            if self.simulation_worker.isRunning():
                self.simulation_worker.wait(5000)  # Wait up to 5 seconds
        
        logger.info("Application cleanup complete")
    
    def init_ui(self):
        """Initialize UI"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        
        # Left Panel: Control and Stats
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Title
        title = QLabel("DASHBOARD PELANGGARAN")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        left_layout.addWidget(title)
        
        # Control Group
        control_group = QGroupBox("Kontrol Simulasi")
        control_layout = QGridLayout()
        
        self.start_btn = QPushButton("Mulai Simulasi")
        self.start_btn.clicked.connect(self.start_simulation)
        self.start_btn.setStyleSheet("background-color: green; color: white; font-weight: bold; padding: 10px; font-size: 12pt;")
        control_layout.addWidget(self.start_btn, 0, 0, 1, 2)
        
        self.stop_btn = QPushButton("Hentikan Simulasi")
        self.stop_btn.clicked.connect(self.stop_simulation)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("background-color: red; color: white; font-weight: bold; padding: 10px; font-size: 12pt;")
        control_layout.addWidget(self.stop_btn, 1, 0, 1, 2)
        
        self.clear_btn = QPushButton("Hapus Data")
        self.clear_btn.clicked.connect(self.clear_data)
        control_layout.addWidget(self.clear_btn, 2, 0, 1, 2)
        
        control_group.setLayout(control_layout)
        left_layout.addWidget(control_group)
        
        # Statistics Group
        stats_group = QGroupBox("Statistik Real-time")
        stats_layout = QGridLayout()
        
        stats_layout.addWidget(QLabel("Total Pelanggaran:"), 0, 0)
        self.violations_count_label = QLabel("0")
        violations_font = QFont()
        violations_font.setPointSize(12)
        violations_font.setBold(True)
        self.violations_count_label.setFont(violations_font)
        self.violations_count_label.setStyleSheet("color: red;")
        stats_layout.addWidget(self.violations_count_label, 0, 1)
        
        stats_layout.addWidget(QLabel("Kendaraan Diproses:"), 1, 0)
        self.vehicles_count_label = QLabel("0")
        self.vehicles_count_label.setFont(violations_font)
        stats_layout.addWidget(self.vehicles_count_label, 1, 1)
        
        stats_layout.addWidget(QLabel("Total Denda (IDR):"), 2, 0)
        self.total_fines_label = QLabel("Rp 0")
        self.total_fines_label.setFont(violations_font)
        self.total_fines_label.setStyleSheet("color: darkred;")
        stats_layout.addWidget(self.total_fines_label, 2, 1)
        
        stats_layout.addWidget(QLabel("Rata-rata Kecepatan:"), 3, 0)
        self.avg_speed_label = QLabel("0 km/h")
        stats_layout.addWidget(self.avg_speed_label, 3, 1)
        
        stats_layout.addWidget(QLabel("Kecepatan Maksimal:"), 4, 0)
        self.max_speed_label = QLabel("0 km/h")
        stats_layout.addWidget(self.max_speed_label, 4, 1)
        
        stats_group.setLayout(stats_layout)
        left_layout.addWidget(stats_group)
        
        # Live Status Group
        status_group = QGroupBox("Status Pemeriksaan Real-time (5 Sensor)")
        status_layout = QVBoxLayout()
        
        # Create 5 sensor panels
        sensors_container = QWidget()
        sensors_grid = QGridLayout()
        
        self.sensor_labels = {}  # Dictionary to store sensor UI elements
        
        for sensor_id in range(1, 6):
            # Each sensor in a group
            sensor_group = QGroupBox(f"Sensor {sensor_id}")
            sensor_layout = QVBoxLayout()
            
            # Sensor status (IDLE/CHECKING/SAFE/VIOLATION)
            status_label = QLabel("IDLE")
            status_label.setStyleSheet("color: gray; font-weight: bold; font-size: 10pt; padding: 5px;")
            sensor_layout.addWidget(status_label)
            
            # Current car plate
            plate_label = QLabel("-")
            plate_label.setStyleSheet("color: black; font-size: 10pt; padding: 3px;")
            plate_label.setWordWrap(True)
            sensor_layout.addWidget(QLabel("Plat:"))
            sensor_layout.addWidget(plate_label)
            
            # Speed
            speed_label = QLabel("-")
            speed_label.setStyleSheet("color: black; font-size: 10pt; padding: 3px;")
            sensor_layout.addWidget(QLabel("Kecepatan:"))
            sensor_layout.addWidget(speed_label)
            
            # Fine amount
            fine_label = QLabel("-")
            fine_label.setStyleSheet("color: darkred; font-size: 10pt; padding: 3px;")
            sensor_layout.addWidget(QLabel("Denda:"))
            sensor_layout.addWidget(fine_label)
            
            sensor_group.setLayout(sensor_layout)
            
            # Store references to labels
            self.sensor_labels[sensor_id] = {
                'status': status_label,
                'plate': plate_label,
                'speed': speed_label,
                'fine': fine_label,
                'group': sensor_group
            }
            
            # Add to grid (2 rows x 3 columns)
            row = (sensor_id - 1) // 3
            col = (sensor_id - 1) % 3
            sensors_grid.addWidget(sensor_group, row, col)
        
        sensors_container.setLayout(sensors_grid)
        status_layout.addWidget(sensors_container)
        
        status_group.setLayout(status_layout)
        left_layout.addWidget(status_group)
        
        left_layout.addStretch()
        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(300)
        
        # Right Panel: Violations Table
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        right_title = QLabel("DAFTAR PELANGGARAN")
        right_title.setFont(title_font)
        right_layout.addWidget(right_title)
        
        # Violations Table
        self.violations_table = QTableWidget()
        self.violations_table.setColumnCount(6)
        self.violations_table.setHorizontalHeaderLabels([
            "Plat Nomor", "Pemilik", "Kecepatan", "Denda (IDR)", "Status STNK", "Detail"
        ])
        
        header = self.violations_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        right_layout.addWidget(self.violations_table)
        right_panel.setLayout(right_layout)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)
        
        main_widget.setLayout(main_layout)
        self.update_stats()
    
    def load_violations(self):
        """Load violations from file"""
        try:
            violations_file = Path("data_files/tickets.json")
            if violations_file.exists():
                with open(violations_file, 'r') as f:
                    raw_violations = json.load(f) or []
                # Convert nested structure to flat structure for GUI
                self.violations = [self._flatten_violation(v) for v in raw_violations]
                self.refresh_violations_table()
                self.update_stats()
        except Exception as e:
            print(f"Error loading violations: {e}")
    
    def _flatten_violation(self, violation: Dict) -> Dict:
        """Convert nested violation structure from JSON to flat GUI structure"""
        flattened = violation.copy()
        
        # Flatten owner data
        if 'owner' in violation and isinstance(violation['owner'], dict):
            flattened['owner_id'] = violation['owner'].get('id', '-')
            flattened['owner_name'] = violation['owner'].get('name', '-')
            flattened['owner_region'] = violation['owner'].get('region', '-')
        
        # Flatten registration data
        if 'registration' in violation and isinstance(violation['registration'], dict):
            flattened['stnk_status'] = violation['registration'].get('stnk_status', '-')
            flattened['sim_status'] = violation['registration'].get('sim_status', '-')
        
        # Flatten fine data
        if 'fine' in violation and isinstance(violation['fine'], dict):
            flattened['fine_amount'] = violation['fine'].get('total_fine', 0)
            flattened['penalty_multiplier'] = violation['fine'].get('penalty_multiplier', 1.0)
            flattened['base_fine'] = violation['fine'].get('base_fine', 0)
        
        return flattened
    
    def refresh_violations_table(self):
        """Refresh the violations table"""
        self.violations_table.setRowCount(len(self.violations))
        
        for row, violation in enumerate(self.violations):
            plate_item = QTableWidgetItem(str(violation.get('license_plate', '-')))
            self.violations_table.setItem(row, 0, plate_item)
            
            owner_name = violation.get('owner_name', violation.get('owner', {}).get('name', '-'))
            owner_item = QTableWidgetItem(str(owner_name))
            self.violations_table.setItem(row, 1, owner_item)
            
            speed_item = QTableWidgetItem(f"{violation.get('speed', 0):.1f} km/h")
            self.violations_table.setItem(row, 2, speed_item)
            
            total_fine_usd = violation.get('fine_amount', 0)
            total_fine_idr = total_fine_usd * USD_TO_IDR
            fine_item = QTableWidgetItem(f"Rp {total_fine_idr:,.0f}")
            fine_item.setForeground(QBrush(QColor("darkred")))
            self.violations_table.setItem(row, 3, fine_item)
            
            stnk_status = violation.get('stnk_status', '-')
            stnk_item = QTableWidgetItem(stnk_status)
            if stnk_status == 'Non-Active':
                stnk_item.setForeground(QBrush(QColor("red")))
            self.violations_table.setItem(row, 4, stnk_item)
            
            detail_btn = QPushButton("Lihat")
            detail_btn.clicked.connect(lambda checked, v=violation: self.show_detail(v))
            self.violations_table.setCellWidget(row, 5, detail_btn)
    
    def show_detail(self, violation: Dict):
        """Show detail dialog for a violation"""
        dialog = ViolationDetailDialog(violation, self)
        dialog.exec_()
    
    def start_simulation(self):
        """Start the simulation"""
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        # Clear previous data
        self.violations = []
        self.last_violation_count = 0
        self.last_vehicle_count = 0
        self.refresh_violations_table()
        
        # Start refresh timer for real-time updates
        self.refresh_timer.start()
        
        self.simulation_worker = SimulationWorker()
        self.simulation_worker.emitter.violation_detected.connect(self.on_violation_detected)
        self.simulation_worker.emitter.stats_updated.connect(self.on_stats_updated)
        self.simulation_worker.emitter.simulation_finished.connect(self.on_simulation_finished)
        self.simulation_worker.start()
    
    def stop_simulation(self):
        """Stop the simulation"""
        if self.simulation_worker:
            self.simulation_worker.stop()
            self.stop_btn.setEnabled(False)
    
    def on_violation_detected(self, violation: Dict):
        """Handle new violation detection"""
        # Flatten violation data if needed
        flattened = self._flatten_violation(violation)
        self.violations.append(flattened)
        self.refresh_violations_table()
        self.update_stats()
    
    def on_stats_updated(self, stats: Dict):
        """Handle stats update"""
        self.violations_count_label.setText(str(stats['violations_count']))
        self.vehicles_count_label.setText(str(stats['vehicles_processed']))
        
        total_idr = stats['total_fines_idr']
        self.total_fines_label.setText(f"Rp {total_idr:,.0f}")
        
        self.avg_speed_label.setText(f"{stats['avg_speed']:.1f} km/h")
        self.max_speed_label.setText(f"{stats['max_speed']:.1f} km/h")
    
    def on_simulation_finished(self):
        """Handle simulation finished"""
        self.refresh_timer.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
    
    def auto_refresh(self):
        """Auto-refresh violations and status every 500ms"""
        try:
            violations_file = Path("data_files/tickets.json")
            vehicles_file = Path("data_files/traffic_data.json")
            worker_status_file = Path("data_files/worker_status.json")
            
            violations = []
            vehicles = []
            worker_statuses = {}
            
            if violations_file.exists():
                try:
                    with open(violations_file, 'r') as f:
                        violations = json.load(f) or []
                except:
                    violations = []
            
            if vehicles_file.exists():
                try:
                    with open(vehicles_file, 'r') as f:
                        vehicles = json.load(f) or []
                except:
                    vehicles = []
            
            if worker_status_file.exists():
                try:
                    with open(worker_status_file, 'r') as f:
                        worker_statuses = json.load(f) or {}
                except:
                    worker_statuses = {}
            
            # Update violations table if count changed
            viol_count = len(violations)
            if viol_count != self.last_violation_count:
                self.violations = [self._flatten_violation(v) for v in violations]
                self.refresh_violations_table()
                self.last_violation_count = viol_count
            
            # Update vehicle count
            vehicle_count = len(vehicles)
            if vehicle_count != self.last_vehicle_count:
                self.vehicles_count_label.setText(str(vehicle_count))
                self.last_vehicle_count = vehicle_count
            
            # Update each sensor's status
            for sensor_id in range(1, 6):
                sensor_info = self.sensor_labels.get(sensor_id)
                if not sensor_info:
                    continue
                
                # Get worker status for this sensor
                worker_key = str(sensor_id - 1)
                worker_data = worker_statuses.get(worker_key, {})
                
                if worker_data and worker_data.get('vehicle'):
                    vehicle = worker_data['vehicle']
                    status = worker_data.get('status', 'CHECKING')
                    
                    plate = vehicle.get('license_plate', '?')
                    speed = vehicle.get('speed', 0)
                    
                    # Check if this is a violation
                    is_violation = any(v.get('license_plate') == plate for v in violations)
                    
                    if is_violation:
                        # Find the violation to get fine
                        violation = next((v for v in violations if v.get('license_plate') == plate), None)
                        fine = violation.get('fine_amount', 0) * USD_TO_IDR if violation else 0
                        
                        status_text = "VIOLATION"
                        color = "darkred"
                        status_bg = "#ffe0e0"
                        fine_text = f"Rp {fine:,.0f}"
                    else:
                        status_text = "SAFE"
                        color = "darkgreen"
                        status_bg = "#e0ffe0"
                        fine_text = "-"
                    
                    # Update sensor display
                    sensor_info['status'].setText(status_text)
                    sensor_info['status'].setStyleSheet(f"color: {color}; font-weight: bold; font-size: 10pt; padding: 5px; background-color: {status_bg}; border-radius: 3px;")
                    
                    sensor_info['plate'].setText(f"{plate}")
                    sensor_info['speed'].setText(f"{speed:.1f} km/h")
                    sensor_info['fine'].setText(fine_text)
                    
                else:
                    # Sensor is idle
                    sensor_info['status'].setText("IDLE")
                    sensor_info['status'].setStyleSheet("color: gray; font-weight: bold; font-size: 10pt; padding: 5px;")
                    sensor_info['plate'].setText("-")
                    sensor_info['speed'].setText("-")
                    sensor_info['fine'].setText("-")
            
            # Update statistics
            self.violations_count_label.setText(str(len(violations)))
            total_fines = sum(v.get('fine_amount', 0) for v in violations) * USD_TO_IDR
            self.total_fines_label.setText(f"Rp {total_fines:,.0f}")
            
            speeds = [v.get('speed', 0) for v in vehicles]
            if speeds:
                self.avg_speed_label.setText(f"{sum(speeds) / len(speeds):.1f} km/h")
                self.max_speed_label.setText(f"{max(speeds):.1f} km/h")
        
        except Exception as e:
            pass  # Silent fail for file read errors
    
    
    def update_stats(self):
        """Update statistics display"""
        try:
            violations_file = Path("data_files/tickets.json")
            vehicles_file = Path("data_files/traffic_data.json")
            
            violations = []
            vehicles = []
            
            if violations_file.exists():
                with open(violations_file, 'r') as f:
                    violations = json.load(f) or []
            
            if vehicles_file.exists():
                with open(vehicles_file, 'r') as f:
                    vehicles = json.load(f) or []
            
            self.violations_count_label.setText(str(len(violations)))
            self.vehicles_count_label.setText(str(len(vehicles)))
            
            total_fines = sum(t.get('total_fine', 0) for t in violations)
            self.total_fines_label.setText(f"Rp {total_fines * USD_TO_IDR:,.0f}")
            
            speeds = [v.get('speed', 0) for v in violations]
            if speeds:
                self.avg_speed_label.setText(f"{sum(speeds) / len(speeds):.1f} km/h")
                self.max_speed_label.setText(f"{max(speeds):.1f} km/h")
            
        except Exception as e:
            # Silent error handling
            pass
    
    def clear_data(self):
        """Clear all data"""
        reply = QMessageBox.question(
            self, "Konfirmasi", "Apakah Anda yakin ingin menghapus semua data?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                Path("data_files/tickets.json").write_text("[]")
                Path("data_files/traffic_data.json").write_text("[]")
                self.violations = []
                self.refresh_violations_table()
                self.update_stats()
                QMessageBox.information(self, "Sukses", "Data telah dihapus.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error menghapus data: {e}")


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    window = TrafficSimulationGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
