"""
PyQt5 GUI Integration Example - Traffic Simulation with Color-Coded Plates
Shows how to integrate the plate generator system with the PyQt5 GUI

Key Features:
- Display vehicles with color-coded license plates
- Show vehicle categories with icons
- Filter by category and plate color
- Display vehicle statistics
- Real-time vehicle generation
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton, QComboBox,
    QGroupBox, QMessageBox, QTextEdit
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QColor, QFont
from datetime import datetime
import sys
sys.path.insert(0, '.')

from utils.generators import DataGenerator
from utils.gui_vehicle_formatter import VehicleDisplayFormatter
from data_models.models import Vehicle


# Color mapping for UI
PLATE_COLORS_HEX = {
    'BLACK': '#000000',
    'YELLOW': '#FFD700',
    'RED': '#DC143C',
    'WHITE': '#FFFFFF'
}

TEXT_COLORS = {
    'BLACK': '#FFFFFF',
    'YELLOW': '#000000',
    'RED': '#FFFFFF',
    'WHITE': '#000000'
}

CATEGORY_ICONS = {
    'Pribadi': '🚗',
    'Barang': '🚛',
    'PEMERINTAH': '🚔',
    'KEDUTAAN': '🏳️'
}


class VehicleGeneratorThread(QThread):
    """Background thread for generating vehicles"""
    vehicle_generated = pyqtSignal(Vehicle)
    batch_complete = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.running = False
    
    def run(self):
        """Generate vehicle batches continuously"""
        while self.running:
            try:
                vehicles = DataGenerator.generate_vehicle_batch()
                self.batch_complete.emit(vehicles)
                for vehicle in vehicles:
                    self.vehicle_generated.emit(vehicle)
            except Exception as e:
                print(f"Error generating vehicles: {e}")
    
    def start_generation(self):
        """Start vehicle generation"""
        self.running = True
        self.start()
    
    def stop_generation(self):
        """Stop vehicle generation"""
        self.running = False


class TrafficSimulationGUI(QMainWindow):
    """Main GUI window for traffic simulation with plate visualization"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Indonesian Traffic Simulation - Plate Generator Integration")
        self.setGeometry(100, 100, 1200, 800)
        
        self.vehicles = []
        self.generator_thread = None
        
        self.setup_ui()
        self.setup_timer()
    
    def setup_ui(self):
        """Setup the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        
        # Left panel - Controls and statistics
        left_panel = QVBoxLayout()
        
        # Title
        title = QLabel("Traffic Simulation - Plate Generator System")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        left_panel.addWidget(title)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.gen_button = QPushButton("Generate Batch")
        self.gen_button.clicked.connect(self.generate_batch)
        button_layout.addWidget(self.gen_button)
        
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_vehicles)
        button_layout.addWidget(self.clear_button)
        
        left_panel.addLayout(button_layout)
        
        # Filter controls
        filter_group = QGroupBox("Filters")
        filter_layout = QVBoxLayout()
        
        filter_layout.addWidget(QLabel("Filter by Category:"))
        self.category_filter = QComboBox()
        self.category_filter.addItems(['All', 'Pribadi', 'Barang', 'PEMERINTAH', 'KEDUTAAN'])
        self.category_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.category_filter)
        
        filter_layout.addWidget(QLabel("Filter by Plate Color:"))
        self.color_filter = QComboBox()
        self.color_filter.addItems(['All', 'BLACK', 'YELLOW', 'RED', 'WHITE'])
        self.color_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.color_filter)
        
        filter_group.setLayout(filter_layout)
        left_panel.addWidget(filter_group)
        
        # Statistics display
        stats_group = QGroupBox("Statistics")
        stats_layout = QVBoxLayout()
        
        self.stats_display = QTextEdit()
        self.stats_display.setReadOnly(True)
        self.stats_display.setMaximumHeight(150)
        stats_layout.addWidget(self.stats_display)
        
        stats_group.setLayout(stats_layout)
        left_panel.addWidget(stats_group)
        
        # Vehicle information detail
        detail_group = QGroupBox("Selected Vehicle Details")
        detail_layout = QVBoxLayout()
        
        self.detail_display = QTextEdit()
        self.detail_display.setReadOnly(True)
        detail_layout.addWidget(self.detail_display)
        
        detail_group.setLayout(detail_layout)
        left_panel.addWidget(detail_group)
        
        # Right panel - Vehicle table
        right_panel = QVBoxLayout()
        
        table_label = QLabel("Vehicles")
        table_font = QFont()
        table_font.setBold(True)
        table_label.setFont(table_font)
        right_panel.addWidget(table_label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            'License Plate', 'Category', 'Make', 'Owner', 'Speed', 'STNK', 'SIM'
        ])
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 80)
        self.table.setColumnWidth(5, 80)
        self.table.setColumnWidth(6, 80)
        self.table.cellClicked.connect(self.on_vehicle_selected)
        right_panel.addWidget(self.table)
        
        # Add panels to main layout
        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 2)
        
        central_widget.setLayout(main_layout)
    
    def setup_timer(self):
        """Setup timer for periodic updates"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_statistics)
        self.update_timer.start(1000)  # Update every second
    
    def generate_batch(self):
        """Generate a new batch of vehicles"""
        try:
            new_vehicles = DataGenerator.generate_vehicle_batch()
            self.vehicles.extend(new_vehicles)
            self.update_table()
            self.update_statistics()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate vehicles: {e}")
    
    def clear_vehicles(self):
        """Clear all vehicles"""
        self.vehicles.clear()
        self.update_table()
        self.update_statistics()
    
    def apply_filters(self):
        """Apply category and color filters"""
        category = self.category_filter.currentText()
        color = self.color_filter.currentText()
        
        filtered = self.vehicles.copy()
        
        if category != 'All':
            filtered = [v for v in filtered if v.vehicle_category == category]
        
        if color != 'All':
            filtered = [v for v in filtered if v.plate_color == color]
        
        self.update_table(filtered)
    
    def update_table(self, vehicles=None):
        """Update the vehicle table"""
        if vehicles is None:
            vehicles = self.vehicles
        
        self.table.setRowCount(len(vehicles))
        
        for row, vehicle in enumerate(vehicles):
            # License plate with color
            plate_item = QTableWidgetItem(vehicle.license_plate)
            plate_bg_color = PLATE_COLORS_HEX.get(vehicle.plate_color, '#000000')
            plate_text_color = TEXT_COLORS.get(vehicle.plate_color, '#FFFFFF')
            
            plate_item.setBackground(QColor(plate_bg_color))
            plate_item.setForeground(QColor(plate_text_color))
            plate_font = QFont()
            plate_font.setBold(True)
            plate_item.setFont(plate_font)
            
            self.table.setItem(row, 0, plate_item)
            
            # Category with icon
            category = vehicle.vehicle_category
            icon = CATEGORY_ICONS.get(category, '?')
            category_item = QTableWidgetItem(f"{icon} {category}")
            self.table.setItem(row, 1, category_item)
            
            # Make/Model
            make_item = QTableWidgetItem(vehicle.vehicle_make)
            self.table.setItem(row, 2, make_item)
            
            # Owner
            owner_item = QTableWidgetItem(vehicle.owner_name)
            self.table.setItem(row, 3, owner_item)
            
            # Speed
            speed_item = QTableWidgetItem(f"{vehicle.speed:.1f}")
            self.table.setItem(row, 4, speed_item)
            
            # STNK
            stnk_item = QTableWidgetItem(vehicle.stnk_status)
            self.table.setItem(row, 5, stnk_item)
            
            # SIM
            sim_item = QTableWidgetItem(vehicle.sim_status)
            self.table.setItem(row, 6, sim_item)
    
    def on_vehicle_selected(self, row, column):
        """Handle vehicle selection in table"""
        if 0 <= row < len(self.vehicles):
            vehicle = self.vehicles[row]
            details = VehicleDisplayFormatter.get_vehicle_details(vehicle)
            self.detail_display.setText(details)
    
    def update_statistics(self):
        """Update statistics display"""
        if not self.vehicles:
            self.stats_display.setText("No vehicles generated yet.")
            return
        
        stats = VehicleDisplayFormatter.get_statistics(self.vehicles)
        
        stats_text = f"""
Batch Statistics (Total: {stats['total_vehicles']} vehicles)

Distribution by Category:
"""
        
        for category, count in sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True):
            pct = (count / stats['total_vehicles']) * 100
            stats_text += f"  {category:15s}: {count:3d} ({pct:5.1f}%)\n"
        
        stats_text += f"""
Distribution by Plate Color:
"""
        
        for color, count in sorted(stats['plate_colors'].items(), key=lambda x: x[1], reverse=True):
            pct = (count / stats['total_vehicles']) * 100
            stats_text += f"  {color:10s}: {count:3d} ({pct:5.1f}%)\n"
        
        stats_text += f"""
Speed Statistics:
  Average: {stats['avg_speed']:.1f} km/h
  Maximum: {stats['max_speed']:.1f} km/h
  Minimum: {stats['min_speed']:.1f} km/h
"""
        
        self.stats_display.setText(stats_text)
    
    def closeEvent(self, event):
        """Handle window close"""
        self.update_timer.stop()
        if self.generator_thread and self.generator_thread.isRunning():
            self.generator_thread.stop_generation()
        event.accept()


if __name__ == '__main__':
    # Import PyQt5 application
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    gui = TrafficSimulationGUI()
    gui.show()
    sys.exit(app.exec_())
