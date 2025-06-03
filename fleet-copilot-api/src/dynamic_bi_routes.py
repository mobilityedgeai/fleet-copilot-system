"""
Rotas Backend para Sistema de IA Dinâmica
Suporte para múltiplas collections com geração automática de componentes
"""

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

# Create blueprint
dynamic_bi_bp = Blueprint('dynamic_bi', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_copilot_components():
    """Get copilot components (processor, etc.)"""
    try:
        from fleet_data_connector import FleetDataConnector
        
        processor = FleetDataConnector()
        
        return {
            'processor': processor,
            'status': 'success'
        }
    except Exception as e:
        logger.error(f"Error getting copilot components: {str(e)}")
        return {
            'processor': None,
            'status': 'error',
            'message': str(e)
        }

@dynamic_bi_bp.route('/collections', methods=['GET'])
@cross_origin()
def get_available_collections():
    """Get list of available collections for BI analysis"""
    try:
        collections = {
            'checklist': {
                'name': 'Checklist de Veículos',
                'description': 'Inspeções e verificações de conformidade dos veículos',
                'icon': 'fas fa-clipboard-check',
                'color': '#1abc9c',
                'endpoint': '/checklist',
                'fields': ['vehiclePlate', 'driverName', 'itemName', 'noCompliant', 'created_at']
            },
            'trips': {
                'name': 'Viagens',
                'description': 'Histórico de viagens e rotas dos veículos',
                'icon': 'fas fa-route',
                'color': '#3498db',
                'endpoint': '/driver-trips',
                'fields': ['vehiclePlate', 'driverName', 'origin', 'destination', 'distance', 'duration']
            },
            'alerts': {
                'name': 'Alertas',
                'description': 'Alertas e notificações do sistema de monitoramento',
                'icon': 'fas fa-exclamation-triangle',
                'color': '#e74c3c',
                'endpoint': '/alerts-checkin',
                'fields': ['vehiclePlate', 'alertType', 'severity', 'timestamp', 'status']
            },
            'maintenance': {
                'name': 'Manutenção',
                'description': 'Agendamentos e histórico de manutenção preventiva e corretiva',
                'icon': 'fas fa-tools',
                'color': '#f39c12',
                'endpoint': '/maintenance',
                'fields': ['vehiclePlate', 'maintenanceType', 'scheduledDate', 'status', 'cost']
            },
            'drivers': {
                'name': 'Motoristas',
                'description': 'Performance e dados dos motoristas da frota',
                'icon': 'fas fa-user-tie',
                'color': '#9b59b6',
                'endpoint': '/drivers',
                'fields': ['driverName', 'score', 'violations', 'totalTrips', 'status']
            },
            'vehicles': {
                'name': 'Veículos',
                'description': 'Informações e status da frota de veículos',
                'icon': 'fas fa-truck',
                'color': '#27ae60',
                'endpoint': '/vehicles',
                'fields': ['vehiclePlate', 'vehicleType', 'status', 'mileage', 'lastMaintenance']
            }
        }
        
        return jsonify({
            'success': True,
            'data': collections,
            'message': 'Collections retrieved successfully'
        })
        
    except Exception as e:
        logger.error(f"Error getting collections: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error getting collections: {str(e)}'
        }), 500

@dynamic_bi_bp.route('/trips', methods=['GET'])
@cross_origin()
def get_trips_analysis():
    """Get trips analysis data"""
    try:
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = int(request.args.get('days', 30))
        
        components = get_copilot_components()
        if components['status'] == 'error':
            return jsonify({
                'success': False,
                'message': components['message']
            }), 500
        
        processor = components['processor']
        
        # Get trips data (simulated for now)
        trips_data = generate_sample_trips_data(enterprise_id, days)
        
        # Calculate metrics
        metrics = calculate_trips_metrics(trips_data)
        
        # Generate chart data
        chart_data = generate_trips_charts(trips_data)
        
        return jsonify({
            'success': True,
            'data': {
                **metrics,
                'chart_data': chart_data,
                'raw_data': trips_data,
                'period_days': days,
                'enterprise_id': enterprise_id
            }
        })
        
    except Exception as e:
        logger.error(f"Error in trips analysis: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error in trips analysis: {str(e)}'
        }), 500

