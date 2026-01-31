"""Final verification of synchronized vehicle generation"""

from utils.indonesian_plates import OwnerDatabase
from utils.plate_ktp_sync import PlateKTPSync

print("\n" + "="*70)
print("FINAL VERIFICATION - SYNCHRONIZED VEHICLE GENERATION")
print("="*70 + "\n")

db = OwnerDatabase()
test_plates = ['B 1111 UA', 'D 2222 UD', 'H 3333 UH', 'L 4444 UL', 'P 5555 UP', 'AB 6666 UAA']

all_sync = True
for plate in test_plates:
    owner = db.get_or_create_owner(plate)
    is_sync, msg = PlateKTPSync.validate_plate_ktp_sync(plate, owner.owner_id)
    
    status = "✓ SINKRON" if is_sync else "✗ TIDAK SINKRON"
    print(f"Plate: {plate:15} | NIK: {owner.owner_id} | {status}")
    
    if not is_sync:
        all_sync = False

print("\n" + "="*70)
if all_sync:
    print("✓✓✓ SUCCESS - ALL VEHICLES ARE SYNCHRONIZED! ✓✓✓")
    print("The plate and KTP generation are perfectly synchronized!")
else:
    print("✗✗✗ FAILED - Some vehicles are not synchronized ✗✗✗")
print("="*70 + "\n")
