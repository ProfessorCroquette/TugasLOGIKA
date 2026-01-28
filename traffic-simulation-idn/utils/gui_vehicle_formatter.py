"""
GUI Component Example: Vehicle Display with Color-Coded License Plates
Demonstrates integration of plate generator output with PyQt5 GUI

This example shows how to:
1. Display vehicles with color-coded plates
2. Show vehicle information (category, owner, etc.)
3. Filter by vehicle type or category
4. Render plate background colors
"""

import sys
sys.path.insert(0, '.')

from typing import List, Dict, Optional
from data_models.models import Vehicle

# Color mapping for different plate types
PLATE_COLOR_MAP = {
    'BLACK': {
        'background': '#000000',
        'text': '#FFFFFF',
        'border': '#FFD700'
    },
    'YELLOW': {
        'background': '#FFD700',
        'text': '#000000',
        'border': '#FFA500'
    },
    'RED': {
        'background': '#DC143C',
        'text': '#FFFFFF',
        'border': '#8B0000'
    },
    'WHITE': {
        'background': '#FFFFFF',
        'text': '#000000',
        'border': '#000000'
    }
}

# Category icons and descriptions
CATEGORY_INFO = {
    'Pribadi': {
        'icon': '🚗',
        'description': 'Private Vehicle',
        'plate_type': 'PRIBADI'
    },
    'Barang': {
        'icon': '🚛',
        'description': 'Commercial/Truck',
        'plate_type': 'NIAGA/TRUK'
    },
    'PEMERINTAH': {
        'icon': '🚔',
        'description': 'Government Vehicle',
        'plate_type': 'PEMERINTAH'
    },
    'KEDUTAAN': {
        'icon': '🏳️',
        'description': 'Diplomatic Vehicle',
        'plate_type': 'DIPLOMATIK'
    }
}


class VehicleDisplayFormatter:
    """Helper class for formatting vehicle information for GUI display"""
    
    @staticmethod
    def get_plate_html(vehicle: Vehicle) -> str:
        """Generate HTML for license plate display with proper coloring
        
        Args:
            vehicle: Vehicle object
            
        Returns:
            HTML string for plate display
        """
        colors = PLATE_COLOR_MAP.get(vehicle.plate_color, PLATE_COLOR_MAP['BLACK'])
        
        html = f"""
        <div style="
            background-color: {colors['background']};
            color: {colors['text']};
            border: 2px solid {colors['border']};
            padding: 8px 12px;
            border-radius: 4px;
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            text-align: center;
            min-width: 200px;
            font-size: 18px;
            margin: 5px 0;
        ">
            {vehicle.license_plate}
        </div>
        """
        return html
    
    @staticmethod
    def get_vehicle_info(vehicle: Vehicle) -> Dict[str, str]:
        """Get formatted vehicle information
        
        Args:
            vehicle: Vehicle object
            
        Returns:
            Dictionary with formatted information
        """
        category = vehicle.vehicle_category
        info = CATEGORY_INFO.get(category, CATEGORY_INFO['Pribadi'])
        
        return {
            'plate': vehicle.license_plate,
            'plate_type': vehicle.plate_type,
            'plate_color': vehicle.plate_color,
            'category': category,
            'category_icon': info['icon'],
            'category_desc': info['description'],
            'make': vehicle.vehicle_make,
            'model': vehicle.vehicle_model,
            'owner': vehicle.owner_name,
            'region': vehicle.owner_region,
            'speed': f"{vehicle.speed:.1f} km/h",
            'stnk': vehicle.stnk_status,
            'sim': vehicle.sim_status,
            'vehicle_type': vehicle.vehicle_type
        }
    
    @staticmethod
    def get_vehicle_summary(vehicle: Vehicle) -> str:
        """Get one-line summary of vehicle
        
        Args:
            vehicle: Vehicle object
            
        Returns:
            Summary string
        """
        info = VehicleDisplayFormatter.get_vehicle_info(vehicle)
        return (f"{info['category_icon']} {vehicle.license_plate} | "
                f"{vehicle.vehicle_make} | "
                f"{info['category_desc']} | "
                f"Speed: {info['speed']}")
    
    @staticmethod
    def get_vehicle_details(vehicle: Vehicle) -> str:
        """Get detailed information string about vehicle
        
        Args:
            vehicle: Vehicle object
            
        Returns:
            Detailed information string
        """
        info = VehicleDisplayFormatter.get_vehicle_info(vehicle)
        
        details = f"""
VEHICLE INFORMATION
{'='*60}

License Plate: {info['plate']}
  Type:  {info['plate_type']}
  Color: {info['plate_color']}

Category: {info['category_icon']} {info['category_desc']}
  Vehicle Type: {info['vehicle_type']}

Make & Model:
  {info['make']}

Owner Information:
  Name:   {info['owner']}
  Region: {info['region']}

Status:
  Speed:       {info['speed']}
  STNK Status: {info['stnk']}
  SIM Status:  {info['sim']}
{'='*60}
        """
        return details
    
    @staticmethod
    def filter_vehicles_by_category(
        vehicles: List[Vehicle],
        category: Optional[str] = None
    ) -> List[Vehicle]:
        """Filter vehicles by category
        
        Args:
            vehicles: List of vehicles
            category: Category to filter by (None for all)
            
        Returns:
            Filtered list of vehicles
        """
        if category is None or category == 'All':
            return vehicles
        
        return [v for v in vehicles if v.vehicle_category == category]
    
    @staticmethod
    def filter_vehicles_by_plate_color(
        vehicles: List[Vehicle],
        color: Optional[str] = None
    ) -> List[Vehicle]:
        """Filter vehicles by plate color
        
        Args:
            vehicles: List of vehicles
            color: Plate color to filter by (None for all)
            
        Returns:
            Filtered list of vehicles
        """
        if color is None or color == 'All':
            return vehicles
        
        return [v for v in vehicles if v.plate_color == color]
    
    @staticmethod
    def get_statistics(vehicles: List[Vehicle]) -> Dict[str, any]:
        """Get statistics about vehicle batch
        
        Args:
            vehicles: List of vehicles
            
        Returns:
            Dictionary with statistics
        """
        from collections import Counter
        
        categories = Counter(v.vehicle_category for v in vehicles)
        colors = Counter(v.plate_color for v in vehicles)
        types = Counter(v.vehicle_type for v in vehicles)
        speeds = [v.speed for v in vehicles]
        
        return {
            'total_vehicles': len(vehicles),
            'categories': dict(categories),
            'plate_colors': dict(colors),
            'vehicle_types': dict(types),
            'avg_speed': sum(speeds) / len(speeds) if speeds else 0,
            'max_speed': max(speeds) if speeds else 0,
            'min_speed': min(speeds) if speeds else 0,
        }


