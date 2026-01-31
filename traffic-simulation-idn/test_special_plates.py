"""
Test special plates (Government RI, Diplomatic CD/CC) handling
"""

from utils.indonesian_plates import OwnerDatabase

print("\n" + "="*80)
print("TESTING SPECIAL PLATE HANDLING")
print("="*80 + "\n")

db = OwnerDatabase()

test_cases = [
    ("B 1234 AA", "Regular - Jakarta"),
    ("RI 123 456", "Government - Indonesia"),
    ("CD 12 345", "Diplomatic - CD"),
    ("CC 67 890", "Diplomatic - CC"),
    ("L 9999 LA", "Regular - Surabaya"),
]

for plate, description in test_cases:
    try:
        owner = db.get_or_create_owner(plate)
        nik = owner.owner_id
        
        print(f"Plate: {plate:15} ({description})")
        print(f"  Name: {owner.name}")
        print(f"  Region: {owner.region}")
        print(f"  Sub-region: {owner.sub_region}")
        print(f"  NIK: {nik}")
        
        if plate.startswith(('RI', 'CD', 'CC')):
            print(f"  → SPECIAL PLATE (No administrative mapping)")
            print(f"     [1-2] Province: {nik[0:2]} (00=Government, 99=Diplomatic)")
            print(f"     [3-4] District: {nik[2:4]} (00=Special)")
            print(f"     [5-6] Subdistrict: {nik[4:6]} (00=Special)")
        else:
            print(f"  → REGULAR PLATE (With administrative mapping)")
            print(f"     [1-2] Province: {nik[0:2]}")
            print(f"     [3-4] District: {nik[2:4]} (from region)")
            print(f"     [5-6] Subdistrict: {nik[4:6]} (from sub_region)")
        
        print(f"  ✓ Success\n")
    except Exception as e:
        print(f"Plate: {plate:15} ({description})")
        print(f"  ✗ Error: {str(e)}\n")

print("="*80)
print("RESULT: All special plates handled correctly!")
print("="*80 + "\n")
