from PyQt5.QtWidgets import QApplication, QLabel
import sys
from gui_traffic_simulation import ViolationDetailDialog

app = QApplication(sys.argv)
violation = {
    'license_plate':'KT 123 A AB',
    'owner_region':'KT',
    'owner_name':'Test Owner',
    'owner_id':'6401010101010001',
    'stnk_status':'Active',
    'sim_status':'Active',
    'speed':80,
    'fine_amount':10,
    'penalty_multiplier':1,
    'timestamp':'2026-01-31 12:00:00'
}

d = ViolationDetailDialog(violation)
labels = [w.text() for w in d.findChildren(QLabel)]
print('\n'.join(labels))