# Example usage
if __name__ == '__main__':
    from utils.generators import DataGenerator
    
    print("=" * 70)
    print("GUI Integration Example: Vehicle Display with Color-Coded Plates")
    print("=" * 70)
    
    # Generate sample vehicles
    vehicles = DataGenerator.generate_vehicle_batch()
    
    print(f"\nGenerated {len(vehicles)} vehicles\n")
    
    # Display each vehicle with color coding information
    for i, vehicle in enumerate(vehicles[:3], 1):
        print(f"\n{i}. Vehicle Summary:")
        print(f"   {VehicleDisplayFormatter.get_vehicle_summary(vehicle)}")
        print(f"\n   Plate HTML (for GUI rendering):")
        print(f"   {VehicleDisplayFormatter.get_plate_html(vehicle)}")
    
    # Show filtering example
    print("\n" + "=" * 70)
    print("Filtering Examples")
    print("=" * 70)
    
    pribadi_vehicles = VehicleDisplayFormatter.filter_vehicles_by_category(
        vehicles, 'Pribadi'
    )
    print(f"\nPrivate vehicles (Pribadi): {len(pribadi_vehicles)}")
    
    yellow_plates = VehicleDisplayFormatter.filter_vehicles_by_plate_color(
        vehicles, 'YELLOW'
    )
    print(f"Yellow plates (Commercial): {len(yellow_plates)}")
    
    # Show statistics
    print("\n" + "=" * 70)
    print("Statistics")
    print("=" * 70)
    
    stats = VehicleDisplayFormatter.get_statistics(vehicles)
    print(f"\nTotal vehicles: {stats['total_vehicles']}")
    print(f"Average speed: {stats['avg_speed']:.1f} km/h")
    print(f"Max speed: {stats['max_speed']:.1f} km/h")
    
    print("\nCategory distribution:")
    for category, count in sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True):
        pct = (count / stats['total_vehicles']) * 100
        print(f"  {category:15s}: {count:3d} ({pct:5.1f}%)")
    
    print("\nPlate color distribution:")
    for color, count in sorted(stats['plate_colors'].items(), key=lambda x: x[1], reverse=True):
        pct = (count / stats['total_vehicles']) * 100
        print(f"  {color:10s}: {count:3d} ({pct:5.1f}%)")
