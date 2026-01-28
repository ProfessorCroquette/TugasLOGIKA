"""
Indonesian License Plate Generator - Demonstration Script
Shows all plate types and specifications in action
"""

from utils.plate_generator import (
    PlatGenerator, PlateType, TruckSubType, TruckClass,
    GovernmentAgency, DiplomaticCountry, TourRoute
)
import json


def print_section(title: str, char: str = "=") -> None:
    """Print a formatted section header"""
    print(f"\n{char * 80}")
    print(f"{title:^80}")
    print(f"{char * 80}\n")


def print_plate_details(result: dict, indent: int = 0) -> None:
    """Pretty print plate generation result"""
    prefix = " " * indent
    print(f"{prefix}Plat Nomor    : {result['plate']}")
    print(f"{prefix}Jenis         : {result['type']}")
    print(f"{prefix}Warna         : {result['color']}")
    print(f"{prefix}Deskripsi     : {result.get('description', 'N/A')}")
    
    if 'region_name' in result:
        print(f"{prefix}Wilayah       : {result['region_name']}")
    
    if 'truck_subtype' in result:
        print(f"{prefix}Tipe Truk     : {result['truck_subtype']}")
        print(f"{prefix}Kelas Truk    : {result['truck_class']} ({result['truck_weight']})")
        print(f"{prefix}Rute          : {result['route']}")
    
    if 'agency_name' in result:
        print(f"{prefix}Instansi      : {result['agency_name']}")
    
    if 'country_name' in result:
        print(f"{prefix}Negara        : {result['country_name']}")
        print(f"{prefix}Jenis Dip     : {result['diplomatic_type']}")
    
    if 'expiry_date' in result:
        print(f"{prefix}Berlaku Hingga: {result['expiry_date']}")


def demo_private_plates():
    """Demonstrate private vehicle plate generation"""
    print_section("DEMO 1: KENDARAAN PRIBADI (PLAT HITAM)", "=")
    
    gen = PlatGenerator()
    
    print("Format: [KodeWilayah] [1-4 digit] [1-3 huruf]\n")
    print("Contoh Kendaraan Pribadi:\n")
    
    for i in range(5):
        result = gen.generate_private_plate()
        print(f"Plat {i+1}:")
        print_plate_details(result, indent=2)
        print()


def demo_commercial_plates():
    """Demonstrate commercial vehicle plate generation"""
    print_section("DEMO 2: KENDARAAN NIAGA (PLAT KUNING)", "=")
    
    gen = PlatGenerator()
    
    print("Format: [KodeWilayah] [1-4 digit] [1-3 huruf] (NIAGA)\n")
    print("Contoh Kendaraan Niaga:\n")
    
    for i in range(5):
        result = gen.generate_commercial_plate()
        print(f"Plat {i+1}:")
        print_plate_details(result, indent=2)
        print()


def demo_truck_plates():
    """Demonstrate truck plate generation"""
    print_section("DEMO 3: KENDARAAN TRUK (PLAT KUNING KHUSUS)", "=")
    
    gen = PlatGenerator()
    
    print("Format: [KodeWilayah] [1-4 digit] [T/K/G/D][1-3 huruf] (TRUK-BERAT)\n")
    print("Keterangan Kode Truk:")
    print("  T = Truk Bak Terbuka (Flatbed)")
    print("  K = Truk Kontainer")
    print("  G = Truk Tangki (Gas/Oli)")
    print("  D = Truk Dump\n")
    
    # Truck types and classes
    truck_configs = [
        (TruckSubType.GENERAL, TruckClass.LIGHT, "Truk Umum - Ringan"),
        (TruckSubType.CONTAINER, TruckClass.MEDIUM, "Truk Kontainer - Sedang"),
        (TruckSubType.TANKER, TruckClass.HEAVY, "Truk Tangki - Berat"),
        (TruckSubType.DUMP, TruckClass.HEAVY, "Truk Dump - Berat"),
        (TruckSubType.FLATBED, TruckClass.MEDIUM, "Truk Bak - Sedang"),
    ]
    
    print("Contoh Kendaraan Truk:\n")
    
    for truck_type, truck_class, title in truck_configs:
        result = gen.generate_truck_plate(truck_type=truck_type, truck_class=truck_class)
        print(f"{title}:")
        print_plate_details(result, indent=2)
        print()


