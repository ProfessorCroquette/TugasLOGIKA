#!/usr/bin/env python3
import json

tickets = json.load(open('data_files/tickets.json'))
slow = [t for t in tickets if t['speed'] < 40]
speeding = [t for t in tickets if t['speed'] > 75.9]

print(f'Total tickets: {len(tickets)}')
print(f'Slow violations: {len(slow)}')
print(f'Speeding violations: {len(speeding)}')
print(f'\nSample slow tickets:')
for t in slow[:5]:
    print(f"  {t['license_plate']}: {t['speed']} km/h")
print(f'\nSample speeding tickets:')
for t in speeding[:5]:
    print(f"  {t['license_plate']}: {t['speed']} km/h")