@dynamic_bi_bp.route('/alerts', methods=['GET'])
@cross_origin()
def get_alerts_analysis():
    """Get alerts analysis data"""
    try:
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = int(request.args.get('days', 30))
        
        components = get_copilot_components()
        if components['status'] == 'error':
            return jsonify({
                'success': False,
                'message': components['message']
            }), 500
        
        processor = components['processor']
        
        # Get alerts data (simulated for now)
        alerts_data = generate_sample_alerts_data(enterprise_id, days)
        
        # Calculate metrics
        metrics = calculate_alerts_metrics(alerts_data)
        
        # Generate chart data
        chart_data = generate_alerts_charts(alerts_data)
        
        return jsonify({
            'success': True,
            'data': {
                **metrics,
                'chart_data': chart_data,
                'raw_data': alerts_data,
                'period_days': days,
                'enterprise_id': enterprise_id
            }
        })
        
    except Exception as e:
        logger.error(f"Error in alerts analysis: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error in alerts analysis: {str(e)}'
        }), 500

@dynamic_bi_bp.route('/maintenance', methods=['GET'])
@cross_origin()
def get_maintenance_analysis():
    """Get maintenance analysis data"""
    try:
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = int(request.args.get('days', 30))
        
        components = get_copilot_components()
        if components['status'] == 'error':
            return jsonify({
                'success': False,
                'message': components['message']
            }), 500
        
        processor = components['processor']
        
        # Get maintenance data (simulated for now)
        maintenance_data = generate_sample_maintenance_data(enterprise_id, days)
        
        # Calculate metrics
        metrics = calculate_maintenance_metrics(maintenance_data)
        
        # Generate chart data
        chart_data = generate_maintenance_charts(maintenance_data)
        
        return jsonify({
            'success': True,
            'data': {
                **metrics,
                'chart_data': chart_data,
                'raw_data': maintenance_data,
                'period_days': days,
                'enterprise_id': enterprise_id
            }
        })
        
    except Exception as e:
        logger.error(f"Error in maintenance analysis: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error in maintenance analysis: {str(e)}'
        }), 500

@dynamic_bi_bp.route('/drivers', methods=['GET'])
@cross_origin()
def get_drivers_analysis():
    """Get drivers analysis data"""
    try:
        enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
        days = int(request.args.get('days', 30))
        
        components = get_copilot_components()
        if components['status'] == 'error':
            return jsonify({
                'success': False,
                'message': components['message']
            }), 500
        
        processor = components['processor']
        
        # Get drivers data (simulated for now)
        drivers_data = generate_sample_drivers_data(enterprise_id, days)
        
        # Calculate metrics
        metrics = calculate_drivers_metrics(drivers_data)
        
        # Generate chart data
        chart_data = generate_drivers_charts(drivers_data)
        
        return jsonify({
            'success': True,
            'data': {
                **metrics,
                'chart_data': chart_data,
                'raw_data': drivers_data,
                'period_days': days,
                'enterprise_id': enterprise_id
            }
        })
        
    except Exception as e:
        logger.error(f"Error in drivers analysis: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error in drivers analysis: {str(e)}'
        }), 500

# Helper functions for data generation and analysis

def generate_sample_trips_data(enterprise_id, days):
    """Generate sample trips data"""
    import random
    from datetime import datetime, timedelta
    
    vehicles = ['ABC1234', 'DEF5678', '4564564', 'GHI9012']
    drivers = ['João Silva', 'Maria Santos', 'Pedro Costa', 'Ana Oliveira']
    origins = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Brasília']
    destinations = ['Campinas', 'Niterói', 'Contagem', 'Goiânia']
    
    trips = []
    for i in range(random.randint(20, 50)):
        trip_date = datetime.now() - timedelta(days=random.randint(0, days))
        trips.append({
            'id': f'trip_{i}',
            'date': trip_date.isoformat(),
            'vehiclePlate': random.choice(vehicles),
            'driverName': random.choice(drivers),
            'origin': random.choice(origins),
            'destination': random.choice(destinations),
            'distance': random.randint(50, 500),
            'duration': f"{random.randint(1, 8)}h{random.randint(0, 59)}m",
            'avgSpeed': random.randint(60, 90),
            'fuelConsumption': round(random.uniform(8, 15), 2),
            'enterpriseId': enterprise_id
        })
    
    return trips

