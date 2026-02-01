"""
Indonesian License Plate Management System
Implements complete Indonesian plate nomenclature per official format
Supports both Roda Dua (motorcycles) and Roda Empat atau lebih (4+ wheels)
Format: [RegionCode] [4-digit number] [SubCode] [Owner letters]
Examples:
  - Motor: B 1234 U AB
  - Mobil: B 5678 P ABC
"""

import json
import random
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from pathlib import Path
from enum import Enum


class VehicleType(Enum):
    """Vehicle classification per Indonesian regulations"""
    RODA_DUA = "Roda Dua (Motor)"
    RODA_EMPAT_LEBIH = "Roda Empat atau lebih (Mobil)"


class VehicleCategory(Enum):
    """Vehicle category per Indonesian License Plate Regulations
    
    Categories determine plate suffix and color:
    - Pribadi: Private vehicles (no suffix, black plate)
    - Umum: Public transport (H suffix, yellow plate)
    - Barang: Commercial goods (K suffix, yellow plate)
    - Pemerintah: Government (no suffix, red plate)
    - Diplomatik: Diplomatic (CD/CC + country code, white plate)
    - Sementara: Temporary/Test (TMP suffix, white plate)
    - Alat Berat: Heavy equipment (BG suffix, white plate)
    """
    PRIBADI = "Pribadi"           # Private: B 1234 ABC
    UMUM = "Umum"                 # Public: B 1234 UD H
    BARANG = "Barang"             # Commercial: B 1234 XY K
    PEMERINTAH = "Pemerintah"     # Government: B 1234 CD
    DIPLOMATIK = "Diplomatik"     # Diplomatic: CD 12 123
    SEMENTARA = "Sementara"       # Temporary: B 1234 TMP
    ALAT_BERAT = "Alat Berat"    # Heavy: L 987 TA BG


