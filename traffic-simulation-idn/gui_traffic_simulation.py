"""
Qt5 GUI for Indonesian Traffic Violation Simulation
Displays real-time violations with owner information, vehicle types, and Rupiah currency
Follows Indonesian plate nomenclature: Roda Dua (Motor) and Roda Empat atau lebih (Mobil)
"""

import sys
import json
import subprocess
import time
import os
import signal
from pathlib import Path
from typing import Dict
import psutil

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSpinBox, QTableWidget, QTableWidgetItem,
    QDialog, QGroupBox, QGridLayout, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QBrush

from config import Config
from utils.logger import logger
from utils.indonesian_plates import IndonesianPlateManager

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
            
            # Create process with proper subprocess handling
            if os.name == 'nt':  # Windows
                self.process = subprocess.Popen(
                    [sys.executable, "main.py"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    cwd=current_dir,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP  # This helps with killing child processes
                )
            else:  # Linux/Mac
                self.process = subprocess.Popen(
                    [sys.executable, "main.py"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    cwd=current_dir,
                    preexec_fn=os.setsid  # Create new process group
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
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.stop()
            
            # Final stats
            stats = self._get_current_stats()
            self.emitter.stats_updated.emit(stats)
            
        except Exception as e:
            logger.error(f"Simulation error: {e}")
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
                logger.info(f"Terminating subprocess (PID: {self.process.pid})")
                
                # Kill process and all children using psutil
                try:
                    parent = psutil.Process(self.process.pid)
                    # Get all child processes
                    children = parent.children(recursive=True)
                    
                    # Terminate all children first
                    for child in children:
                        try:
                            if os.name == 'nt':
                                child.kill()
                            else:
                                child.terminate()
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
                    
                    # Then terminate parent
                    if os.name == 'nt':
                        parent.kill()
                    else:
                        parent.terminate()
                    
                    # Wait for process to die
                    try:
                        parent.wait(timeout=3)
                        logger.info(f"Process {self.process.pid} terminated successfully")
                    except subprocess.TimeoutExpired:
                        logger.warning(f"Process {self.process.pid} didn't stop, force killing...")
                        parent.kill()
                        try:
                            parent.wait(timeout=2)
                        except subprocess.TimeoutExpired:
                            logger.error(f"Could not kill process {self.process.pid}")
                            
                except psutil.NoSuchProcess:
                    logger.info("Process already terminated")
                except Exception as e:
                    logger.error(f"Error using psutil: {e}, trying fallback...")
                    # Fallback method if psutil fails
                    if os.name == 'nt':
                        subprocess.Popen(['taskkill', '/PID', str(self.process.pid), '/T', '/F'],
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    else:
                        self.process.terminate()
                    
                    try:
                        self.process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        logger.warning("Fallback termination also timed out")
                            
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
        
        vehicle_layout.addWidget(QLabel("Sub-Wilayah:"), 2, 0)
        sub_region = self._get_sub_region_from_plate(self.violation.get('license_plate', ''))
        vehicle_layout.addWidget(QLabel(sub_region), 2, 1)
        
        vehicle_layout.addWidget(QLabel("Tipe Kendaraan:"), 3, 0)
        vehicle_type = self.violation.get('vehicle_type', '-')
        vehicle_make = self.violation.get('vehicle_make', '').strip()
        vehicle_model = self.violation.get('vehicle_model', '').strip()
        vehicle_category = self.violation.get('vehicle_category', 'Pribadi')
        
        # Translate vehicle type to Indonesian
        if vehicle_type == 'roda_dua':
            vehicle_type_display = 'Roda Dua (Motor)'
        elif vehicle_type == 'roda_empat':
            vehicle_type_display = 'Roda Empat atau lebih (Mobil/Truk)'
        else:
            vehicle_type_display = str(vehicle_type)
        
        # Add make and model if available (skip if empty or 'Unknown')
        if vehicle_make and vehicle_make != 'Unknown' and vehicle_model and vehicle_model != 'Unknown':
            vehicle_type_display = f"{vehicle_type_display} - {vehicle_make} {vehicle_model}"
        elif vehicle_make and vehicle_make != 'Unknown':
            vehicle_type_display = f"{vehicle_type_display} - {vehicle_make}"
        
        vehicle_layout.addWidget(QLabel(vehicle_type_display), 3, 1)
        
        vehicle_layout.addWidget(QLabel("Kategori Kendaraan:"), 4, 0)
        vehicle_layout.addWidget(QLabel(vehicle_category), 4, 1)
        
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
        # Convert region code to region name if needed (use authoritative PLATE_DATA first)
        owner_region_display = owner_region
        try:
            val = str(owner_region).upper().strip()
            if val in IndonesianPlateManager.PLATE_DATA:
                owner_region_display = IndonesianPlateManager.PLATE_DATA[val].get('region_name', owner_region)
            else:
                owner_region_display = self._convert_region_code_to_name(owner_region)
        except Exception:
            owner_region_display = owner_region
        owner_layout.addWidget(QLabel("Tempat Tinggal:"), 2, 0)
        owner_layout.addWidget(QLabel(str(owner_region_display)), 2, 1)
        
        # Add sub-region for owner - extract from plate's parsed information
        owner_sub_region = '-'
        try:
            plate_str = self.violation.get('plate', self.violation.get('license_plate', ''))
            if plate_str:
                plate_info = IndonesianPlateManager.parse_plate(plate_str)
                if plate_info and 'sub_region' in plate_info:
                    owner_sub_region = plate_info['sub_region']
        except Exception:
            pass
        owner_layout.addWidget(QLabel("Sub-Wilayah Tempat Tinggal:"), 3, 0)
        owner_layout.addWidget(QLabel(owner_sub_region), 3, 1)
        
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
        
        # Determine if this is a speeding or too-slow violation and display accordingly
        detected_speed = float(self.violation.get('speed', 0) or 0)
        if detected_speed < Config.MIN_SPEED_LIMIT:
            # Too slow
            viol_layout.addWidget(QLabel("Batas Minimum:"), 1, 0)
            viol_layout.addWidget(QLabel(f"{Config.MIN_SPEED_LIMIT} km/h"), 1, 1)

            viol_layout.addWidget(QLabel("Selisih dari Minimum:"), 2, 0)
            diff = detected_speed - Config.MIN_SPEED_LIMIT
            # Show negative value (how much below the minimum)
            viol_layout.addWidget(QLabel(f"{diff:.1f} km/h"), 2, 1)
        else:
            # Speeding (over the limit)
            viol_layout.addWidget(QLabel("Batas Kecepatan:"), 1, 0)
            viol_layout.addWidget(QLabel(f"{Config.SPEED_LIMIT} km/h"), 1, 1)

            viol_layout.addWidget(QLabel("Kelebihan Kecepatan:"), 2, 0)
            excess = detected_speed - Config.SPEED_LIMIT
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
        total_fine_usd = base_fine_usd * multiplier
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
        # First, try authoritative PLATE_DATA mapping from IndonesianPlateManager
        if not plate:
            return 'Tidak Diketahui'
        
        parts = plate.split()
        if parts:
            code = parts[0].upper()
            # Use PLATE_DATA if available
            try:
                if code in IndonesianPlateManager.PLATE_DATA:
                    return IndonesianPlateManager.PLATE_DATA[code].get('region_name', f'Kode: {code}')
            except Exception:
                pass
            
            # Fallback to legacy static mapping for presentation
            regions = {
                'A': 'Banten', 'AA': 'Jawa Tengah (Keresidenan Kedu)', 'AB': 'Daerah Istimewa Yogyakarta',
                'AD': 'Jawa Tengah (Keresidenan Surakarta)', 'AE': 'Jawa Timur (Madiun)', 'AG': 'Jawa Timur (Kediri)',
                'B': 'DKI Jakarta', 'BA': 'Sumatera Barat', 'BB': 'Sumatera Utara Barat (Tapanuli)',
                'BD': 'Bengkulu', 'BE': 'Lampung', 'BG': 'Sumatera Selatan', 'BH': 'Jambi',
                'BK': 'Sumatera Utara Timur (Pesisir Timur Sumatra)', 'BL': 'Aceh', 'BM': 'Riau', 'BN': 'Kepulauan Bangka Belitung',
                'BP': 'Kepulauan Riau', 'D': 'Jawa Barat (Priangan Tengah)', 'DA': 'Kalimantan Selatan', 'DB': 'Sulawesi Utara (Daratan)',
                'DC': 'Sulawesi Barat', 'DD': 'Sulawesi Selatan (Makassar)', 'DE': 'Maluku', 'DG': 'Maluku Utara',
                'DH': 'NTT (Timor)', 'DK': 'Bali', 'DL': 'Sulawesi Utara (Kepulauan)', 'DM': 'Gorontalo',
                'DN': 'Sulawesi Tengah', 'DP': 'Sulawesi Selatan (Utara)', 'DR': 'NTB (Lombok)', 'DT': 'Sulawesi Tenggara',
                'DW': 'Sulawesi Selatan (Bone, Wajo)', 'E': 'Jawa Barat (Keresidenan Cirebon)', 'EA': 'NTB (Sumbawa)',
                'EB': 'NTT (Flores)', 'ED': 'NTT (Sumba)', 'F': 'Jawa Barat (Keresidenan Bogor dan Priangan Barat)',
                'G': 'Jawa Tengah (Keresidenan Pekalongan)', 'H': 'Jawa Tengah (Keresidenan Semarang)', 'K': 'Jawa Tengah (Keresidenan Pati dan Grobogan)',
                'KB': 'Kalimantan Barat', 'KH': 'Kalimantan Tengah', 'KT': 'Kalimantan Timur', 'KU': 'Kalimantan Utara',
                'L': 'Jawa Timur (Kota Surabaya)', 'M': 'Jawa Timur (Madura)', 'N': 'Jawa Timur (Pasuruan-Malang)', 'P': 'Jawa Timur (Besuki)',
                'PA': 'Papua', 'PB': 'Papua Barat', 'PG': 'Papua Pegunungan', 'PS': 'Papua Selatan', 'PT': 'Papua Tengah', 'PY': 'Papua Barat Daya',
                'R': 'Jawa Tengah (Keresidenan Banyumas)', 'S': 'Jawa Timur (Bojonegoro, Mojokerto, Lamongan, Jombang)', 
                'T': 'Jawa Barat (Keresidenan Karawang)', 'W': 'Jawa Timur (Surabaya)', 'Z': 'Jawa Barat (Priangan Timur dan Kabupaten Sumedang)',
                'CC': 'Diplomatik', 'CD': 'Diplomatik', 'RI': 'Pemerintah Indonesia'
            }
            return regions.get(code, f'Kode: {code}')
        return 'Tidak Diketahui' 
    
    def _convert_region_code_to_name(self, value: str) -> str:
        """Convert region code to full region name"""
        if not value or value == '-':
            return value
        
        # Try authoritative PLATE_DATA first
        try:
            val = str(value).upper().strip()
            if val in IndonesianPlateManager.PLATE_DATA:
                return IndonesianPlateManager.PLATE_DATA[val].get('region_name', value)
        except Exception:
            pass
        
        # Fallback to legacy static mapping for presentation - using PLATE_DATA values
        regions_map = {
            'A': 'Banten', 'AA': 'Jawa Tengah (Keresidenan Kedu)', 'AB': 'Daerah Istimewa Yogyakarta',
            'AD': 'Jawa Tengah (Keresidenan Surakarta)', 'AE': 'Jawa Timur (Madiun)', 'AG': 'Jawa Timur (Kediri)',
            'B': 'DKI Jakarta', 'BA': 'Sumatera Barat', 'BB': 'Sumatera Utara Barat (Tapanuli)',
            'BD': 'Bengkulu', 'BE': 'Lampung', 'BG': 'Sumatera Selatan', 'BH': 'Jambi',
            'BK': 'Sumatera Utara Timur (Pesisir Timur Sumatra)', 'BL': 'Aceh', 'BM': 'Riau', 'BN': 'Kepulauan Bangka Belitung',
            'BP': 'Kepulauan Riau', 'D': 'Jawa Barat (Priangan Tengah)', 'DA': 'Kalimantan Selatan', 'DB': 'Sulawesi Utara (Daratan)',
            'DC': 'Sulawesi Barat', 'DD': 'Sulawesi Selatan (Makassar)', 'DE': 'Maluku', 'DG': 'Maluku Utara',
            'DH': 'NTT (Timor)', 'DK': 'Bali', 'DL': 'Sulawesi Utara (Kepulauan)', 'DM': 'Gorontalo',
            'DN': 'Sulawesi Tengah', 'DP': 'Sulawesi Selatan (Utara)', 'DR': 'NTB (Lombok)', 'DT': 'Sulawesi Tenggara',
            'DW': 'Sulawesi Selatan (Bone, Wajo)', 'E': 'Jawa Barat (Keresidenan Cirebon)', 'EA': 'NTB (Sumbawa)',
            'EB': 'NTT (Flores)', 'ED': 'NTT (Sumba)', 'F': 'Jawa Barat (Keresidenan Bogor dan Priangan Barat)',
            'G': 'Jawa Tengah (Keresidenan Pekalongan)', 'H': 'Jawa Tengah (Keresidenan Semarang)', 'K': 'Jawa Tengah (Keresidenan Pati dan Grobogan)',
            'KB': 'Kalimantan Barat', 'KH': 'Kalimantan Tengah', 'KT': 'Kalimantan Timur', 'KU': 'Kalimantan Utara',
            'L': 'Jawa Timur (Kota Surabaya)', 'M': 'Jawa Timur (Madura)', 'N': 'Jawa Timur (Pasuruan-Malang)', 'P': 'Jawa Timur (Besuki)',
            'PA': 'Papua', 'PB': 'Papua Barat', 'PG': 'Papua Pegunungan', 'PS': 'Papua Selatan', 'PT': 'Papua Tengah', 'PY': 'Papua Barat Daya',
            'R': 'Jawa Tengah (Keresidenan Banyumas)', 'S': 'Jawa Timur (Bojonegoro, Mojokerto, Lamongan, Jombang)', 
            'T': 'Jawa Barat (Keresidenan Karawang)', 'W': 'Jawa Timur (Surabaya)', 'Z': 'Jawa Barat (Priangan Timur dan Kabupaten Sumedang)',
            'CC': 'Diplomatik', 'CD': 'Diplomatik', 'RI': 'Pemerintah Indonesia'
        }
        
        # If value looks like a region code, convert it
        if value.upper() in regions_map:
            return regions_map[value.upper()]
        
        # If it's already a full name or unknown format, return as is
        return value
    
    def _get_sub_region_from_plate(self, plate: str) -> str:
        """Get sub-region from license plate based on the owner code letters
        
        The sub-region is determined by the owner code letters (position [2] in plate).
        Example: "BL 104 LWG" -> owner code is "LWG", lookup first letter "L" in BL's sub_codes
        """
        if not plate:
            return '-'
        
        parts = plate.split()
        if len(parts) < 3:
            return '-'
        
        plate_code = parts[0].upper()
        owner_code = parts[2].upper()  # This is the owner letters (position 2)
        
        try:
            if plate_code in IndonesianPlateManager.PLATE_DATA:
                plate_info = IndonesianPlateManager.PLATE_DATA[plate_code]
                sub_codes = plate_info.get('sub_codes', {})
                
                # Try first letter of owner code
                if owner_code and owner_code[0] in sub_codes:
                    return sub_codes[owner_code[0]]
                
                # Try full owner code in case it's mapped
                if owner_code in sub_codes:
                    return sub_codes[owner_code]
        except Exception:
            pass
        
        return '-'
    
    def _get_sub_region_from_code(self, code: str) -> str:
        """Get sub-region from a region code (used for owner region)
        This maps province codes to common sub-regions or returns hyphen if not available"""
        if not code or code == '-':
            return '-'
        
        code = str(code).upper().strip()
        
        try:
            # Try to find if this code exists in PLATE_DATA
            if code in IndonesianPlateManager.PLATE_DATA:
                plate_info = IndonesianPlateManager.PLATE_DATA[code]
                # Get first available sub-region as representative
                sub_codes = plate_info.get('sub_codes', {})
                if sub_codes:
                    first_sub = next(iter(sub_codes.values()), '-')
                    return first_sub
        except Exception:
            pass
        
        return '-'
    
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
        try:
            # Stop the refresh timer
            self.refresh_timer.stop()
            
            # Stop the simulation if running
            if self.simulation_worker:
                logger.info("Stopping simulation worker...")
                self.simulation_worker.stop()
                
                # Wait for worker thread to finish with timeout
                if self.simulation_worker.isRunning():
                    logger.info("Waiting for worker thread to finish...")
                    self.simulation_worker.wait(3000)  # Wait 3 seconds
                    
                    if self.simulation_worker.isRunning():
                        logger.warning("Worker thread still running, forcing quit...")
                        self.simulation_worker.quit()
                        self.simulation_worker.wait(2000)
                
                logger.info("Simulation worker stopped")
            
            # Double-check: Kill any stray main.py processes
            try:
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        if 'main.py' in proc.name() or (proc.name() == 'python.exe' and 'main' in ' '.join(proc.cmdline())):
                            logger.warning(f"Found stray main.py process (PID: {proc.pid}), killing...")
                            proc.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            except Exception as e:
                logger.debug(f"Could not check for stray processes: {e}")
            
            logger.info("Application cleanup complete")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
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
        self.violations_table.setColumnCount(7)
        self.violations_table.setHorizontalHeaderLabels([
            "Plat Nomor", "Pemilik", "Jenis Pelanggaran", "Kecepatan", "Denda (IDR)", "Status STNK", "Detail"
        ])
        
        header = self.violations_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        
        right_layout.addWidget(self.violations_table)
        right_panel.setLayout(right_layout)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)
        
        main_widget.setLayout(main_layout)
        self.update_stats()
    
    def _convert_region_code_to_name(self, value: str) -> str:
        """Convert region code to full region name"""
        if not value or value == '-':
            return value
        
        # Map of region codes to full names
        regions_map = {
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
        
        # If value looks like a region code, convert it
        if value.upper() in regions_map:
            return regions_map[value.upper()]
        
        # If it's already a full name or unknown format, return as is
        return value
    
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
        
        # Ensure vehicle_type is present (from root level or keep as-is)
        if 'vehicle_type' not in flattened:
            flattened['vehicle_type'] = '-'
        
        # Keep vehicle make and model as empty if not present (don't force to '-')
        # This prevents 'Unknown Unknown' from showing in detail dialog
        if 'vehicle_make' not in flattened:
            flattened['vehicle_make'] = ''
        if 'vehicle_model' not in flattened:
            flattened['vehicle_model'] = ''
        
        # Ensure vehicle category is present
        if 'vehicle_category' not in flattened:
            flattened['vehicle_category'] = 'Pribadi'
        
        # Flatten owner data
        if 'owner' in violation and isinstance(violation['owner'], dict):
            flattened['owner_id'] = violation['owner'].get('id', '-')
            flattened['owner_name'] = violation['owner'].get('name', '-')
            # Convert region code to region name for export
            region_value = violation['owner'].get('region', '-')
            flattened['owner_region'] = self._convert_region_code_to_name(region_value)
        else:
            # Handle flat structure where owner_region is already a plate code
            if 'owner_region' in flattened:
                # owner_region is already the plate code from Vehicle object
                # Keep it as-is (don't convert to name)
                pass
        
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
            
            # Determine violation type (Speeding vs Too Slow) and display
            speed = float(violation.get('speed', 0) or 0)
            if speed < Config.MIN_SPEED_LIMIT:
                violation_type = "TERLALU LAMBAT"
                violation_color = QColor("orange")
            else:
                violation_type = "SPEEDING"
                violation_color = QColor("darkred")
            
            type_item = QTableWidgetItem(violation_type)
            type_item.setForeground(QBrush(violation_color))
            type_item.setFont(QFont())
            type_item.font().setBold(True)
            self.violations_table.setItem(row, 2, type_item)
            
            speed_item = QTableWidgetItem(f"{speed:.1f} km/h")
            self.violations_table.setItem(row, 3, speed_item)
            
            total_fine_usd = violation.get('fine_amount', 0)
            total_fine_idr = total_fine_usd * USD_TO_IDR
            fine_item = QTableWidgetItem(f"Rp {total_fine_idr:,.0f}")
            fine_item.setForeground(QBrush(QColor("darkred")))
            self.violations_table.setItem(row, 4, fine_item)
            
            stnk_status = violation.get('stnk_status', '-')
            stnk_item = QTableWidgetItem(stnk_status)
            if stnk_status == 'Non-Active':
                stnk_item.setForeground(QBrush(QColor("red")))
            self.violations_table.setItem(row, 5, stnk_item)
            
            detail_btn = QPushButton("Lihat")
            detail_btn.clicked.connect(lambda checked, v=violation: self.show_detail(v))
            self.violations_table.setCellWidget(row, 6, detail_btn)
    
    def show_detail(self, violation: Dict):
        """Show detail dialog for a violation"""
        dialog = ViolationDetailDialog(violation, self)
        dialog.exec_()
    
    def start_simulation(self):
        """Start the simulation"""
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        # Reset counters for update detection (don't clear violations)
        self.last_violation_count = 0
        self.last_vehicle_count = 0
        
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
            
            # Update vehicle count - always update to show current count
            vehicle_count = len(vehicles)
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
            # Extract fine amounts from nested structure
            total_fines = 0
            for v in violations:
                fine_amount = v.get('fine_amount', 0)
                if not fine_amount and 'fine' in v and isinstance(v['fine'], dict):
                    fine_amount = v['fine'].get('total_fine', 0)
                total_fines += fine_amount
            total_fines_idr = total_fines * USD_TO_IDR
            self.total_fines_label.setText(f"Rp {total_fines_idr:,.0f}")
            
            # Calculate speeds from violations (all checked vehicles)
            speeds = [v.get('speed', 0) for v in violations]
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
            
            # Extract fine amounts from nested structure
            total_fines = 0
            for t in violations:
                fine_amount = t.get('fine_amount', 0)
                if not fine_amount and 'fine' in t and isinstance(t['fine'], dict):
                    fine_amount = t['fine'].get('total_fine', 0)
                total_fines += fine_amount
            self.total_fines_label.setText(f"Rp {total_fines * USD_TO_IDR:,.0f}")
            
            # Calculate speeds from violations (checked vehicles)
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
