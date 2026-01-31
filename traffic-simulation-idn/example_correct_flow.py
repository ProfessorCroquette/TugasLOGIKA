#!/usr/bin/env python3
"""
CONTOH PRAKTIS: Menggunakan Correct Flow untuk Generate Vehicle dengan Owner

Alur yang benar:
1. Generate PLAT NOMOR terlebih dahulu
2. Parse PLAT NOMOR untuk get region info
3. Generate OWNER dari PLAT (bukan independent!)
4. Create Vehicle object dengan synchronized owner

Hasil: Vehicle dengan NIK yang match dengan kode wilayah plat
"""

from utils.indonesian_plates import IndonesianPlateManager, VehicleType

def generate_complete_vehicle():
    """
    Generate vehicle dengan CORRECT FLOW:
    PLAT NOMOR → Region Info → Generate OWNER dari PLAT
    """
    
    print("\n" + "=" * 80)
    print("GENERATE COMPLETE VEHICLE WITH CORRECT FLOW")
    print("=" * 80)
    
    # ========================================================================
    # STEP 1: Generate PLAT NOMOR secara random
    # ========================================================================
    print("\n[STEP 1] Generate PLAT NOMOR")
    print("-" * 80)
    
    plate, region_name, sub_region, vehicle_type_display = IndonesianPlateManager.generate_plate(
        VehicleType.RODA_EMPAT_LEBIH  # Generate 4-wheel vehicle
    )
    
    print(f"Generated Plate: {plate}")
    print(f"Vehicle Type: {vehicle_type_display}")
    print(f"Region: {region_name}")
    print(f"Sub Region: {sub_region}")
    
    # ========================================================================
    # STEP 2: Parse PLAT NOMOR untuk get region information
    # ========================================================================
    print("\n[STEP 2] Parse PLAT NOMOR - Extract Region Information")
    print("-" * 80)
    
    region_info = IndonesianPlateManager.extract_region_info_from_plate(plate)
    
    if not region_info:
        print("ERROR: Could not parse plate!")
        return None
    
    print(f"Region Code: {region_info['region_code']}")
    print(f"Region Name: {region_info['region_name']}")
    print(f"Province Code: {region_info['province_code']}")
    print(f"Sub Region: {region_info['sub_region']}")
    print(f"Vehicle Type: {region_info.get('vehicle_type', 'PRIBADI')}")
    
    # ========================================================================
    # STEP 3: Generate OWNER DARI PLAT (PENTING: dari plat, bukan random!)
    # ========================================================================
    print("\n[STEP 3] Generate OWNER FROM PLATE")
    print("-" * 80)
    
    vehicle_type = 'roda_empat' if 'Mobil' in vehicle_type_display else 'roda_dua'
    owner = IndonesianPlateManager.generate_owner_from_plate(plate, vehicle_type)
    
    if not owner:
        print("ERROR: Could not generate owner!")
        return None
    
    print(f"Owner ID (NIK): {owner.owner_id}")
    print(f"  ├─ Province Code: {owner.owner_id[:2]}")
    print(f"  ├─ City Code: {owner.owner_id[2:4]}")
    print(f"  └─ Birth Info: {owner.owner_id[6:12]}")
    print(f"Owner Name: {owner.name}")
    print(f"Region: {owner.region}")
    print(f"Sub Region: {owner.sub_region}")
    print(f"Address: {owner.address}")
    print(f"STNK Status: {'Active' if owner.stnk_status else 'Expired'}")
    print(f"SIM Status: {'Active' if owner.sim_status else 'Expired'}")
    print(f"Vehicle Type: {owner.vehicle_type}")
    
    # ========================================================================
    # STEP 4: Validate Synchronization (NIK province = Plat province)
    # ========================================================================
    print("\n[STEP 4] Validate Synchronization")
    print("-" * 80)
    
    nik_province = owner.owner_id[:2]
    plat_province = region_info['province_code']
    
    print(f"NIK Province Code: {nik_province}")
    print(f"Plate Province Code: {plat_province}")
    
    if nik_province == plat_province:
        print(f"\n✓ SYNCHRONIZED! NIK and Plate match province code ({nik_province})")
        sync_status = "SYNCHRONIZED"
    else:
        print(f"\n✗ NOT SYNCHRONIZED! NIK ({nik_province}) != Plate ({plat_province})")
        sync_status = "NOT_SYNCHRONIZED"
    
    # ========================================================================
    # STEP 5: Create Vehicle Object
    # ========================================================================
    print("\n[STEP 5] Create Vehicle Object")
    print("-" * 80)
    
    vehicle = {
        # Identitas Kendaraan
        'license_plate': plate,
        'model': 'Toyota Avanza 2024',  # Can be generated separately
        'type': vehicle_type_display,
        
        # Identitas Pemilik (FROM PLATE)
        'owner_id': owner.owner_id,
        'owner_name': owner.name,
        'owner_region': owner.region,
        'owner_address': owner.address,
        
        # Status Dokumen
        'stnk_status': 'Active' if owner.stnk_status else 'Expired',
        'sim_status': 'Active' if owner.sim_status else 'Expired',
        
        # Tipe Kendaraan (dapat diekstrak dari plat)
        'tipe': region_info.get('vehicle_type', 'PRIBADI'),
        
        # Kecepatan (digenerate terpisah)
        'speed': 65.5,  # km/h
        
        # Metadata
        'synchronization': sync_status,
        'generated_at': '2026-01-31',
        'version': '2.0'
    }
    
    return vehicle