def generate_sample_alerts_data(enterprise_id, days):
    """Generate sample alerts data"""
    import random
    from datetime import datetime, timedelta
    
    vehicles = ['ABC1234', 'DEF5678', '4564564', 'GHI9012']
    alert_types = ['Velocidade Excessiva', 'Freada Brusca', 'Aceleração Brusca', 'Manutenção Preventiva']
    severities = ['low', 'medium', 'high', 'critical']
    statuses = ['active', 'resolved']
    
    alerts = []
    for i in range(random.randint(10, 30)):
        alert_date = datetime.now() - timedelta(days=random.randint(0, days))
        alerts.append({
            'id': f'alert_{i}',
            'timestamp': alert_date.isoformat(),
            'vehiclePlate': random.choice(vehicles),
            'alertType': random.choice(alert_types),
            'severity': random.choice(severities),
            'description': f'Alerta de {random.choice(alert_types)} detectado',
            'status': random.choice(statuses),
            'enterpriseId': enterprise_id
        })
    
    return alerts

def generate_sample_maintenance_data(enterprise_id, days):
    """Generate sample maintenance data"""
    import random
    from datetime import datetime, timedelta
    
    vehicles = ['ABC1234', 'DEF5678', '4564564', 'GHI9012']
    maintenance_types = ['Preventiva', 'Corretiva', 'Preditiva', 'Emergencial']
    statuses = ['scheduled', 'in_progress', 'completed', 'cancelled']
    technicians = ['Carlos Mecânico', 'José Técnico', 'Roberto Silva', 'Fernando Costa']
    
    maintenance = []
    for i in range(random.randint(15, 25)):
        scheduled_date = datetime.now() + timedelta(days=random.randint(-days, 30))
        maintenance.append({
            'id': f'maintenance_{i}',
            'scheduledDate': scheduled_date.isoformat(),
            'vehiclePlate': random.choice(vehicles),
            'maintenanceType': random.choice(maintenance_types),
            'description': f'Manutenção {random.choice(maintenance_types)} programada',
            'status': random.choice(statuses),
            'cost': random.randint(200, 2000),
            'technician': random.choice(technicians),
            'enterpriseId': enterprise_id
        })
    
    return maintenance

def generate_sample_drivers_data(enterprise_id, days):
    """Generate sample drivers data"""
    import random
    
    drivers = ['João Silva', 'Maria Santos', 'Pedro Costa', 'Ana Oliveira', 'Carlos Souza']
    
    drivers_data = []
    for driver in drivers:
        drivers_data.append({
            'id': f'driver_{driver.replace(" ", "_").lower()}',
            'driverName': driver,
            'score': random.randint(60, 100),
            'violations': random.randint(0, 5),
            'totalTrips': random.randint(10, 50),
            'totalDistance': random.randint(1000, 5000),
            'avgSpeed': random.randint(65, 85),
            'status': random.choice(['active', 'inactive']),
            'lastActivity': (datetime.now() - timedelta(days=random.randint(0, days))).isoformat(),
            'enterpriseId': enterprise_id
        })
    
    return drivers_data

def calculate_trips_metrics(trips_data):
    """Calculate trips metrics"""
    if not trips_data:
        return {
            'total_trips': 0,
            'total_distance': 0,
            'avg_speed': 0,
            'fuel_efficiency': 0
        }
    
    total_trips = len(trips_data)
    total_distance = sum(trip['distance'] for trip in trips_data)
    avg_speed = sum(trip['avgSpeed'] for trip in trips_data) / total_trips if total_trips > 0 else 0
    fuel_efficiency = sum(trip.get('fuelConsumption', 10) for trip in trips_data) / total_trips if total_trips > 0 else 0
    
    return {
        'total_trips': total_trips,
        'total_distance': total_distance,
        'avg_speed': round(avg_speed, 1),
        'fuel_efficiency': round(fuel_efficiency, 2)
    }

