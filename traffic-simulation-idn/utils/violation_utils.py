"""
Utility functions for Indonesian traffic violation system
"""

import json
from typing import List, Dict, Any
from utils.indonesian_plates import IndonesianPlateManager, owner_db
from data_models.models import Ticket

def format_violation_report(ticket: Ticket) -> str:
    """Format a ticket as a detailed violation report"""
    report = f"""
╔════════════════════════════════════════════════════════════════╗
║                   TRAFFIC VIOLATION REPORT                     ║
╚════════════════════════════════════════════════════════════════╝

TICKET ID:           {ticket.ticket_id}
LOCATION:            {ticket.location}
TIMESTAMP:           {ticket.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

─── VEHICLE INFORMATION ───
LICENSE PLATE:       {ticket.license_plate}
PLATE REGION:        {IndonesianPlateManager.parse_plate(ticket.license_plate)['region']}
VEHICLE TYPE:        {ticket.vehicle_type}

─── OWNER INFORMATION ───
NAME:                {ticket.owner_name}
ID (NIK):            {ticket.owner_id}
RESIDENCE:           {ticket.owner_region}

─── REGISTRATION STATUS ───
STNK STATUS:         {ticket.stnk_status}
SIM STATUS:          {ticket.sim_status}

─── VIOLATION DETAILS ───
DETECTED SPEED:      {ticket.speed} km/h
SPEED LIMIT:         {ticket.speed_limit} km/h
EXCESS SPEED:        {ticket.speed - ticket.speed_limit} km/h

─── FINE CALCULATION ───
BASE FINE:           ${ticket.base_fine:.2f}
PENALTY MULTIPLIER:  {ticket.penalty_multiplier}x
"""
    
    if ticket.penalty_multiplier > 1.0:
        report += f"PENALTY REASON:      Non-Active STNK & Expired SIM (+20%)\n"
    
    report += f"""
TOTAL FINE:          ${ticket.fine_amount:.2f}

STATUS:              {ticket.status}
════════════════════════════════════════════════════════════════
"""
    return report

def analyze_violations(tickets_file: str) -> Dict[str, Any]:
    """Analyze all violations in tickets file"""
    try:
        with open(tickets_file, 'r', encoding='utf-8') as f:
            tickets = json.load(f)
    except:
        return {'error': 'Could not read tickets file'}
    
    # Analyze data
    analysis = {
        'total_violations': len(tickets),
        'total_fines': sum(t.get('fine', {}).get('total_fine', 0) for t in tickets),
        'by_stnk_status': {},
        'by_sim_status': {},
        'penalties_applied': 0,
        'average_excess_speed': 0,
        'highest_fine': 0,
        'violations_with_penalties': []
    }
    
    excess_speeds = []
    
    for ticket in tickets:
        stnk = ticket.get('registration', {}).get('stnk_status', 'Unknown')
        sim = ticket.get('registration', {}).get('sim_status', 'Unknown')
        
        # Count by status
        analysis['by_stnk_status'][stnk] = analysis['by_stnk_status'].get(stnk, 0) + 1
        analysis['by_sim_status'][sim] = analysis['by_sim_status'].get(sim, 0) + 1
        
        # Check for penalties
        multiplier = ticket.get('fine', {}).get('penalty_multiplier', 1.0)
        if multiplier > 1.0:
            analysis['penalties_applied'] += 1
            analysis['violations_with_penalties'].append({
                'plate': ticket.get('license_plate'),
                'owner': ticket.get('owner', {}).get('name'),
                'speed': ticket.get('speed'),
                'base_fine': ticket.get('fine', {}).get('base_fine'),
                'total_fine': ticket.get('fine', {}).get('total_fine'),
                'penalty': f"+{(multiplier-1)*100:.0f}%"
            })
        
        # Track speeds and fines
        speed = ticket.get('speed', 0)
        excess_speeds.append(speed - ticket.get('speed_limit', 75))
        fine = ticket.get('fine', {}).get('total_fine', 0)
        if fine > analysis['highest_fine']:
            analysis['highest_fine'] = fine
    
    if excess_speeds:
        analysis['average_excess_speed'] = round(sum(excess_speeds) / len(excess_speeds), 1)
    
    return analysis

def print_violation_analysis(analysis: Dict[str, Any]):
    """Print formatted violation analysis"""
    print("\n" + "="*70)
    print("          VIOLATION ANALYSIS REPORT")
    print("="*70)
    
    print(f"\nTotal Violations: {analysis['total_violations']}")
    print(f"Total Fines Collected: ${analysis['total_fines']:.2f}")
    print(f"Average Excess Speed: {analysis['average_excess_speed']} km/h")
    print(f"Highest Fine: ${analysis['highest_fine']:.2f}")
    
    print("\n─── REGISTRATION STATUS ───")
    for status, count in analysis['by_stnk_status'].items():
        pct = (count / analysis['total_violations'] * 100) if analysis['total_violations'] > 0 else 0
        print(f"  STNK {status}: {count} ({pct:.1f}%)")
    
    for status, count in analysis['by_sim_status'].items():
        pct = (count / analysis['total_violations'] * 100) if analysis['total_violations'] > 0 else 0
        print(f"  SIM {status}: {count} ({pct:.1f}%)")
    
    print(f"\n─── PENALTIES ───")
    print(f"Violations with +20% Penalty: {analysis['penalties_applied']}")
    
    if analysis['violations_with_penalties']:
        print(f"\nTop Penalties Applied:")
        for i, v in enumerate(analysis['violations_with_penalties'][:5], 1):
            print(f"  {i}. {v['plate']} - {v['owner']}")
            print(f"     Speed: {v['speed']} km/h | Fine: ${v['base_fine']:.0f} → ${v['total_fine']:.0f} {v['penalty']}")
    
    print("\n" + "="*70 + "\n")