class IndonesianPlateManager:
    """Manages Indonesian license plate generation following official nomenclature"""
    
    OWNER_CODE_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # Complete Indonesian plate data per official regulations (Peraturan Kapolri Nomor 7 Tahun 2021)
    # Updated with comprehensive regional mapping from Wikipedia (Jan 31, 2026)
    PLATE_DATA = {
        # SUMATRA BAGIAN UTARA (North Sumatra Region)
        'BL': {
            'region_name': 'Aceh',
            'province_code': '11',
            'area': 'Sumatra Bagian Utara',
            'sub_codes': {
                'A': 'Kota Banda Aceh', 'J': 'Kota Banda Aceh', 'B': 'Gayo Lues', 'C': 'Aceh Barat Daya',
                'D': 'Aceh Timur', 'E': 'Aceh Barat', 'F': 'Kota Langsa', 'G': 'Aceh Tengah',
                'H': 'Aceh Tenggara', 'I': 'Kota Subulussalam', 'K': 'Aceh Utara', 'Q': 'Aceh Utara',
                'L': 'Aceh Besar', 'M': 'Kota Sabang', 'N': 'Kota Lhokseumawe', 'O': 'Pidie Jaya',
                'P': 'Pidie', 'R': 'Aceh Singkil', 'S': 'Simeulue', 'T': 'Aceh Selatan',
                'U': 'Aceh Tamiang', 'V': 'Nagan Raya', 'W': 'Aceh Jaya', 'Y': 'Bener Meriah',
                'Z': 'Bireuen'
            }
        },
        'BB': {
            'region_name': 'Sumatera Utara Barat (Tapanuli)',
            'province_code': '12',
            'area': 'Sumatra Bagian Utara',
            'sub_codes': {
                'A': 'Kota Sibolga', 'L': 'Kota Sibolga', 'N': 'Kota Sibolga', 'B': 'Tapanuli Utara',
                'C': 'Samosir', 'D': 'Humbang Hasundutan', 'E': 'Toba', 'F': 'Kota Padang Sidempuan',
                'H': 'Kota Padang Sidempuan', 'G': 'Tapanuli Selatan', 'J': 'Padang Lawas Utara',
                'K': 'Padang Lawas', 'M': 'Tapanuli Tengah', 'Q': 'Nias Utara', 'R': 'Mandailing Natal',
                'T': 'Kota Gunungsitoli', 'U': 'Nias Barat', 'V': 'Nias', 'W': 'Nias Selatan',
                'Y': 'Dairi', 'Z': 'Pakpak Bharat'
            }
        },
        'BK': {
            'region_name': 'Sumatera Utara Timur (Pesisir Timur Sumatra)',
            'province_code': '12',
            'area': 'Sumatra Bagian Utara',
            'sub_codes': {
                'A': 'Kota Medan', 'B': 'Kota Medan', 'C': 'Kota Medan', 'D': 'Kota Medan',
                'E': 'Kota Medan', 'F': 'Kota Medan', 'G': 'Kota Medan', 'H': 'Kota Medan',
                'I': 'Kota Medan', 'K': 'Kota Medan', 'L': 'Kota Medan', 'J': 'Labuhanbatu Utara',
                'M': 'Deli Serdang', 'N': 'Kota Tebing Tinggi', 'O': 'Batubara', 'P': 'Langkat',
                'Q': 'Kota Tanjung Balai', 'R': 'Kota Binjai', 'S': 'Karo', 'T': 'Simalungun',
                'U': 'Simalungun', 'V': 'Asahan', 'W': 'Kota Pematang Siantar', 'X': 'Serdang Bedagai',
                'Y': 'Labuhanbatu', 'Z': 'Labuhanbatu Selatan'
            }
        },
        
        # SUMATRA BAGIAN SELATAN (South Sumatra Region)
        'BA': {
            'region_name': 'Sumatera Barat',
            'province_code': '13',
            'area': 'Sumatra Bagian Selatan',
            'sub_codes': {
                'A': 'Kota Padang', 'B': 'Kota Padang', 'O': 'Kota Padang', 'Q': 'Kota Padang',
                'C': 'Lima Puluh Kota', 'X': 'Lima Puluh Kota', 'D': 'Pasaman', 'E': 'Tanah Datar',
                'F': 'Padang Pariaman', 'G': 'Pesisir Selatan', 'I': 'Pesisir Selatan', 'H': 'Solok',
                'J': 'Kota Sawahlunto', 'K': 'Sijunjung', 'L': 'Kota Bukittinggi', 'M': 'Kota Payakumbuh',
                'N': 'Kota Padang Panjang', 'P': 'Kota Solok', 'S': 'Pasaman Barat', 'T': 'Agam',
                'Z': 'Agam', 'U': 'Kepulauan Mentawai', 'V': 'Dharmasraya', 'W': 'Kota Pariaman',
                'Y': 'Solok Selatan'
            }
        },
        'BM': {
            'region_name': 'Riau',
            'province_code': '14',
            'area': 'Sumatra Bagian Selatan',
            'sub_codes': {
                'A': 'Kota Pekanbaru', 'J': 'Kota Pekanbaru', 'N': 'Kota Pekanbaru',
                'O': 'Kota Pekanbaru', 'Q': 'Kota Pekanbaru', 'T': 'Kota Pekanbaru',
                'V': 'Kota Pekanbaru', 'B': 'Indragiri Hulu', 'C': 'Pelalawan', 'I': 'Pelalawan',
                'D': 'Bengkalis', 'E': 'Bengkalis', 'F': 'Kampar', 'Z': 'Kampar',
                'G': 'Indragiri Hilir', 'H': 'Kota Dumai', 'R': 'Kota Dumai', 'K': 'Kuantan Singingi',
                'M': 'Rokan Hulu', 'U': 'Rokan Hulu', 'P': 'Rokan Hilir', 'W': 'Rokan Hilir',
                'S': 'Siak', 'Y': 'Siak'
            }
        },
        'BP': {
            'region_name': 'Kepulauan Riau',
            'province_code': '21',
            'area': 'Sumatra Bagian Selatan',
            'sub_codes': {
                'A': 'Kota Tanjung Pinang', 'P': 'Kota Tanjung Pinang', 'T': 'Kota Tanjung Pinang',
                'W': 'Kota Tanjung Pinang', 'B': 'Bintan', 'C': 'Kota Batam', 'D': 'Kota Batam',
                'E': 'Kota Batam', 'F': 'Kota Batam', 'G': 'Kota Batam', 'H': 'Kota Batam',
                'I': 'Kota Batam', 'J': 'Kota Batam', 'M': 'Kota Batam', 'O': 'Kota Batam',
                'Q': 'Kota Batam', 'R': 'Kota Batam', 'U': 'Kota Batam', 'V': 'Kota Batam',
                'X': 'Kota Batam', 'Z': 'Kota Batam', 'K': 'Karimun', 'L': 'Lingga',
                'N': 'Natuna', 'S': 'Kepulauan Anambas'
            }
        },
        'BH': {
            'region_name': 'Jambi',
            'province_code': '15',
            'area': 'Sumatra Bagian Selatan',
            'sub_codes': {
                'A': 'Kota Jambi', 'H': 'Kota Jambi', 'M': 'Kota Jambi', 'N': 'Kota Jambi',
                'Y': 'Kota Jambi', 'Z': 'Kota Jambi', 'B': 'Batanghari', 'V': 'Batanghari',
                'C': 'Tebo', 'W': 'Tebo', 'D': 'Kerinci', 'E': 'Tanjung Jabung Barat',
                'O': 'Tanjung Jabung Barat', 'F': 'Merangin', 'P': 'Merangin', 'X': 'Merangin',
                'G': 'Muaro Jambi', 'I': 'Muaro Jambi', 'J': 'Tanjung Jabung Timur',
                'T': 'Tanjung Jabung Timur', 'K': 'Bungo', 'U': 'Bungo', 'Q': 'Sarolangun',
                'S': 'Sarolangun', 'R': 'Kota Sungai Penuh'
            }
        },
        'BG': {
            'region_name': 'Sumatera Selatan',
            'province_code': '16',
            'area': 'Sumatra Bagian Selatan',
            'sub_codes': {
                'A': 'Kota Palembang', 'I': 'Kota Palembang', 'M': 'Kota Palembang',
                'N': 'Kota Palembang', 'O': 'Kota Palembang', 'R': 'Kota Palembang',
                'U': 'Kota Palembang', 'Z': 'Kota Palembang', 'B': 'Musi Banyuasin',
                'C': 'Kota Prabumulih', 'D': 'Muara Enim', 'E': 'Lahat', 'F': 'Ogan Komering Ulu',
                'G': 'Musi Rawas', 'H': 'Kota Lubuk Linggau', 'J': 'Banyuasin',
                'K': 'Ogan Komering Ilir', 'P': 'Penukal Abab Lematang Ilir', 'Q': 'Musi Rawas Utara',
                'S': 'Empat Lawang', 'T': 'Ogan Ilir', 'V': 'Ogan Komering Ulu Selatan',
                'W': 'Kota Pagaralam', 'Y': 'Ogan Komering Ulu Timur'
            }
        },
        'BD': {
            'region_name': 'Bengkulu',
            'province_code': '17',
            'area': 'Sumatra Bagian Selatan',
            'sub_codes': {
                'A': 'Kota Bengkulu', 'C': 'Kota Bengkulu', 'E': 'Kota Bengkulu', 'I': 'Kota Bengkulu',
                'U': 'Kota Bengkulu', 'V': 'Kota Bengkulu', 'B': 'Bengkulu Selatan', 'M': 'Bengkulu Selatan',
                'D': 'Bengkulu Utara', 'Q': 'Bengkulu Utara', 'S': 'Bengkulu Utara', 'F': 'Rejang Lebong',
                'K': 'Rejang Lebong', 'G': 'Kepahiang', 'H': 'Lebong', 'N': 'Muko Muko',
                'T': 'Muko Muko', 'P': 'Seluma', 'R': 'Seluma', 'W': 'Kaur', 'Y': 'Bengkulu Tengah'
            }
        },
        'BE': {
            'region_name': 'Lampung',
            'province_code': '18',
            'area': 'Sumatra Bagian Selatan',
            'sub_codes': {
                'A': 'Kota Bandar Lampung', 'B': 'Kota Bandar Lampung', 'C': 'Kota Bandar Lampung',
                'D': 'Lampung Selatan', 'E': 'Lampung Selatan', 'O': 'Lampung Selatan',
                'F': 'Kota Metro', 'G': 'Lampung Tengah', 'H': 'Lampung Tengah', 'I': 'Lampung Tengah',
                'J': 'Lampung Utara', 'K': 'Lampung Utara', 'L': 'Mesuji', 'M': 'Lampung Barat',
                'N': 'Lampung Timur', 'P': 'Lampung Timur', 'Q': 'Tulang Bawang Barat',
                'R': 'Pesawaran', 'S': 'Tulang Bawang', 'T': 'Tulang Bawang', 'U': 'Pringsewu',
                'V': 'Tanggamus', 'Z': 'Tanggamus', 'W': 'Way Kanan', 'X': 'Pesisir Barat'
            }
        },
        'BN': {
            'region_name': 'Kepulauan Bangka Belitung',
            'province_code': '19',
            'area': 'Sumatra Bagian Selatan',
            'sub_codes': {
                'A': 'Kota Pangkal Pinang', 'P': 'Kota Pangkal Pinang', 'B': 'Bangka', 'Q': 'Bangka',
                'C': 'Bangka Tengah', 'T': 'Bangka Tengah', 'D': 'Bangka Barat', 'R': 'Bangka Barat',
                'E': 'Bangka Selatan', 'V': 'Bangka Selatan', 'F': 'Belitung', 'W': 'Belitung',
                'G': 'Belitung Timur', 'X': 'Belitung Timur'
            }
        },
        
        # JAWA BAGIAN BARAT (West Java Region)
        'A': {
            'region_name': 'Banten',
            'province_code': '36',
            'area': 'Jawa Bagian Barat',
            'sub_codes': {
                'A': 'Kota Serang', 'B': 'Kota Serang', 'C': 'Kota Serang', 'D': 'Kota Serang',
                'E': 'Serang', 'F': 'Serang', 'G': 'Serang', 'H': 'Serang', 'I': 'Serang',
                'J': 'Pandeglang', 'K': 'Pandeglang', 'L': 'Pandeglang', 'M': 'Pandeglang',
                'N': 'Lebak', 'O': 'Lebak', 'P': 'Lebak', 'Q': 'Lebak', 'R': 'Kota Cilegon',
                'S': 'Kota Cilegon', 'T': 'Kota Cilegon', 'U': 'Kota Cilegon', 'V': 'Tangerang',
                'W': 'Tangerang', 'X': 'Tangerang', 'Y': 'Tangerang', 'Z': 'Tangerang'
            }
        },
        'B': {
            'region_name': 'DKI Jakarta',
            'province_code': '31',
            'area': 'Jawa Bagian Barat',
            'sub_codes': {
                'B': 'Jakarta Barat', 'H': 'Jakarta Barat', 'P': 'Jakarta Pusat', 'D': 'Jakarta Selatan',
                'S': 'Jakarta Selatan', 'R': 'Jakarta Timur', 'T': 'Jakarta Timur', 'U': 'Jakarta Utara',
                'E': 'Kota Depok', 'Z': 'Kota Depok', 'F': 'Kabupaten Bekasi', 'Y': 'Kabupaten Bekasi',
                'K': 'Kota Bekasi', 'J': 'Kabupaten Tangerang', 'C': 'Kota Tangerang',
                'V': 'Kota Tangerang', 'N': 'Kota Tangerang Selatan', 'W': 'Kota Tangerang Selatan',
                'A': 'Jawa Timur', 'G': 'Jakarta Barat', 'I': 'Jakarta Barat', 'L': 'Jawa Barat',
                'M': 'Jawa Barat', 'O': 'Jawa Barat', 'Q': 'Jawa Barat', 'X': 'Tangerang'
            }
        },
        'D': {
            'region_name': 'Jawa Barat (Priangan Tengah)',
            'province_code': '32',
            'area': 'Jawa Bagian Barat',
            'sub_codes': {
                'A': 'Kota Bandung', 'B': 'Kota Bandung', 'C': 'Kota Bandung', 'D': 'Kota Bandung',
                'E': 'Kota Bandung', 'F': 'Kota Bandung', 'G': 'Kota Bandung', 'H': 'Kota Bandung',
                'I': 'Kota Bandung', 'J': 'Kota Bandung', 'K': 'Kota Bandung', 'L': 'Kota Bandung',
                'M': 'Kota Bandung', 'N': 'Kota Bandung', 'O': 'Kota Bandung', 'P': 'Kota Bandung',
                'Q': 'Kota Bandung', 'R': 'Kota Bandung', 'S': 'Kota Cimahi', 'T': 'Kota Cimahi',
                'U': 'Bandung Barat', 'X': 'Bandung Barat', 'V': 'Kabupaten Bandung',
                'W': 'Kabupaten Bandung', 'Y': 'Kabupaten Bandung', 'Z': 'Kabupaten Bandung'
            }
        },
        'E': {
            'region_name': 'Jawa Barat (Keresidenan Cirebon)',
            'province_code': '32',
            'area': 'Jawa Bagian Barat',
            'sub_codes': {
                'A': 'Kota Cirebon', 'B': 'Kota Cirebon', 'C': 'Kota Cirebon', 'D': 'Kota Cirebon',
                'E': 'Kota Cirebon', 'F': 'Kota Cirebon', 'G': 'Kota Cirebon', 'H': 'Kabupaten Cirebon',
                'I': 'Kabupaten Cirebon', 'J': 'Kabupaten Cirebon', 'K': 'Kabupaten Cirebon',
                'L': 'Kabupaten Cirebon', 'M': 'Kabupaten Cirebon', 'N': 'Kabupaten Cirebon',
                'O': 'Kabupaten Cirebon', 'P': 'Indramayu', 'Q': 'Indramayu', 'R': 'Indramayu',
                'S': 'Indramayu', 'T': 'Indramayu', 'U': 'Majalengka', 'V': 'Majalengka',
                'W': 'Majalengka', 'X': 'Majalengka', 'Y': 'Kuningan', 'Z': 'Kuningan'
            }
        },
        'F': {
            'region_name': 'Jawa Barat (Keresidenan Bogor dan Priangan Barat)',
            'province_code': '32',
            'area': 'Jawa Bagian Barat',
            'sub_codes': {
                'A': 'Kota Bogor', 'B': 'Kota Bogor', 'C': 'Kota Bogor', 'D': 'Kota Bogor',
                'E': 'Kota Bogor', 'F': 'Kabupaten Bogor', 'G': 'Kabupaten Bogor', 'H': 'Kabupaten Bogor',
                'I': 'Kabupaten Bogor', 'J': 'Kabupaten Bogor', 'K': 'Kabupaten Bogor',
                'L': 'Kabupaten Bogor', 'M': 'Kabupaten Bogor', 'N': 'Kabupaten Bogor',
                'P': 'Kabupaten Bogor', 'R': 'Kabupaten Bogor', 'O': 'Kota Sukabumi',
                'S': 'Kota Sukabumi', 'T': 'Kota Sukabumi', 'Q': 'Kabupaten Sukabumi',
                'U': 'Kabupaten Sukabumi', 'V': 'Kabupaten Sukabumi', 'W': 'Cianjur',
                'X': 'Cianjur', 'Y': 'Cianjur', 'Z': 'Cianjur'
            }
        },
        'T': {
            'region_name': 'Jawa Barat (Keresidenan Karawang)',
            'province_code': '32',
            'area': 'Jawa Bagian Barat',
            'sub_codes': {
                'A': 'Purwakarta', 'B': 'Purwakarta', 'C': 'Purwakarta', 'I': 'Purwakarta',
                'J': 'Purwakarta', 'D': 'Karawang', 'E': 'Karawang', 'F': 'Karawang',
                'G': 'Karawang', 'H': 'Karawang', 'K': 'Karawang', 'L': 'Karawang',
                'M': 'Karawang', 'N': 'Karawang', 'O': 'Karawang', 'P': 'Karawang',
                'Q': 'Karawang', 'R': 'Karawang', 'S': 'Karawang', 'T': 'Subang',
                'U': 'Subang', 'V': 'Subang', 'W': 'Subang', 'X': 'Subang', 'Y': 'Subang',
                'Z': 'Subang'
            }
        },
        'Z': {
            'region_name': 'Jawa Barat (Priangan Timur dan Kabupaten Sumedang)',
            'province_code': '32',
            'area': 'Jawa Bagian Barat',
            'sub_codes': {
                'A': 'Sumedang', 'B': 'Sumedang', 'C': 'Sumedang', 'D': 'Garut',
                'E': 'Garut', 'F': 'Garut', 'G': 'Garut', 'H': 'Kota Tasikmalaya',
                'I': 'Kota Tasikmalaya', 'J': 'Kota Tasikmalaya', 'K': 'Kota Tasikmalaya',
                'L': 'Kota Tasikmalaya', 'M': 'Kota Tasikmalaya', 'N': 'Kabupaten Tasikmalaya',
                'O': 'Kabupaten Tasikmalaya', 'P': 'Kabupaten Tasikmalaya', 'Q': 'Kabupaten Tasikmalaya',
                'R': 'Kabupaten Tasikmalaya', 'S': 'Kabupaten Tasikmalaya', 'T': 'Ciamis',
                'V': 'Ciamis', 'W': 'Ciamis', 'U': 'Pangandaran', 'X': 'Kota Banjar',
                'Y': 'Kota Banjar', 'Z': 'Kota Banjar'
            }
        },
        
        # JAWA BAGIAN TENGAH (Central Java Region)
        'G': {
            'region_name': 'Jawa Tengah (Keresidenan Pekalongan)',
            'province_code': '33',
            'area': 'Jawa Bagian Tengah',
            'sub_codes': {
                'A': 'Kota Pekalongan', 'H': 'Kota Pekalongan', 'S': 'Kota Pekalongan',
                'B': 'Kabupaten Pekalongan', 'K': 'Kabupaten Pekalongan', 'O': 'Kabupaten Pekalongan',
                'T': 'Kabupaten Pekalongan', 'C': 'Batang', 'L': 'Batang', 'V': 'Batang',
                'D': 'Pemalang', 'I': 'Pemalang', 'M': 'Pemalang', 'W': 'Pemalang',
                'E': 'Kota Tegal', 'N': 'Kota Tegal', 'Y': 'Kota Tegal', 'F': 'Kabupaten Tegal',
                'P': 'Kabupaten Tegal', 'Q': 'Kabupaten Tegal', 'Z': 'Kabupaten Tegal',
                'G': 'Brebes', 'J': 'Brebes', 'R': 'Brebes', 'U': 'Brebes'
            }
        },
        'H': {
            'region_name': 'Jawa Tengah (Keresidenan Semarang)',
            'province_code': '33',
            'area': 'Jawa Bagian Tengah',
            'sub_codes': {
                'A': 'Kota Semarang', 'F': 'Kota Semarang', 'G': 'Kota Semarang',
                'H': 'Kota Semarang', 'P': 'Kota Semarang', 'Q': 'Kota Semarang',
                'R': 'Kota Semarang', 'S': 'Kota Semarang', 'W': 'Kota Semarang',
                'Y': 'Kota Semarang', 'Z': 'Kota Semarang', 'B': 'Kota Salatiga',
                'K': 'Kota Salatiga', 'O': 'Kota Salatiga', 'T': 'Kota Salatiga',
                'C': 'Kabupaten Semarang', 'I': 'Kabupaten Semarang', 'L': 'Kabupaten Semarang',
                'V': 'Kabupaten Semarang', 'D': 'Kendal', 'M': 'Kendal', 'U': 'Kendal',
                'E': 'Demak', 'J': 'Demak', 'N': 'Demak'
            }
        },
        'K': {
            'region_name': 'Jawa Tengah (Keresidenan Pati dan Grobogan)',
            'province_code': '33',
            'area': 'Jawa Bagian Tengah',
            'sub_codes': {
                'A': 'Pati', 'G': 'Pati', 'H': 'Pati', 'S': 'Pati', 'U': 'Pati',
                'B': 'Kudus', 'K': 'Kudus', 'O': 'Kudus', 'R': 'Kudus', 'T': 'Kudus',
                'C': 'Jepara', 'L': 'Jepara', 'Q': 'Jepara', 'V': 'Jepara', 'D': 'Rembang',
                'I': 'Rembang', 'M': 'Rembang', 'W': 'Rembang', 'E': 'Blora',
                'N': 'Blora', 'Y': 'Blora', 'F': 'Grobogan', 'J': 'Grobogan',
                'P': 'Grobogan', 'Z': 'Grobogan'
            }
        },
        'R': {
            'region_name': 'Jawa Tengah (Keresidenan Banyumas)',
            'province_code': '33',
            'area': 'Jawa Bagian Tengah',
            'sub_codes': {
                'A': 'Banyumas', 'E': 'Banyumas', 'G': 'Banyumas', 'H': 'Banyumas',
                'J': 'Banyumas', 'R': 'Banyumas', 'S': 'Banyumas', 'B': 'Cilacap',
                'F': 'Cilacap', 'K': 'Cilacap', 'N': 'Cilacap', 'P': 'Cilacap',
                'T': 'Cilacap', 'C': 'Purbalingga', 'L': 'Purbalingga', 'Q': 'Purbalingga',
                'U': 'Purbalingga', 'V': 'Purbalingga', 'Z': 'Purbalingga', 'D': 'Banjarnegara',
                'I': 'Banjarnegara', 'M': 'Banjarnegara', 'O': 'Banjarnegara',
                'W': 'Banjarnegara', 'Y': 'Banjarnegara'
            }
        },
        'AA': {
            'region_name': 'Jawa Tengah (Keresidenan Kedu)',
            'province_code': '33',
            'area': 'Jawa Bagian Tengah',
            'sub_codes': {
                'A': 'Kota Magelang', 'H': 'Kota Magelang', 'S': 'Kota Magelang',
                'U': 'Kota Magelang', 'B': 'Kabupaten Magelang', 'G': 'Kabupaten Magelang',
                'K': 'Kabupaten Magelang', 'O': 'Kabupaten Magelang', 'T': 'Kabupaten Magelang',
                'C': 'Purworejo', 'L': 'Purworejo', 'Q': 'Purworejo', 'V': 'Purworejo',
                'D': 'Kebumen', 'J': 'Kebumen', 'M': 'Kebumen', 'W': 'Kebumen',
                'E': 'Temanggung', 'N': 'Temanggung', 'Y': 'Temanggung', 'F': 'Wonosobo',
                'P': 'Wonosobo', 'Z': 'Wonosobo'
            }
        },
        'AD': {
            'region_name': 'Jawa Tengah (Keresidenan Surakarta)',
            'province_code': '33',
            'area': 'Jawa Bagian Tengah',
            'sub_codes': {
                'A': 'Kota Surakarta', 'H': 'Kota Surakarta', 'S': 'Kota Surakarta',
                'U': 'Kota Surakarta', 'B': 'Sukoharjo', 'K': 'Sukoharjo', 'O': 'Sukoharjo',
                'T': 'Sukoharjo', 'C': 'Klaten', 'J': 'Klaten', 'L': 'Klaten',
                'Q': 'Klaten', 'V': 'Klaten', 'D': 'Boyolali', 'M': 'Boyolali',
                'W': 'Boyolali', 'E': 'Sragen', 'N': 'Sragen', 'Y': 'Sragen',
                'F': 'Karanganyar', 'P': 'Karanganyar', 'Z': 'Karanganyar', 'G': 'Wonogiri',
                'I': 'Wonogiri', 'R': 'Wonogiri'
            }
        },
        'AB': {
            'region_name': 'Daerah Istimewa Yogyakarta',
            'province_code': '34',
            'area': 'Jawa Tengah',
            'sub_codes': {
                'A': 'Kota Yogyakarta', 'F': 'Kota Yogyakarta', 'H': 'Kota Yogyakarta',
                'I': 'Kota Yogyakarta', 'S': 'Kota Yogyakarta', 'B': 'Bantul',
                'G': 'Bantul', 'J': 'Bantul', 'K': 'Bantul', 'T': 'Bantul',
                'C': 'Kulon Progo', 'L': 'Kulon Progo', 'O': 'Kulon Progo',
                'P': 'Kulon Progo', 'V': 'Kulon Progo', 'D': 'Gunungkidul',
                'M': 'Gunungkidul', 'R': 'Gunungkidul', 'W': 'Gunungkidul',
                'E': 'Sleman', 'N': 'Sleman', 'Q': 'Sleman', 'U': 'Sleman',
                'X': 'Sleman', 'Y': 'Sleman', 'Z': 'Sleman'
            }
        },
        
        # JAWA TIMUR DAN KEPULAUAN NUSA TENGGARA (East Java & NTT Region)
        'L': {
            'region_name': 'Jawa Timur (Kota Surabaya)',
            'province_code': '35',
            'area': 'Jawa Timur',
            'sub_codes': {
                c: 'Kota Surabaya' for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            }
        },
        'M': {
            'region_name': 'Jawa Timur (Madura)',
            'province_code': '35',
            'area': 'Jawa Timur',
            'sub_codes': {
                'A': 'Pamekasan', 'B': 'Pamekasan', 'C': 'Pamekasan', 'D': 'Pamekasan',
                'E': 'Pamekasan', 'F': 'Pamekasan', 'G': 'Bangkalan', 'H': 'Bangkalan',
                'I': 'Bangkalan', 'J': 'Bangkalan', 'K': 'Bangkalan', 'L': 'Bangkalan',
                'M': 'Bangkalan', 'N': 'Sampang', 'O': 'Sampang', 'P': 'Sampang',
                'Q': 'Sampang', 'R': 'Sampang', 'S': 'Sampang', 'T': 'Sumenep',
                'U': 'Sumenep', 'V': 'Sumenep', 'W': 'Sumenep', 'X': 'Sumenep',
                'Y': 'Sumenep', 'Z': 'Sumenep'
            }
        },
        'N': {
            'region_name': 'Jawa Timur (Pasuruan-Malang)',
            'province_code': '35',
            'area': 'Jawa Timur',
            'sub_codes': {
                'A': 'Kota Malang', 'B': 'Kota Malang', 'C': 'Kota Malang',
                'D': 'Kota Malang', 'E': 'Kabupaten Malang', 'F': 'Kabupaten Malang',
                'G': 'Kabupaten Malang', 'H': 'Kabupaten Malang', 'I': 'Kabupaten Malang',
                'J': 'Kota Batu', 'K': 'Kota Batu', 'L': 'Kota Batu',
                'M': 'Kabupaten Probolinggo', 'N': 'Kabupaten Probolinggo', 'O': 'Kabupaten Probolinggo',
                'P': 'Kota Probolinggo', 'Q': 'Kota Probolinggo', 'R': 'Kota Probolinggo',
                'T': 'Kabupaten Pasuruan', 'U': 'Lumajang', 'Y': 'Lumajang', 'Z': 'Lumajang',
                'V': 'Kota Pasuruan', 'W': 'Kota Pasuruan', 'X': 'Kota Pasuruan'
            }
        },
        'P': {
            'region_name': 'Jawa Timur (Besuki)',
            'province_code': '35',
            'area': 'Jawa Timur',
            'sub_codes': {
                'A': 'Bondowoso', 'B': 'Bondowoso', 'C': 'Bondowoso', 'D': 'Situbondo',
                'E': 'Situbondo', 'F': 'Situbondo', 'G': 'Jember', 'H': 'Jember',
                'I': 'Jember', 'J': 'Jember', 'K': 'Jember', 'L': 'Jember',
                'M': 'Jember', 'N': 'Jember', 'O': 'Jember', 'P': 'Jember',
                'Q': 'Banyuwangi', 'R': 'Banyuwangi', 'S': 'Banyuwangi',
                'T': 'Banyuwangi', 'U': 'Banyuwangi', 'V': 'Banyuwangi',
                'W': 'Banyuwangi', 'X': 'Banyuwangi', 'Y': 'Banyuwangi', 'Z': 'Banyuwangi'
            }
        },
        'S': {
            'region_name': 'Jawa Timur (Bojonegoro, Mojokerto, Lamongan, Jombang)',
            'province_code': '35',
            'area': 'Jawa Timur',
            'sub_codes': {
                'A': 'Bojonegoro', 'B': 'Bojonegoro', 'C': 'Bojonegoro', 'D': 'Bojonegoro',
                'E': 'Tuban', 'F': 'Tuban', 'G': 'Tuban', 'H': 'Tuban', 'I': 'Tuban',
                'J': 'Lamongan', 'K': 'Lamongan', 'L': 'Lamongan', 'M': 'Lamongan',
                'N': 'Kabupaten Mojokerto', 'P': 'Kabupaten Mojokerto', 'Q': 'Kabupaten Mojokerto',
                'R': 'Kabupaten Mojokerto', 'O': 'Jombang', 'W': 'Jombang', 'X': 'Jombang',
                'Y': 'Jombang', 'Z': 'Jombang', 'S': 'Kota Mojokerto', 'T': 'Kota Mojokerto',
                'U': 'Kota Mojokerto', 'V': 'Kota Mojokerto'
            }
        },
        'W': {
            'region_name': 'Jawa Timur (Surabaya)',
            'province_code': '35',
            'area': 'Jawa Timur',
            'sub_codes': {
                'A': 'Gresik', 'B': 'Gresik', 'C': 'Gresik', 'D': 'Gresik',
                'E': 'Gresik', 'F': 'Gresik', 'G': 'Gresik', 'H': 'Gresik',
                'I': 'Gresik', 'J': 'Gresik', 'K': 'Gresik', 'L': 'Gresik',
                'M': 'Gresik', 'N': 'Sidoarjo', 'O': 'Sidoarjo', 'P': 'Sidoarjo',
                'Q': 'Sidoarjo', 'R': 'Sidoarjo', 'S': 'Sidoarjo', 'T': 'Sidoarjo',
                'U': 'Sidoarjo', 'V': 'Sidoarjo', 'W': 'Sidoarjo', 'X': 'Sidoarjo',
                'Y': 'Sidoarjo', 'Z': 'Sidoarjo'
            }
        },
        'AE': {
            'region_name': 'Jawa Timur (Madiun)',
            'province_code': '35',
            'area': 'Jawa Timur',
            'sub_codes': {
                'A': 'Kota Madiun', 'B': 'Kota Madiun', 'C': 'Kota Madiun', 'D': 'Kota Madiun',
                'E': 'Kabupaten Madiun', 'F': 'Kabupaten Madiun', 'G': 'Kabupaten Madiun',
                'H': 'Kabupaten Madiun', 'I': 'Kabupaten Madiun', 'J': 'Ngawi',
                'K': 'Ngawi', 'L': 'Ngawi', 'M': 'Ngawi', 'N': 'Magetan',
                'O': 'Magetan', 'P': 'Magetan', 'Q': 'Magetan', 'R': 'Magetan',
                'S': 'Ponorogo', 'T': 'Ponorogo', 'U': 'Ponorogo', 'V': 'Ponorogo',
                'W': 'Ponorogo', 'X': 'Pacitan', 'Y': 'Pacitan', 'Z': 'Pacitan'
            }
        },
        'AG': {
            'region_name': 'Jawa Timur (Kediri)',
            'province_code': '35',
            'area': 'Jawa Timur',
            'sub_codes': {
                'A': 'Kota Kediri', 'B': 'Kota Kediri', 'C': 'Kota Kediri', 'D': 'Kota Kediri',
                'E': 'Kabupaten Kediri', 'F': 'Kabupaten Kediri', 'G': 'Kabupaten Kediri',
                'H': 'Kabupaten Kediri', 'J': 'Kabupaten Kediri', 'O': 'Kabupaten Kediri',
                'I': 'Kabupaten Blitar', 'K': 'Kabupaten Blitar', 'L': 'Kabupaten Blitar',
                'M': 'Kabupaten Blitar', 'P': 'Kabupaten Blitar', 'N': 'Kota Blitar',
                'Q': 'Kota Blitar', 'R': 'Tulungagung', 'S': 'Tulungagung', 'T': 'Tulungagung',
                'U': 'Nganjuk', 'V': 'Nganjuk', 'W': 'Nganjuk', 'X': 'Nganjuk',
                'Y': 'Trenggalek', 'Z': 'Trenggalek'
            }
        },
        'DK': {
            'region_name': 'Bali',
            'province_code': '51',
            'area': 'Bali',
            'sub_codes': {
                'A': 'Kota Denpasar', 'B': 'Kota Denpasar', 'C': 'Kota Denpasar',
                'D': 'Kota Denpasar', 'E': 'Kota Denpasar', 'I': 'Kota Denpasar',
                'X': 'Kota Denpasar', 'F': 'Badung', 'J': 'Badung', 'O': 'Badung',
                'Q': 'Badung', 'G': 'Tabanan', 'H': 'Tabanan', 'K': 'Gianyar',
                'L': 'Gianyar', 'M': 'Klungkung', 'N': 'Klungkung', 'P': 'Bangli',
                'R': 'Bangli', 'S': 'Karangasem', 'T': 'Karangasem', 'U': 'Buleleng',
                'V': 'Buleleng', 'W': 'Jembrana', 'Z': 'Jembrana'
            }
        },
        'DR': {
            'region_name': 'NTB (Lombok)',
            'province_code': '52',
            'area': 'Nusa Tenggara Barat',
            'sub_codes': {
                'A': 'Kota Mataram', 'B': 'Kota Mataram', 'C': 'Kota Mataram',
                'D': 'Kota Mataram', 'E': 'Kota Mataram', 'F': 'Kota Mataram',
                'N': 'Kota Mataram', 'O': 'Kota Mataram', 'P': 'Kota Mataram',
                'R': 'Kota Mataram', 'X': 'Kota Mataram', 'G': 'Lombok Utara',
                'M': 'Lombok Utara', 'H': 'Lombok Barat', 'J': 'Lombok Barat',
                'K': 'Lombok Barat', 'T': 'Lombok Barat', 'W': 'Lombok Barat',
                'L': 'Lombok Timur', 'Q': 'Lombok Timur', 'Y': 'Lombok Timur',
                'S': 'Lombok Tengah', 'U': 'Lombok Tengah', 'V': 'Lombok Tengah',
                'Z': 'Lombok Tengah'
            }
        },
        'EA': {
            'region_name': 'NTB (Sumbawa)',
            'province_code': '52',
            'area': 'Nusa Tenggara Barat',
            'sub_codes': {
                'A': 'Sumbawa', 'C': 'Sumbawa', 'D': 'Sumbawa', 'E': 'Sumbawa',
                'F': 'Sumbawa', 'P': 'Sumbawa', 'H': 'Sumbawa Barat', 'K': 'Sumbawa Barat',
                'L': 'Kota Bima', 'S': 'Kota Bima', 'M': 'Dompu', 'N': 'Dompu',
                'Q': 'Dompu', 'R': 'Dompu', 'T': 'Dompu', 'W': 'Bima',
                'X': 'Bima', 'Y': 'Bima', 'Z': 'Bima'
            }
        },
        'DH': {
            'region_name': 'NTT (Timor)',
            'province_code': '53',
            'area': 'Nusa Tenggara Timur',
            'sub_codes': {
                'A': 'Kota Kupang', 'H': 'Kota Kupang', 'K': 'Kota Kupang',
                'B': 'Kupang', 'N': 'Kupang', 'C': 'Timor Tengah Selatan',
                'D': 'Timor Tengah Utara', 'M': 'Timor Tengah Utara', 'E': 'Belu',
                'T': 'Belu', 'F': 'Sabu Raijua', 'G': 'Rote Ndao', 'J': 'Malaka'
            }
        },
        'EB': {
            'region_name': 'NTT (Flores)',
            'province_code': '53',
            'area': 'Nusa Tenggara Timur',
            'sub_codes': {
                'A': 'Ende', 'B': 'Sikka', 'C': 'Flores Timur', 'D': 'Ngada',
                'E': 'Manggarai', 'F': 'Lembata', 'G': 'Manggarai Barat', 'H': 'Nagekeo',
                'J': 'Alor', 'K': 'Alor', 'P': 'Manggarai Timur'
            }
        },
        'ED': {
            'region_name': 'NTT (Sumba)',
            'province_code': '53',
            'area': 'Nusa Tenggara Timur',
            'sub_codes': {
                'A': 'Sumba Timur', 'B': 'Sumba Barat', 'C': 'Sumba Barat Daya',
                'D': 'Sumba Tengah'
            }
        },
        
        # KALIMANTAN (Borneo Region)
        'KB': {
            'region_name': 'Kalimantan Barat',
            'province_code': '61',
            'area': 'Kalimantan',
            'sub_codes': {
                'A': 'Kota Pontianak', 'H': 'Kota Pontianak', 'O': 'Kota Pontianak',
                'Q': 'Kota Pontianak', 'W': 'Kota Pontianak',
                'B': 'Kabupaten Pontianak', 'C': 'Kota Singkawang', 'Y': 'Kota Singkawang',
                'D': 'Kabupaten Sanggau', 'U': 'Kabupaten Sanggau', 'E': 'Kabupaten Sintang', 'F': 'Kabupaten Kapuas Hulu',
                'G': 'Kabupaten Ketapang', 'J': 'Kabupaten Melawi', 'K': 'Kabupaten Bengkayang', 'L': 'Kabupaten Landak',
                'M': 'Kabupaten Kubu Raya', 'N': 'Kabupaten Kubu Raya', 'P': 'Kabupaten Sambas', 'T': 'Kabupaten Sambas',
                'V': 'Kabupaten Sekadau', 'Z': 'Kabupaten Kayong Utara', 'S': 'Kabupaten Sintang'
            }
        },
        'KH': {
            'region_name': 'Kalimantan Tengah',
            'province_code': '62',
            'area': 'Kalimantan',
            'sub_codes': {
                'A': 'Kota Palangkaraya', 'Q': 'Kota Palangkaraya', 'T': 'Kota Palangkaraya',
                'Y': 'Kota Palangkaraya', 'B': 'Kapuas', 'C': 'Kapuas', 'U': 'Kapuas',
                'D': 'Barito Selatan', 'E': 'Barito Utara', 'F': 'Kotawaringin Timur',
                'L': 'Kotawaringin Timur', 'W': 'Kotawaringin Timur', 'G': 'Kotawaringin Barat',
                'V': 'Kotawaringin Barat', 'H': 'Gunung Mas', 'J': 'Pulang Pisau',
                'K': 'Barito Timur', 'M': 'Murung Raya', 'N': 'Katingan', 'P': 'Seruyan',
                'R': 'Lamandau', 'S': 'Sukamara'
            }
        },
        'DA': {
            'region_name': 'Kalimantan Selatan',
            'province_code': '63',
            'area': 'Kalimantan',
            'sub_codes': {
                'A': 'Kota Banjarmasin', 'C': 'Kota Banjarmasin', 'I': 'Kota Banjarmasin',
                'J': 'Kota Banjarmasin', 'N': 'Kota Banjarmasin', 'S': 'Kota Banjarmasin',
                'V': 'Kota Banjarmasin', 'X': 'Kota Banjarmasin', 'B': 'Banjar',
                'O': 'Banjar', 'Q': 'Banjar', 'D': 'Hulu Sungai Selatan', 'E': 'Hulu Sungai Tengah',
                'F': 'Hulu Sungai Utara', 'G': 'Kota Baru', 'H': 'Tabalong',
                'U': 'Tabalong', 'K': 'Tapin', 'L': 'Tanah Laut', 'M': 'Barito Kuala',
                'P': 'Kota Banjarbaru', 'R': 'Kota Banjarbaru', 'W': 'Kota Banjarbaru',
                'Y': 'Balangan', 'Z': 'Tanah Bumbu'
            }
        },
        'KT': {
            'region_name': 'Kalimantan Timur',
            'province_code': '64',
            'area': 'Kalimantan',
            'sub_codes': {
                'A': 'Kota Balikpapan', 'H': 'Kota Balikpapan', 'K': 'Kota Balikpapan',
                'L': 'Kota Balikpapan', 'Y': 'Kota Balikpapan', 'Z': 'Kota Balikpapan',
                'B': 'Kota Samarinda', 'F': 'Kota Samarinda', 'I': 'Kota Samarinda',
                'M': 'Kota Samarinda', 'N': 'Kota Samarinda', 'S': 'Kota Samarinda',
                'W': 'Kota Samarinda', 'C': 'Kutai Kartanegara', 'J': 'Kutai Kartanegara',
                'O': 'Kutai Kartanegara', 'U': 'Kutai Kartanegara', 'D': 'Kota Bontang',
                'Q': 'Kota Bontang', 'E': 'Paser', 'S': 'Paser', 'G': 'Berau',
                'R': 'Kutai Timur', 'P': 'Kutai Barat', 'T': 'Mahakam Ulu',
                'V': 'Penajam Paser Utara'
            }
        },
        'KU': {
            'region_name': 'Kalimantan Utara',
            'province_code': '65',
            'area': 'Kalimantan',
            'sub_codes': {
                'A': 'Bulungan', 'B': 'Bulungan', 'G': 'Kota Tarakan', 'H': 'Tana Tidung',
                'J': 'Pulau Morotai', 'N': 'Nunukan', 'S': 'Malinau'
            }
        },
        
        # SULAWESI (Celebes Region)
        'DB': {
            'region_name': 'Sulawesi Utara (Daratan)',
            'province_code': '71',
            'area': 'Sulawesi',
            'sub_codes': {
                'A': 'Kota Manado', 'L': 'Kota Manado', 'M': 'Kota Manado',
                'R': 'Kota Manado', 'T': 'Kota Manado', 'V': 'Kota Manado',
                'B': 'Minahasa', 'Q': 'Minahasa', 'C': 'Kota Bitung', 'O': 'Kota Bitung',
                'D': 'Bolaang Mongondow', 'E': 'Minahasa Selatan', 'F': 'Minahasa Utara',
                'W': 'Minahasa Utara', 'G': 'Kota Tomohon', 'H': 'Bolaang Mongondow Utara',
                'J': 'Minahasa Tenggara', 'K': 'Kota Kotamobagu', 'N': 'Bolaang Mongondow Timur',
                'P': 'Bolaang Mongondow Selatan'
            }
        },
        'DL': {
            'region_name': 'Sulawesi Utara (Kepulauan)',
            'province_code': '71',
            'area': 'Sulawesi',
            'sub_codes': {
                'A': 'Kepulauan Sangihe', 'B': 'Kepulauan Talaud', 'C': 'Kepulauan Sitaro'
            }
        },
        'DN': {
            'region_name': 'Sulawesi Tengah',
            'province_code': '72',
            'area': 'Sulawesi',
            'sub_codes': {
                'A': 'Kota Palu', 'I': 'Kota Palu', 'N': 'Kota Palu', 'V': 'Kota Palu',
                'Y': 'Kota Palu', 'B': 'Donggala', 'J': 'Donggala', 'C': 'Banggai',
                'R': 'Banggai', 'D': 'Toli-Toli', 'E': 'Poso', 'F': 'Buol',
                'G': 'Morowali', 'H': 'Banggai Kepulauan', 'K': 'Parigi Moutong',
                'P': 'Parigi Moutong', 'L': 'Tojo Una-Una', 'M': 'Sigi',
                'Q': 'Banggai Laut', 'U': 'Morowali Utara'
            }
        },
        'DD': {
            'region_name': 'Sulawesi Selatan (Makassar)',
            'province_code': '73',
            'area': 'Sulawesi',
            'sub_codes': {
                'A': 'Kota Makassar', 'I': 'Kota Makassar', 'K': 'Kota Makassar',
                'M': 'Kota Makassar', 'O': 'Kota Makassar', 'Q': 'Kota Makassar',
                'R': 'Kota Makassar', 'S': 'Kota Makassar', 'U': 'Kota Makassar',
                'V': 'Kota Makassar', 'X': 'Kota Makassar', 'B': 'Gowa',
                'L': 'Gowa', 'N': 'Gowa', 'Y': 'Gowa', 'C': 'Takalar', 'P': 'Takalar',
                'D': 'Maros', 'T': 'Maros', 'E': 'Pangkajene dan Kepulauan',
                'W': 'Pangkajene dan Kepulauan', 'F': 'Bantaeng', 'G': 'Jeneponto',
                'H': 'Bulukumba', 'Z': 'Bulukumba', 'J': 'Selayar'
            }
        },
        'DW': {
            'region_name': 'Sulawesi Selatan (Bone, Wajo)',
            'province_code': '73',
            'area': 'Sulawesi',
            'sub_codes': {
                'A': 'Bone', 'E': 'Bone', 'F': 'Bone', 'G': 'Bone', 'H': 'Bone',
                'B': 'Wajo', 'L': 'Wajo', 'M': 'Wajo', 'N': 'Wajo', 'O': 'Wajo',
                'P': 'Wajo', 'C': 'Soppeng', 'Q': 'Soppeng', 'Y': 'Soppeng',
                'D': 'Sinjai', 'V': 'Sinjai', 'Z': 'Sinjai'
            }
        },
        'DP': {
            'region_name': 'Sulawesi Selatan (Utara)',
            'province_code': '73',
            'area': 'Sulawesi',
            'sub_codes': {
                'A': 'Kota Parepare', 'L': 'Kota Parepare', 'M': 'Kota Parepare',
                'B': 'Barru', 'O': 'Barru', 'C': 'Sidenreng Rappang', 'P': 'Sidenreng Rappang',
                'Q': 'Sidenreng Rappang', 'D': 'Pinrang', 'R': 'Pinrang', 'S': 'Pinrang',
                'E': 'Kota Palopo', 'T': 'Kota Palopo', 'F': 'Luwu', 'U': 'Luwu',
                'G': 'Luwu Timur', 'V': 'Luwu Timur', 'H': 'Luwu Utara', 'W': 'Luwu Utara',
                'J': 'Tana Toraja', 'Y': 'Tana Toraja', 'K': 'Toraja Utara', 'Z': 'Toraja Utara',
                'N': 'Enrekang', 'X': 'Enrekang'
            }
        },
        'DT': {
            'region_name': 'Sulawesi Tenggara',
            'province_code': '74',
            'area': 'Sulawesi',
            'sub_codes': {
                'A': 'Konawe', 'B': 'Kolaka', 'C': 'Buton', 'D': 'Muna',
                'E': 'Kota Kendari', 'F': 'Kota Kendari', 'I': 'Kota Kendari',
                'G': 'Kota Baubau', 'H': 'Konawe Selatan', 'J': 'Kolaka Utara',
                'K': 'Bombana', 'L': 'Wakatobi', 'M': 'Konawe Utara', 'N': 'Buton Utara',
                'O': 'Konawe Kepulauan', 'R': 'Muna Barat', 'T': 'Kolaka Timur',
                'W': 'Buton Selatan', 'Y': 'Buton Tengah'
            }
        },
        'DM': {
            'region_name': 'Gorontalo',
            'province_code': '75',
            'area': 'Sulawesi',
            'sub_codes': {
                'A': 'Kota Gorontalo', 'J': 'Kota Gorontalo', 'X': 'Kota Gorontalo',
                'B': 'Gorontalo', 'H': 'Gorontalo', 'C': 'Boalemo', 'D': 'Pohuwato',
                'E': 'Bone Bolango', 'F': 'Gorontalo Utara'
            }
        },
        'DC': {
            'region_name': 'Sulawesi Barat',
            'province_code': '76',
            'area': 'Sulawesi',
            'sub_codes': {
                'A': 'Mamuju', 'G': 'Mamuju', 'L': 'Mamuju', 'P': 'Mamuju',
                'B': 'Majene', 'Q': 'Majene', 'C': 'Polewali Mandar', 'N': 'Polewali Mandar',
                'D': 'Mamasa', 'E': 'Pasangkayu', 'X': 'Pasangkayu', 'F': 'Mamuju Tengah'
            }
        },
        
        # MALUKU DAN PAPUA (Maluku and Papua Region)
        'DE': {
            'region_name': 'Maluku',
            'province_code': '81',
            'area': 'Maluku dan Papua',
            'sub_codes': {
                'A': 'Kota Ambon', 'L': 'Kota Ambon', 'N': 'Kota Ambon',
                'B': 'Maluku Tengah', 'C': 'Maluku Tenggara', 'D': 'Buru',
                'E': 'Kepulauan Tanimbar', 'F': 'Kepulauan Aru', 'G': 'Seram Bagian Barat',
                'O': 'Seram Bagian Barat', 'H': 'Seram Bagian Timur', 'I': 'Kota Tual',
                'J': 'Maluku Barat Daya', 'K': 'Buru Selatan'
            }
        },
        'DG': {
            'region_name': 'Maluku Utara',
            'province_code': '82',
            'area': 'Maluku dan Papua',
            'sub_codes': {
                'A': 'Kota Ternate', 'K': 'Kota Ternate', 'Q': 'Kota Ternate',
                'B': 'Kota Tidore Kepulauan', 'L': 'Kota Tidore Kepulauan', 'H': 'Pulau Taliabu',
                'J': 'Pulau Morotai', 'M': 'Halmahera Barat', 'N': 'Halmahera Utara',
                'P': 'Halmahera Selatan', 'R': 'Kepulauan Sula', 'S': 'Halmahera Tengah',
                'T': 'Halmahera Timur'
            }
        },
        'PA': {
            'region_name': 'Papua',
            'province_code': '94',
            'area': 'Maluku dan Papua',
            'sub_codes': {
                'A': 'Kota Jayapura', 'F': 'Kota Jayapura', 'R': 'Kota Jayapura',
                'C': 'Biak Numfor', 'J': 'Jayapura', 'L': 'Kepulauan Yapen',
                'N': 'Waropen', 'Q': 'Keerom', 'S': 'Sarmi', 'U': 'Supiori',
                'X': 'Mamberamo Raya'
            }
        },
        'PB': {
            'region_name': 'Papua Barat',
            'province_code': '91',
            'area': 'Maluku dan Papua',
            'sub_codes': {
                'B': 'Teluk Bintuni', 'D': 'Pegunungan Arfak', 'F': 'Fakfak',
                'G': 'Manokwari', 'H': 'Manokwari', 'M': 'Manokwari', 'K': 'Kaimana',
                'L': 'Manokwari Selatan', 'W': 'Teluk Wondama'
            }
        },
        'PG': {
            'region_name': 'Papua Pegunungan',
            'province_code': '92',
            'area': 'Maluku dan Papua',
            'sub_codes': {
                'A': 'Jayawijaya', 'F': 'Pegunungan Bintang', 'J': 'Yahukimo', 'X': 'Nduga'
            }
        },
        'PS': {
            'region_name': 'Papua Selatan',
            'province_code': '93',
            'area': 'Maluku dan Papua',
            'sub_codes': {
                'A': 'Merauke', 'V': 'Boven Digoel'
            }
        },
        'PT': {
            'region_name': 'Papua Tengah',
            'province_code': '94',
            'area': 'Maluku dan Papua',
            'sub_codes': {
                'A': 'Nabire', 'E': 'Dogiyai', 'H': 'Deiyai', 'L': 'Mimika',
                'M': 'Mimika', 'N': 'Mimika', 'P': 'Paniai', 'S': 'Puncak Jaya',
                'V': 'Intan Jaya', 'Y': 'Puncak'
            }
        },
        'CC': {
            'region_name': 'Diplomatik',
            'province_code': '31',
            'area': 'Diplomatik',
            'sub_codes': {
                'A': 'Diplomatik', 'B': 'Diplomatik'
            }
        },
        'PY': {
            'region_name': 'Papua Barat Daya',
            'province_code': '91',
            'area': 'Maluku dan Papua',
            'sub_codes': {
                'A': 'Kota Sorong', 'E': 'Sorong', 'K': 'Raja Ampat',
                'Q': 'Tambrauw', 'T': 'Sorong Selatan', 'V': 'Maybrat'
            }
        }
    }
    
    # Mapping of plate codes to Indonesian province codes for KTP synchronization
    # This ensures that generated vehicles have matching plate and KTP province codes
    # Generated from PLATE_DATA to ensure consistency
    PLATE_CODE_TO_PROVINCE = {
        'A': '36',    # Banten
        'AA': '33',   # Jawa Tengah (Keresidenan Kedu)
        'AB': '34',   # Daerah Istimewa Yogyakarta
        'AD': '33',   # Jawa Tengah (Keresidenan Surakarta)
        'AE': '35',   # Jawa Timur (Madiun)
        'AG': '35',   # Jawa Timur (Kediri)
        'B': '31',    # DKI Jakarta, Jawa Barat, Banten (Polda Metro Jaya)
        'BA': '13',   # Sumatera Barat
        'BB': '12',   # Sumatera Utara Barat (Tapanuli)
        'BD': '17',   # Bengkulu
        'BE': '18',   # Lampung
        'BG': '16',   # Sumatera Selatan
        'BH': '15',   # Jambi
        'BK': '12',   # Sumatera Utara Timur (Pesisir Timur Sumatra)
        'BL': '11',   # Aceh
        'BM': '14',   # Riau
        'BN': '19',   # Kepulauan Bangka Belitung
        'BP': '21',   # Kepulauan Riau
        'D': '32',    # Jawa Barat (Priangan Tengah)
        'DA': '63',   # Kalimantan Selatan
        'DB': '71',   # Sulawesi Utara (Daratan)
        'DC': '76',   # Sulawesi Barat
        'DD': '73',   # Sulawesi Selatan (Makassar)
        'DE': '81',   # Maluku
        'DG': '82',   # Maluku Utara
        'DH': '53',   # NTT (Timor)
        'DK': '51',   # Bali
        'DL': '71',   # Sulawesi Utara (Kepulauan)
        'DM': '75',   # Gorontalo
        'DN': '72',   # Sulawesi Tengah
        'DP': '73',   # Sulawesi Selatan (Utara)
        'DR': '52',   # NTB (Lombok)
        'DT': '74',   # Sulawesi Tenggara
        'DW': '73',   # Sulawesi Selatan (Bone, Wajo)
        'E': '32',    # Jawa Barat (Keresidenan Cirebon)
        'EA': '52',   # NTB (Sumbawa)
        'EB': '53',   # NTT (Flores)
        'ED': '53',   # NTT (Sumba)
        'F': '32',    # Jawa Barat (Keresidenan Bogor dan Priangan Barat)
        'G': '33',    # Jawa Tengah (Keresidenan Pekalongan)
        'H': '33',    # Jawa Tengah (Keresidenan Semarang)
        'K': '33',    # Jawa Tengah (Keresidenan Pati dan Grobogan)
        'KB': '61',   # Kalimantan Barat
        'KH': '62',   # Kalimantan Tengah
        'KT': '64',   # Kalimantan Timur
        'KU': '65',   # Kalimantan Utara
        'L': '35',    # Jawa Timur (Kota Surabaya)
        'M': '35',    # Jawa Timur (Madura)
        'N': '35',    # Jawa Timur (Pasuruan-Malang)
        'P': '35',    # Jawa Timur (Besuki)
        'PA': '94',   # Papua
        'PB': '91',   # Papua Barat
        'PG': '92',   # Papua Pegunungan
        'PS': '93',   # Papua Selatan
        'PT': '94',   # Papua Tengah
        'PY': '91',   # Papua Barat Daya
        'R': '33',    # Jawa Tengah (Keresidenan Banyumas)
        'S': '35',    # Jawa Timur (Bojonegoro, Mojokerto, Lamongan, Jombang)
        'T': '32',    # Jawa Barat (Keresidenan Karawang)
        'W': '35',    # Jawa Timur (Surabaya)
        'Z': '32',    # Jawa Barat (Priangan Timur dan Kabupaten Sumedang)
        'CC': '31',   # Diplomatik (special vehicle)
        'CD': '31',   # Diplomatik (special vehicle)
        'RI': '31',   # Pemerintah Indonesia (special vehicle)
    }
    
    @classmethod
    def get_province_code_from_plate_code(cls, plate_code: str) -> Optional[str]:
        """
        Get province code from plate code for KTP synchronization
        
        Indonesian regulation: Vehicle plate must match owner's KTP province code
        Example: Plate 'B' (Jakarta) → province_code '31'
        
        Args:
            plate_code: License plate code (e.g., 'B', 'D', 'AB')
        
        Returns:
            Province code as string (e.g., '31') or None if not found
        """
        # Use PLATE_DATA as the authoritative source (most accurate)
        if plate_code in cls.PLATE_DATA:
            return cls.PLATE_DATA[plate_code].get('province_code')
        
        return None
    
    @classmethod
    def generate_plate(
        cls,
        vehicle_type: VehicleType = VehicleType.RODA_DUA
    ) -> Tuple[str, str, str, str]:
        """
        Generate Indonesian license plate following official nomenclature.
        
        Format: [RegionCode] [1-4 digit number] [SubCode] [Owner letters]
        Examples:
        - Motor: B 1 U AB, B 12 U AB, B 123 U AB, B 1234 U AB
        - Mobil: B 5 P ABC, B 56 P ABC, B 567 P ABC, B 5678 P ABC
        
        Args:
            vehicle_type: VehicleType enum value
            
        Returns:
            (plate_string, region_name, sub_region, vehicle_type_display)
        """
        region_code = random.choice(list(cls.PLATE_DATA.keys()))
        region_data = cls.PLATE_DATA[region_code]
        sub_code = random.choice(list(region_data['sub_codes'].keys()))
        sub_region = region_data['sub_codes'][sub_code]
        
        # Randomly choose 1, 2, 3, or 4 digit number
        num_digits = random.choice([1, 2, 3, 4])
        max_number = (10 ** num_digits) - 1
        number = f"{random.randint(0, max_number):0{num_digits}d}"
        
        if vehicle_type == VehicleType.RODA_DUA:
            owner_code = ''.join(random.choices(cls.OWNER_CODE_LETTERS, k=random.randint(1, 2)))
        else:
            owner_code = ''.join(random.choices(cls.OWNER_CODE_LETTERS, k=random.randint(2, 3)))
        
        plate = f"{region_code} {number} {sub_code} {owner_code}"
        return plate, region_data['region_name'], sub_region, vehicle_type.value
    
    @classmethod
    def parse_plate(cls, plate: str) -> Optional[Dict]:
        """Parse Indonesian license plate (handles multiple formats)
        
        Formats supported:
        - New Private: [RegionCode] [1-4 digits] [1-3 letters]
        - New Commercial: [RegionCode] [1-4 digits] [1-3 letters] (NIAGA)
        - New Truck: [RegionCode] [1-4 digits] [T/K/G/D][1-3 letters] (TRUK-XXX) - RUTE: XX
        - New Government: RI [Agency] [1-4 digits]
        - New Diplomatic: CD/CC [CountryCode] [1-4 digits]
        - Old format: [RegionCode] [4-digit] [SubCode] [Owner letters]
        """
        try:
            # Remove extra information in parentheses for parsing
            base_plate = plate.split('(')[0].strip()
            parts = base_plate.split()
            
            if len(parts) < 2:
                return None
            
            region_code = parts[0]
            
            # Handle government plates (RI prefix)
            if region_code == 'RI':
                return {
                    'plate': plate,
                    'region_code': 'RI',
                    'region_name': 'Pemerintah Indonesia',
                    'sub_region': 'Pemerintah Indonesia',
                    'is_valid': True,
                    'format': 'government'
                }
            
            # Handle diplomatic plates (CD/CC prefix)
            if region_code in ('CD', 'CC'):
                return {
                    'plate': plate,
                    'region_code': region_code,
                    'region_name': 'Diplomatik',
                    'sub_region': 'Diplomatik',
                    'is_valid': True,
                    'format': 'diplomatic'
                }
            
            # Check if region code exists in PLATE_DATA
            if region_code not in cls.PLATE_DATA:
                return None
            
            region_data = cls.PLATE_DATA[region_code]
            region_name = region_data['region_name']
            
            # Handle new formats with 3 parts: [RegionCode] [1-4 digits] [1-3 letters]
            if len(parts) == 3:
                number = parts[1]
                letters = parts[2]
                
                # Extract sub-region from first letter of letters (maps to sub_codes)
                first_letter = letters[0] if letters else None
                sub_region = region_name  # Default fallback
                
                # Try to get sub-region name from PLATE_DATA sub_codes using first letter
                if first_letter and 'sub_codes' in region_data and first_letter in region_data['sub_codes']:
                    sub_region = region_data['sub_codes'][first_letter]
                
                return {
                    'plate': plate,
                    'region_code': region_code,
                    'number': number,
                    'letters': letters,
                    'first_letter': first_letter,
                    'region_name': region_name,
                    'sub_region': sub_region,
                    'area': region_data.get('area', 'Unknown'),
                    'is_valid': True,
                    'format': 'new'
                }
            
            # Handle old format with 4+ parts: [RegionCode] [4-digit] [SubCode] [Owner letters]
            elif len(parts) >= 4:
                number = parts[1]
                sub_code = parts[2]
                owner_code = parts[3]
                
                # Check if sub_code exists
                if sub_code not in region_data['sub_codes']:
                    return None
                
                return {
                    'plate': plate,
                    'region_code': region_code,
                    'number': number,
                    'sub_code': sub_code,
                    'owner_code': owner_code,
                    'region_name': region_name,
                    'sub_region': region_data['sub_codes'][sub_code],
                    'area': region_data['area'],
                    'is_valid': True,
                    'format': 'old'
                }
            
            return None
        except Exception:
            return None
    
    @classmethod
    def generate_nik_from_plate(cls, plate_region_code: str, sub_region: str = None) -> str:
        """
        Generate NIK dari plate region dengan CSV administrative codes
        
        Format: Province(2) + City(2) + District(2) + BirthDay(2) + Month(2) + Year(2) + Sequential(4)
        Contoh: "B" + "Jakarta Selatan" -> 31.74.01 -> NIK = 3174DDMMYYSSSS
        """
        # Get province code from plate
        province_code = cls.get_province_code_from_plate_code(plate_region_code)
        if not province_code:
            province_code = f"{random.randint(11, 94):02d}"
        
        # Extract city and district from CSV if sub_region provided
        city_code = None
        district_code = None
        
        if sub_region:
            try:
                csv_codes = cls._get_csv_codes_for_region(sub_region)
                if csv_codes:
                    city_code = csv_codes['city']
                    district_code = csv_codes['district']
            except Exception:
                pass
        
        # If not found in CSV, try using PLATE_DATA sub_region mapping to get a real city name
        if not city_code and plate_region_code in cls.PLATE_DATA:
            try:
                plate_info = cls.PLATE_DATA[plate_region_code]
                # Get a random sub_region from the sub_codes
                if plate_info.get('sub_codes'):
                    random_sub_region_name = random.choice(list(plate_info['sub_codes'].values()))
                    # Now search CSV for this sub_region name
                    csv_codes = cls._get_csv_codes_for_region(random_sub_region_name)
                    if csv_codes:
                        city_code = csv_codes['city']
                        district_code = csv_codes['district']
            except Exception:
                pass
        
        # Fallback to random if still not found
        if not city_code:
            city_code = f"{random.randint(1, 99):02d}"
        if not district_code:
            district_code = f"{random.randint(1, 99):02d}"
        
        # Birth info with gender indicator
        day = random.randint(1, 28)
        is_female = random.random() < 0.5
        if is_female:
            day += 40
        month = random.randint(1, 12)
        year = random.randint(50, 99)
        
        # Sequential
        seq = random.randint(1, 9999)
        
        nik = f"{province_code}{city_code}{district_code}{day:02d}{month:02d}{year:02d}{seq:04d}"
        return nik
    
    @staticmethod
    def _get_csv_codes_for_region(sub_region: str) -> dict:
        """
        Extract city and district codes from base.csv for a given region
        
        Intelligently matches region names from PLATE_DATA sub_codes to CSV entries
        Handles:
        - "Jakarta Selatan" → "KOTA ADM. JAKARTA SELATAN" 
        - "Kota Bandung" → "KOTA BANDUNG"
        - "Kabupaten Tangerang" → "KAB. TANGERANG"
        - Regional descriptions with partial matches
        
        Returns: {'city': '74', 'district': '01', 'full': '31.74.01'} or None
        """
        try:
            base_csv_path = Path(__file__).parent.parent / 'base.csv'
            if not base_csv_path.exists():
                return None
            
            if not sub_region or not isinstance(sub_region, str):
                return None
            
            sub_region_upper = sub_region.upper().strip()
            
            # Read all lines once
            with open(base_csv_path, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
            
            # Build a list of clean region words (remove Kota/Kabupaten/KAB/KOTA/ADM prefixes)
            region_words = []
            temp = sub_region_upper
            for prefix in ['KOTA ', 'KAB. ', 'KABUPATEN ', 'ADM. ', 'KOTA ADM. ']:
                temp = temp.replace(prefix, '', 1)
            region_words = [w for w in temp.split() if w and len(w) > 2]
            
            # First pass: Try to find exact match in CSV (even with prefixes different)
            for line in all_lines:
                line = line.strip()
                if not line or ',' not in line:
                    continue
                
                parts = line.split(',', 1)
                code = parts[0].strip()
                name = parts[1].strip().upper()
                
                # Only look at city/kabupaten level entries (format: XX.YY)
                if code.count('.') != 1 or ('KOTA' not in name and 'KAB' not in name):
                    continue
                
                # Remove prefixes from CSV name too
                csv_name = name
                for prefix in ['KOTA ', 'KAB. ', 'KABUPATEN ', 'ADM. ', 'KOTA ADM. ']:
                    csv_name = csv_name.replace(prefix, '', 1)
                csv_name = csv_name.strip()
                
                # Check exact match of cleaned names
                if csv_name == temp:
                    code_parts = code.split('.')
                    if len(code_parts) == 2:
                        province = code_parts[0]
                        city = code_parts[1]
                        district = f"{random.randint(1, 30):02d}"
                        return {
                            'city': city,
                            'district': district,
                            'full': f"{province}.{city}.{district}"
                        }
                
                # Check if all significant words match
                if sub_region_upper in name or all(word in name for word in region_words):
                    code_parts = code.split('.')
                    if len(code_parts) == 2:
                        province = code_parts[0]
                        city = code_parts[1]
                        district = f"{random.randint(1, 30):02d}"
                        return {
                            'city': city,
                            'district': district,
                            'full': f"{province}.{city}.{district}"
                        }
            
            return None
        except Exception as e:
            return None
    
    @classmethod
    def validate_plate(cls, plate: str) -> Dict:
        """Validate plate and return information"""
        parsed = cls.parse_plate(plate)
        
        if not parsed:
            return {
                'valid': False,
                'error': 'Invalid plate format',
                'suggestion': 'Format: [RegionCode] [4digits] [SubCode] [Letters]'
            }
        
        return {
            'valid': True,
            'plate': parsed['plate'],
            'region_code': parsed['region_code'],
            'region_name': parsed['region_name'],
            'sub_region': parsed['sub_region'],
            'area': parsed['area'],
        }
    
    @classmethod
    def _load_regions_data(cls) -> Dict:
        """Load regions data - returns PLATE_DATA"""
        return cls.PLATE_DATA
    
    @classmethod
    def _get_all_region_codes_flat(cls) -> Dict[str, str]:
        """Get flattened region codes for backwards compatibility"""
        flat = {}
        for region_code, region_data in cls.PLATE_DATA.items():
            for sub_code, location in region_data['sub_codes'].items():
                full_code = f"{region_code}{sub_code}"
                flat[full_code] = location
            flat[region_code] = region_data['region_name']
        return flat
    
    @staticmethod
    def generate_plate_legacy() -> Tuple[str, str]:
        """Legacy method for backwards compatibility"""
        plate, region_name, sub_region, _ = IndonesianPlateManager.generate_plate()
        return plate, sub_region
    
    @staticmethod
    def parse_plate_legacy(plate: str) -> Optional[Dict]:
        """Legacy method for backwards compatibility"""
        return IndonesianPlateManager.parse_plate(plate)


class VehicleOwner:
    """Represents a vehicle owner with registration details"""
    
    INDONESIAN_FIRST_NAMES = [
        'Budi', 'Siti', 'Ahmad', 'Rina', 'Suryanto', 'Dewi', 'Hendra', 'Putri',
        'Bambang', 'Indra', 'Nurhayati', 'Wawan', 'Sari', 'Totok', 'Retno',
        'Yudi', 'Maya', 'Kusuma', 'Handoko', 'Lestari', 'Adi', 'Diana',
        'Prayogo', 'Fitri', 'Rendi', 'Ayu', 'Wahyu', 'Nisak', 'Haryo'
    ]
    
    INDONESIAN_LAST_NAMES = [
        'Wijaya', 'Santoso', 'Rahman', 'Setiawan', 'Gunawan', 'Hartono',
        'Kusuma', 'Hermawan', 'Pratama', 'Sugiono', 'Prasetyo', 'Wibowo',
        'Nugroho', 'Cahyono', 'Sumarlin', 'Hermansyah', 'Bambang',
        'Prabowo', 'Sumargo', 'Indrawan', 'Pujadi', 'Ningsih', 'Sutrisno'
    ]
    
    def __init__(
        self,
        owner_id: str,
        name: str,
        region: str,
        sub_region: str,
        stnk_status: bool,
        sim_status: bool,
        vehicle_type: str = 'roda_dua'
    ):
        """Simple owner object"""
        self.owner_id = owner_id
        self.name = name
        self.region = region
        self.sub_region = sub_region
        self.stnk_status = stnk_status
        self.sim_status = sim_status
        self.vehicle_type = vehicle_type
        self.stnk_expiry = self._generate_stnk_expiry(stnk_status)
        self.sim_expiry = self._generate_sim_expiry(sim_status)
        self.registration_date = datetime.now() - timedelta(days=random.randint(30, 365*3))
    
    # Load base.csv data for real administrative codes (cached for performance)
    _ADMIN_CODES_CACHE = None
    
    @staticmethod
    def _load_admin_codes_from_base_csv():
        """Load administrative codes from base.csv (province, kabupaten, kecamatan)"""
        if VehicleOwner._ADMIN_CODES_CACHE is not None:
            return VehicleOwner._ADMIN_CODES_CACHE
        
        admin_data = {}
        
        try:
            base_csv_path = Path(__file__).parent.parent / 'base.csv'
            
            if not base_csv_path.exists():
                # Fallback if file not found
                return None
            
            with open(base_csv_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = line.split(',', 1)
                    if len(parts) < 2:
                        continue
                    
                    code = parts[0]
                    name = parts[1]
                    
                    # Store mapping: name -> code
                    admin_data[name.strip().upper()] = code
            
            VehicleOwner._ADMIN_CODES_CACHE = admin_data
            return admin_data
        except Exception:
            return None
    
    @staticmethod
    def _extract_administrative_codes(region: str, sub_region: str) -> Tuple[str, str]:
        """
        Extract real district and subdistrict codes from base.csv data
        
        Looks up region and sub_region names in base.csv to get actual administrative codes
        
        Returns: (district_code, subdistrict_code) as 2-digit strings
        
        Format of codes:
        - Province: 11 (Aceh)
        - District/Kabupaten: 11.01 (Aceh Selatan)
        - Subdistrict/Kecamatan: 11.01.01 (Bakongan)
        """
        # Load admin data
        admin_data = VehicleOwner._load_admin_codes_from_base_csv()
        
        if admin_data is None:
            # Fallback to random if CSV not available
            return f"{random.randint(1, 99):02d}", f"{random.randint(1, 99):02d}"
        
        # Look up district code from region name or sub_region
        region_upper = region.upper()
        district_code = None
        
        # First, try to find district using sub_region (which is more specific)
        if sub_region:
            sub_region_upper = sub_region.upper()
            # Search for district level codes using sub_region
            for name, code in admin_data.items():
                # Match district level codes (format: XX.YY)
                if '.' in code and code.count('.') == 1:
                    if sub_region_upper in name:
                        district_code = code
                        break
            
            # If not found, try partial match with sub_region
            if not district_code:
                for name, code in admin_data.items():
                    if '.' in code and code.count('.') == 1:
                        if any(word in name for word in sub_region_upper.split()):
                            district_code = code
                            break
        
        # Fallback: Search for matching district using region name
        if not district_code:
            for name, code in admin_data.items():
                # Match district level codes (format: XX.YY)
                if '.' in code and code.count('.') == 1:
                    if region_upper in name or region.upper() in name:
                        district_code = code
                        break
        
        # If still not found, try partial match with region
        if not district_code:
            for name, code in admin_data.items():
                if '.' in code and code.count('.') == 1:
                    if any(word in name for word in region_upper.split()):
                        district_code = code
                        break
        
        # Look up subdistrict code from sub_region name
        subdistrict_code = None
        
        if sub_region:
            sub_region_upper = sub_region.upper()
            
            # Search for matching subdistrict
            for name, code in admin_data.items():
                # Match subdistrict level codes (format: XX.YY.ZZ)
                if code.count('.') == 2:
                    if sub_region_upper in name or sub_region.upper() in name:
                        subdistrict_code = code
                        break
            
            # If not found, try partial match
            if not subdistrict_code:
                for name, code in admin_data.items():
                    if code.count('.') == 2:
                        if any(word in name for word in sub_region_upper.split()):
                            subdistrict_code = code
                            break
        
        # Extract the numeric parts from codes
        if district_code and '.' in district_code:
            dist_parts = district_code.split('.')
            district_num = dist_parts[1] if len(dist_parts) > 1 else f"{random.randint(1, 99):02d}"
        else:
            district_num = f"{random.randint(1, 99):02d}"
        
        if subdistrict_code and '.' in subdistrict_code:
            subdist_parts = subdistrict_code.split('.')
            subdistrict_num = subdist_parts[2] if len(subdist_parts) > 2 else f"{random.randint(1, 99):02d}"
        else:
            subdistrict_num = f"{random.randint(1, 99):02d}"
        
        return district_num, subdistrict_num
    
    @staticmethod
    def generate_random_owner(region: str, sub_region: str, vehicle_type: str = 'roda_dua', required_province_code: Optional[str] = None, is_special_plate: bool = False) -> 'VehicleOwner':
        """
        Generate random owner with NIK synchronized to plate region.
        
        Args:
            region: Region name (e.g., 'DKI Jakarta')
            sub_region: Sub-region name (e.g., 'Jakarta Selatan')
            vehicle_type: 'roda_dua' (motorcycle) or 'roda_empat' (car)
            required_province_code: Province code from plate (e.g., '31' for Jakarta)
            is_special_plate: If True, use generic codes for special plates (RI, CD, CC)
        
        Returns:
            VehicleOwner with valid NIK matching plate region
        """
        # Step 1: Province code (from plate or random)
        if required_province_code:
            province_code = required_province_code
        else:
            province_code = f"{random.randint(1, 34):02d}"
        
        # Step 2: Extract administrative codes from region/sub_region (skip for special plates)
        if is_special_plate:
            # For special plates (RI, CD, CC), use fixed codes
            district_code = '00'
            subdistrict_code = '00'
        else:
            district_code, subdistrict_code = VehicleOwner._extract_administrative_codes(region, sub_region)
        
        # Step 3: Randomize birth data
        birth_day = random.randint(1, 28)
        is_female = random.random() < 0.5
        if is_female:
            birth_day += 40
        birth_date = f"{birth_day:02d}"
        
        birth_month = f"{random.randint(1, 12):02d}"
        birth_year = f"{random.randint(50, 99):02d}"
        
        # Step 4: Randomize sequential number
        sequential_number = f"{random.randint(1, 9999):04d}"
        
        # Construct NIK: [province][district][subdistrict][birth_date][birth_month][birth_year][sequential]
        owner_id = f"{province_code}{district_code}{subdistrict_code}{birth_date}{birth_month}{birth_year}{sequential_number}"
        
        # Generate name
        first_name = random.choice(VehicleOwner.INDONESIAN_FIRST_NAMES)
        last_name = random.choice(VehicleOwner.INDONESIAN_LAST_NAMES)
        name = f"{first_name} {last_name}"
        
        # Randomize document status
        stnk_status = random.random() < 0.7
        sim_status = random.random() < 0.8
        
        return VehicleOwner(owner_id, name, region, sub_region, stnk_status, sim_status, vehicle_type)
    
    @staticmethod
    def generate_independent_nik(region: str, sub_region: str, vehicle_type: str = 'roda_dua') -> 'VehicleOwner':
        """
        Generate owner with completely independent NIK NOT based on plate region.
        Used for special vehicle categories: PEMERINTAH (Government) and KEDUTAAN (Diplomatic)
        
        Args:
            region: Region name (e.g., 'Pemerintah Indonesia', 'Diplomatik')
            sub_region: Sub-region name
            vehicle_type: 'roda_dua' or 'roda_empat'
        
        Returns:
            VehicleOwner with valid independent NIK (not tied to any plate region)
        """
        # Generate completely random province code (01-34) - NOT from plate
        province_code = f"{random.randint(1, 34):02d}"
        
        # Generate random administrative codes (not extracted from CSV)
        district_code = f"{random.randint(1, 99):02d}"
        subdistrict_code = f"{random.randint(1, 99):02d}"
        
        # Randomize birth data
        birth_day = random.randint(1, 28)
        is_female = random.random() < 0.5
        if is_female:
            birth_day += 40
        birth_date = f"{birth_day:02d}"
        
        birth_month = f"{random.randint(1, 12):02d}"
        birth_year = f"{random.randint(50, 99):02d}"
        
        # Randomize sequential number
        sequential_number = f"{random.randint(1, 9999):04d}"
        
        # Construct NIK: [province][district][subdistrict][birth_date][birth_month][birth_year][sequential]
        owner_id = f"{province_code}{district_code}{subdistrict_code}{birth_date}{birth_month}{birth_year}{sequential_number}"
        
        # Generate name
        first_name = random.choice(VehicleOwner.INDONESIAN_FIRST_NAMES)
        last_name = random.choice(VehicleOwner.INDONESIAN_LAST_NAMES)
        name = f"{first_name} {last_name}"
        
        # Randomize document status
        stnk_status = random.random() < 0.7
        sim_status = random.random() < 0.8
        
        return VehicleOwner(owner_id, name, region, sub_region, stnk_status, sim_status, vehicle_type)
    
    @staticmethod
    def _generate_stnk_expiry(is_active: bool) -> datetime:
        if is_active:
            days = random.randint(30, 365*5)
            return datetime.now() + timedelta(days=days)
        else:
            days = -random.randint(30, 730)
            return datetime.now() + timedelta(days=days)
    
    @staticmethod
    def _generate_sim_expiry(is_active: bool) -> datetime:
        if is_active:
            days = random.randint(30, 365*5)
            return datetime.now() + timedelta(days=days)
        else:
            days = -random.randint(30, 1095)
            return datetime.now() + timedelta(days=days)
    
    def get_vehicle_type_display(self) -> str:
        """Get vehicle type display"""
        if self.vehicle_type == 'roda_dua':
            return 'Roda Dua (Motor)'
        else:
            return 'Roda Empat atau lebih (Mobil)'
    
    def get_stnk_status_display(self) -> str:
        """Get STNK status display"""
        if self.stnk_status:
            return f"Active (Expires: {self.stnk_expiry.strftime('%Y-%m-%d')})"
        else:
            return f"Non-Active (Expired: {self.stnk_expiry.strftime('%Y-%m-%d')})"
    
    def get_sim_status_display(self) -> str:
        """Get SIM status display"""
        if self.sim_status:
            return f"Active (Expires: {self.sim_expiry.strftime('%Y-%m-%d')})"
        else:
            return f"Expired (Expired: {self.sim_expiry.strftime('%Y-%m-%d')})"
    
    def is_violation_risk(self) -> bool:
        """Check if owner has inactive STNK or SIM"""
        return not self.stnk_status or not self.sim_status
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'owner_id': self.owner_id,
            'name': self.name,
            'region': self.region,
            'sub_region': self.sub_region,
            'vehicle_type': self.get_vehicle_type_display(),
            'stnk_status': 'Active' if self.stnk_status else 'Non-Active',
            'stnk_expiry': self.stnk_expiry.strftime('%Y-%m-%d'),
            'sim_status': 'Active' if self.sim_status else 'Expired',
            'sim_expiry': self.sim_expiry.strftime('%Y-%m-%d'),
            'registration_date': self.registration_date.strftime('%Y-%m-%d'),
            'is_violation_risk': self.is_violation_risk()
        }


class OwnerDatabase:
    """Database for storing vehicle owners by license plate"""
    
    def __init__(self):
        self.owners: Dict[str, VehicleOwner] = {}
    
    def register_vehicle(self, plate: str, owner: VehicleOwner) -> None:
        """Register a vehicle with its owner"""
        self.owners[plate] = owner
    
    def get_owner(self, plate: str) -> Optional[VehicleOwner]:
        """Get owner by plate number"""
        return self.owners.get(plate)
    
    def get_or_create_owner(self, plate: str, vehicle_type: str = 'roda_dua', vehicle_category: str = None) -> VehicleOwner:
        """Get existing owner or create a new one with KTP-Plate synchronization
        
        Extracts region information from plate number to generate owner from correct region.
        Uses CSV administrative codes to generate proper NIK aligned with plate region.
        Handles both old and new plate formats.
        Handles special cases: Government (RI) and Diplomatic (CD/CC) plates.
        
        Args:
            plate: License plate string
            vehicle_type: 'roda_dua' or 'roda_empat'
            vehicle_category: Optional - 'PEMERINTAH' or 'KEDUTAAN' for independent NIK generation
        """
        if plate in self.owners:
            return self.owners[plate]
        
        # Extract plate code (first part of plate before space)
        parts = plate.split()
        plate_code = parts[0] if parts else 'B'
        
        # Parse plate to get region information
        plate_info = IndonesianPlateManager.parse_plate(plate)
        
        # Handle special vehicle categories: Government (PEMERINTAH) and Diplomatic (KEDUTAAN)
        # These use independent NIK generation that doesn't depend on plate region
        if vehicle_category in ('PEMERINTAH', 'KEDUTAAN'):
            if vehicle_category == 'PEMERINTAH':
                region = 'Pemerintah Indonesia'
                sub_region = 'Pemerintah Indonesia'
            else:  # KEDUTAAN
                region = 'Diplomatik'
                sub_region = 'Diplomatik'
            
            # Generate completely independent NIK for special vehicles
            # NOT based on plate region codes
            owner = VehicleOwner.generate_independent_nik(
                region, 
                sub_region, 
                vehicle_type
            )
            self.owners[plate] = owner
            return owner
        
        # Handle special plates: Government (RI) and Diplomatic (CD/CC)
        if plate_code in ('RI', 'CD', 'CC'):
            # These are special plates without regional mapping
            # Generate owner with only province code (no administrative codes)
            if plate_code == 'RI':
                region = 'Pemerintah Indonesia'
                sub_region = 'Pemerintah Indonesia'
                # Use a special code for government vehicles
                province_code = '00'  # Special code for government
            else:  # CD or CC (Diplomatic)
                region = 'Diplomatik'
                sub_region = 'Diplomatik'
                # Use a special code for diplomatic vehicles
                province_code = '99'  # Special code for diplomatic
            
            # Create owner WITHOUT extracting administrative codes
            owner = VehicleOwner.generate_random_owner(
                region, 
                sub_region, 
                vehicle_type,
                required_province_code=province_code,
                is_special_plate=True  # Flag to skip administrative code extraction
            )
            self.owners[plate] = owner
            return owner
        
        # Get the required province code from plate for KTP synchronization
        required_province_code = IndonesianPlateManager.get_province_code_from_plate_code(plate_code)
        
        # Get sub_region from parsed plate (which now correctly extracts it from plate letters)
        sub_region = None
        if plate_info and 'sub_region' in plate_info:
            # Use the parsed plate's sub_region which correctly maps letter to city
            sub_region = plate_info['sub_region']
            region = plate_info['region_name']
        elif plate_code in IndonesianPlateManager.PLATE_DATA:
            # Fallback: get region from PLATE_DATA
            plate_data = IndonesianPlateManager.PLATE_DATA[plate_code]
            region = plate_data['region_name']
            # Pick a random sub_region from sub_codes if no parsed sub_region available
            if plate_data.get('sub_codes'):
                sub_region = random.choice(list(plate_data['sub_codes'].values()))
            else:
                sub_region = region
        else:
            # Final fallback
            region = 'Jakarta'
            sub_region = 'Jakarta'
            required_province_code = '31'
        
        # Create new owner with synchronized province code from plate
        # IMPORTANT: Pass sub_region to get_or_create_owner to use CSV administrative codes
        owner = VehicleOwner.generate_random_owner(
            region, 
            sub_region, 
            vehicle_type,
            required_province_code=required_province_code,  # SYNCHRONIZATION POINT
            is_special_plate=False
        )
        self.owners[plate] = owner
        
        return owner
    
    def save_to_file(self, filepath: str) -> None:
        """Save database to JSON file"""
        data = {plate: owner.to_dict() for plate, owner in self.owners.items()}
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_from_file(self, filepath: str) -> None:
        """Load database from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for plate, owner_data in data.items():
                vehicle_type = 'roda_dua' if 'Roda Dua' in owner_data.get('vehicle_type', '') else 'roda_empat'
                owner = VehicleOwner(
                    owner_id=owner_data['owner_id'],
                    name=owner_data['name'],
                    region=owner_data['region'],
                    sub_region=owner_data.get('sub_region', ''),
                    stnk_status=owner_data['stnk_status'] == 'Active',
                    sim_status=owner_data['sim_status'] == 'Active',
                    vehicle_type=vehicle_type
                )
                self.owners[plate] = owner
        except FileNotFoundError:
            pass


# Global database instance
owner_db = OwnerDatabase()
