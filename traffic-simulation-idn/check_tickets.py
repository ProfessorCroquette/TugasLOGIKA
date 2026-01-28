import json
from pathlib import Path

f = json.load(open(Path('data_files/tickets.json')))
print(f'✅ Generated {len(f)} tickets')
if f:
    t = f[0]
    print(f'First ticket:')
    print(f'  vehicle_type: {t.get("vehicle_type")}')
    print(f'  license_plate: {t.get("license_plate")}')
    print(f'  owner: {t.get("owner")}')
    print(f'  registration: {t.get("registration")}')