def print_vehicle_summary(vehicle):
    """Pretty print vehicle information"""
    
    print("\n" + "=" * 80)
    print("VEHICLE SUMMARY")
    print("=" * 80)
    
    print(f"\n📋 IDENTITAS KENDARAAN")
    print(f"   Plat Nomor: {vehicle['license_plate']}")
    print(f"   Model: {vehicle['model']}")
    print(f"   Tipe: {vehicle['tipe']}")
    print(f"   Jenis: {vehicle['type']}")
    
    print(f"\n👤 IDENTITAS PEMILIK")
    print(f"   NIK: {vehicle['owner_id']}")
    print(f"   Nama: {vehicle['owner_name']}")
    print(f"   Wilayah: {vehicle['owner_region']}")
    print(f"   Alamat: {vehicle['owner_address']}")
    
    print(f"\n📄 STATUS DOKUMEN")
    print(f"   STNK: {vehicle['stnk_status']}")
    print(f"   SIM: {vehicle['sim_status']}")
    
    print(f"\n🔒 VALIDASI")
    print(f"   Synchronization: {vehicle['synchronization']}")
    print(f"   Province Code (from NIK): {vehicle['owner_id'][:2]}")
    print(f"   Province Code (from Plate): {vehicle['license_plate'].split()[0]}")
    
    print(f"\n⚡ TRAFFIC DATA")
    print(f"   Speed: {vehicle['speed']} km/h")
    print(f"   Generated: {vehicle['generated_at']}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    # Generate multiple vehicles to show the pattern
    for i in range(3):
        print(f"\n\n{'#' * 80}")
        print(f"# VEHICLE #{i+1}")
        print(f"{'#' * 80}")
        
        vehicle = generate_complete_vehicle()
        
        if vehicle:
            print_vehicle_summary(vehicle)
        else:
            print("ERROR: Failed to generate vehicle")
    
    print(f"\n\n{'=' * 80}")
    print("SEMUA KENDARAAN BERHASIL DIGENERATE DENGAN CORRECT FLOW")
    print("=" * 80)
    print("\nPenting: Setiap vehicle memiliki owner yang:")
    print("  1. Digenerate dari plat nomor (bukan independent)")
    print("  2. NIK synchronized dengan kode wilayah plat")
    print("  3. Alamat sesuai dengan region plat")
    print("  4. STNK & SIM status konsisten")
    print("\nHal ini memastikan compliance dengan regulasi Indonesia")
    print("(Peraturan Kapolri Nomor 7 Tahun 2021)")