def demo_government_plates():
    """Demonstrate government vehicle plate generation"""
    print_section("DEMO 4: KENDARAAN PEMERINTAH (PLAT MERAH)", "=")
    
    gen = PlatGenerator()
    
    print("Format: RI [KodeInstansi] [1-4 digit]\n")
    print("Kode Instansi Pemerintah:")
    print("  1 = Kepolisian (Polri)")
    print("  2 = TNI Angkatan Darat (TNI AD)")
    print("  3 = TNI Angkatan Laut (TNI AL)")
    print("  4 = TNI Angkatan Udara (TNI AU)")
    print("  5 = Kepresidenan")
    print("  6 = DPR/MPR/DPD (Legislatif)")
    print("  7 = Kementerian")
    print("  8 = Pemerintah Daerah")
    print("  9 = Lembaga Penegak Hukum\n")
    
    agencies = [
        GovernmentAgency.POLICE,
        GovernmentAgency.ARMY_LAND,
        GovernmentAgency.ARMY_NAVY,
        GovernmentAgency.ARMY_AIR,
        GovernmentAgency.PRESIDENCY,
        GovernmentAgency.PARLIAMENT,
        GovernmentAgency.MINISTRY,
        GovernmentAgency.LOCAL_GOV,
    ]
    
    print("Contoh Kendaraan Pemerintah:\n")
    
    for agency in agencies:
        result = gen.generate_government_plate(agency=agency)
        print(f"{result['agency_name']}:")
        print_plate_details(result, indent=2)
        print()


def demo_diplomatic_plates():
    """Demonstrate diplomatic vehicle plate generation"""
    print_section("DEMO 5: KENDARAAN DIPLOMATIK (PLAT PUTIH)", "=")
    
    gen = PlatGenerator()
    
    print("Format: [CD/CC] [KodeNegara] [1-4 digit]\n")
    print("Jenis Diplomatik:")
    print("  CD = Corps Diplomatic")
    print("  CC = Consular Corps\n")
    
    countries = [
        (DiplomaticCountry.USA, False, "Duta Besar"),
        (DiplomaticCountry.USA, True, "Konsulat"),
        (DiplomaticCountry.JAPAN, False, "Duta Besar"),
        (DiplomaticCountry.AUSTRALIA, False, "Duta Besar"),
        (DiplomaticCountry.UK, False, "Duta Besar"),
    ]
    
    print("Contoh Kendaraan Diplomatik:\n")
    
    for country, is_consular, title in countries:
        result = gen.generate_diplomatic_plate(country=country, is_consular=is_consular)
        print(f"{title} {country.value[1]}:")
        print_plate_details(result, indent=2)
        print()


def demo_temporary_plates():
    """Demonstrate temporary vehicle plate generation"""
    print_section("DEMO 6: KENDARAAN SEMENTARA (PLAT PUTIH-MERAH)", "=")
    
    gen = PlatGenerator()
    
    print("Format: [KodeWilayah] [1-4 digit] [1-3 huruf] (SEMENTARA) - EXP: DD/MM/YYYY\n")
    print("Contoh Kendaraan Sementara:\n")
    
    for i in range(5):
        result = gen.generate_temporary_plate(valid_days=180)
        print(f"Plat {i+1}:")
        print_plate_details(result, indent=2)
        print()


def demo_trial_plates():
    """Demonstrate trial/dealer vehicle plate generation"""
    print_section("DEMO 7: KENDARAAN UJI COBA/DEALER (PLAT PUTIH-BIRU)", "=")
    
    gen = PlatGenerator()
    
    print("Format: KB [1-4 digit] [1-3 huruf] (UJI COBA) - EXP: DD/MM/YYYY\n")
    print("Contoh Kendaraan Uji Coba:\n")
    
    for i in range(5):
        result = gen.generate_trial_plate(valid_days=365)
        print(f"Plat {i+1}:")
        print_plate_details(result, indent=2)
        print()


def demo_random_generation():
    """Demonstrate random plate generation"""
    print_section("DEMO 8: GENERASI ACAK SEMUA JENIS PLAT", "=")
    
    gen = PlatGenerator()
    
    print("Contoh Plat Acak dari Semua Jenis:\n")
    
    for i in range(10):
        result = gen.generate_random_plate()
        print(f"Plat {i+1}: {result['plate']:40} ({result['type']})")