def calculate_alerts_metrics(alerts_data):
    """Calculate alerts metrics"""
    if not alerts_data:
        return {
            'total_alerts': 0,
            'critical_alerts': 0,
            'resolved_alerts': 0,
            'avg_resolution_time': 0
        }
    
    total_alerts = len(alerts_data)
    critical_alerts = len([a for a in alerts_data if a['severity'] == 'critical'])
    resolved_alerts = len([a for a in alerts_data if a['status'] == 'resolved'])
    
    return {
        'total_alerts': total_alerts,
        'critical_alerts': critical_alerts,
        'resolved_alerts': resolved_alerts,
        'avg_resolution_time': 45  # minutes (simulated)
    }

def calculate_maintenance_metrics(maintenance_data):
    """Calculate maintenance metrics"""
    if not maintenance_data:
        return {
            'scheduled_maintenance': 0,
            'completed_maintenance': 0,
            'overdue_maintenance': 0,
            'total_cost': 0
        }
    
    scheduled = len([m for m in maintenance_data if m['status'] == 'scheduled'])
    completed = len([m for m in maintenance_data if m['status'] == 'completed'])
    overdue = len([m for m in maintenance_data if m['status'] == 'scheduled' and 
                   datetime.fromisoformat(m['scheduledDate'].replace('Z', '+00:00')) < datetime.now()])
    total_cost = sum(m['cost'] for m in maintenance_data if m['status'] == 'completed')
    
    return {
        'scheduled_maintenance': scheduled,
        'completed_maintenance': completed,
        'overdue_maintenance': overdue,
        'total_cost': total_cost
    }

def calculate_drivers_metrics(drivers_data):
    """Calculate drivers metrics"""
    if not drivers_data:
        return {
            'total_drivers': 0,
            'active_drivers': 0,
            'avg_score': 0,
            'violations': 0
        }
    
    total_drivers = len(drivers_data)
    active_drivers = len([d for d in drivers_data if d['status'] == 'active'])
    avg_score = sum(d['score'] for d in drivers_data) / total_drivers if total_drivers > 0 else 0
    total_violations = sum(d['violations'] for d in drivers_data)
    
    return {
        'total_drivers': total_drivers,
        'active_drivers': active_drivers,
        'avg_score': round(avg_score, 1),
        'violations': total_violations
    }

def generate_trips_charts(trips_data):
    """Generate chart data for trips"""
    return {
        'trips_timeline': {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            'data': [12, 19, 3, 5, 2]
        },
        'driver_distances': {
            'labels': ['João', 'Maria', 'Pedro', 'Ana'],
            'data': [1200, 1900, 800, 1500]
        }
    }

def generate_alerts_charts(alerts_data):
    """Generate chart data for alerts"""
    return {
        'severity_distribution': {
            'labels': ['Baixa', 'Média', 'Alta', 'Crítica'],
            'data': [5, 8, 3, 2]
        },
        'alert_types': {
            'labels': ['Velocidade', 'Freada', 'Aceleração', 'Manutenção'],
            'data': [7, 4, 3, 4]
        }
    }

def generate_maintenance_charts(maintenance_data):
    """Generate chart data for maintenance"""
    return {
        'maintenance_timeline': {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            'data': [3, 5, 2, 4, 6]
        },
        'maintenance_types': {
            'labels': ['Preventiva', 'Corretiva', 'Preditiva'],
            'data': [8, 5, 3]
        }
    }

def generate_drivers_charts(drivers_data):
    """Generate chart data for drivers"""
    return {
        'driver_scores': {
            'labels': [d['driverName'] for d in drivers_data[:5]],
            'data': [d['score'] for d in drivers_data[:5]]
        },
        'score_evolution': {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            'data': [85, 87, 83, 89, 91]
        }
    }