def demo_validation():
    """Demonstrate plate validation"""
    print_section("DEMO 9: VALIDASI PLAT NOMOR", "=")
    
    gen = PlatGenerator()
    
    test_plates = [
        "B 1234 ABC",           # Valid private
        "B 5678 XY (NIAGA)",    # Valid commercial
        "RI 1 1234",            # Valid government
        "CD 71 123",            # Valid diplomatic
        "KB 1234 AB",           # Valid trial
        "B 1234 IOQ",           # Invalid - forbidden letters
        "D 0000 XYZ",           # Invalid - zero not allowed
    ]
    
    print("Hasil Validasi Plat:\n")
    
    for plate in test_plates:
        validation = gen.validate_plate(plate)
        
        status = "✓ VALID" if validation['valid'] else "✗ TIDAK VALID"
        print(f"{status:15} | {plate:30} | Tipe: {validation['plate_type']}")
        
        if validation['errors']:
            for error in validation['errors']:
                print(f"               | └─ Error: {error}")
        print()


def demo_statistics():
    """Demonstrate generator statistics"""
    print_section("DEMO 10: STATISTIK GENERATOR", "=")
    
    gen = PlatGenerator()
    
    print("Generating 100 random plates...\n")
    
    type_count = {}
    for _ in range(100):
        result = gen.generate_random_plate()
        plate_type = result['type']
        type_count[plate_type] = type_count.get(plate_type, 0) + 1
    
    print("Distribusi Plat yang Digenerate:\n")
    
    total = gen.get_generated_plates_count()
    for plate_type, count in sorted(type_count.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total) * 100
        bar_length = int(percentage / 2)
        bar = "█" * bar_length
        print(f"{plate_type:20} | {count:3} | {bar:40} ({percentage:5.1f}%)")
    
    print(f"\nTotal Plat Unik Digenerate: {total}")


def demo_complete_vehicle_info():
    """Demonstrate complete vehicle information display"""
    print_section("DEMO 11: INFORMASI KENDARAAN LENGKAP", "=")
    
    gen = PlatGenerator()
    
    vehicle_configs = [
        ("MOBIL PRIBADI", lambda: gen.generate_private_plate()),
        ("MOBIL NIAGA", lambda: gen.generate_commercial_plate()),
        ("TRUK KONTAINER BERAT", lambda: gen.generate_truck_plate(
            TruckSubType.CONTAINER, TruckClass.HEAVY)),
        ("KENDARAAN POLISI", lambda: gen.generate_government_plate(
            GovernmentAgency.POLICE)),
        ("KENDARAAN DIPLOMATIK AS", lambda: gen.generate_diplomatic_plate(
            DiplomaticCountry.USA, False)),
    ]
    
    for title, generator_func in vehicle_configs:
        result = generator_func()
        
        print(f"+{'-'*88}+")
        print(f"| {title:88} |")
        print(f"+{'-'*88}+")
        print(f"| Plat Nomor    : {result['plate']:62} |")
        print(f"| Jenis Kendaraan: {result['type']:60} |")
        print(f"| Warna Plat    : {result['color']:62} |")
        print(f"| Deskripsi     : {result.get('description', 'N/A'):62} |")
        print(f"+{'-'*88}+")
        print()


def main():
    """Run all demonstrations"""
    print("\n")
    print("=" * 90)
    print("GENERATOR PLAT NOMOR KENDARAAN INDONESIA".center(90))
    print("Sesuai Nomenklatur Resmi Polri & Peraturan Ganjil".center(90))
    print("=" * 90)
    print()
    print("Program ini menghasilkan plat nomor yang 100% sesuai dengan:")
    print("  * Struktur resmi Polri")
    print("  * Validasi karakter (tanpa I, O, Q)")
    print("  * Kode wilayah lengkap")
    print("  * Spesifikasi khusus per jenis kendaraan")
    print()
    
    # Run all demos
    demo_private_plates()
    demo_commercial_plates()
    demo_truck_plates()
    demo_government_plates()
    demo_diplomatic_plates()
    demo_temporary_plates()
    demo_trial_plates()
    demo_random_generation()
    demo_validation()
    demo_statistics()
    demo_complete_vehicle_info()
    
    print_section("DOKUMENTASI LENGKAP SELESAI", "=")
    print("\nGenerator ini siap digunakan untuk:")
    print("  * Simulasi traffic dengan plat yang realistis")
    print("  * Testing sistem manajemen kendaraan")
    print("  * Penelitian tentang nomenklatur plat Indonesia")
    print("  * Integrasi dengan aplikasi transportasi\n")


if __name__ == "__main__":
    main()
