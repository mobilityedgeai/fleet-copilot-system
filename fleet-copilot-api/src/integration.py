"""
Arquivo de integração para o Sistema de BI Melhorado
Conecta todos os componentes: filtros, gráficos, tabelas e IA dinâmica
"""

from flask import Flask, Blueprint
from flask_cors import CORS
import os

def create_enhanced_bi_app():
    """Create Flask app with enhanced BI functionality"""
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Configure app
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['FIREBASE_API_URL'] = os.environ.get('FIREBASE_API_URL', 'https://firebase-bi-api.onrender.com')
    
    # Register blueprints
    register_blueprints(app)
    
    return app

def register_blueprints(app):
    """Register all blueprints"""
    
    # Import existing copilot routes
    try:
        from routes.copilot import copilot_bp
        app.register_blueprint(copilot_bp, url_prefix='/api/copilot')
    except ImportError:
        print("Warning: Could not import copilot routes")
    
    # Import FlutterFlow routes
    try:
        from routes.flutterflow import flutterflow_bp
        app.register_blueprint(flutterflow_bp, url_prefix='/api/flutterflow')
    except ImportError:
        print("Warning: Could not import flutterflow routes")
    
    # Import dynamic BI routes
    try:
        from dynamic_bi_routes import dynamic_bi_bp
        app.register_blueprint(dynamic_bi_bp, url_prefix='/api/copilot')
    except ImportError:
        print("Warning: Could not import dynamic BI routes")
    
    # Add enhanced dashboard route
    add_enhanced_dashboard_route(app)

def add_enhanced_dashboard_route(app):
    """Add enhanced dashboard route"""
    
    @app.route('/api/copilot/enhanced-dashboard')
    def enhanced_dashboard():
        """Serve enhanced dashboard HTML"""
        try:
            # Read the enhanced dashboard HTML
            dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard_melhorado.html')
            
            if os.path.exists(dashboard_path):
                with open(dashboard_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Replace API base URL if needed
                api_base_url = os.environ.get('API_BASE_URL', '')
                if api_base_url:
                    html_content = html_content.replace('window.location.origin', f"'{api_base_url}'")
                
                return html_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
            else:
                return "Enhanced dashboard not found", 404
                
        except Exception as e:
            return f"Error loading enhanced dashboard: {str(e)}", 500
    
    @app.route('/api/copilot/dashboard-assets/<filename>')
    def dashboard_assets(filename):
        """Serve dashboard assets (JS, CSS)"""
        try:
            asset_path = os.path.join(os.path.dirname(__file__), filename)
            
            if os.path.exists(asset_path):
                with open(asset_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Determine content type
                content_type = 'text/javascript' if filename.endswith('.js') else 'text/css'
                
                return content, 200, {'Content-Type': content_type}
            else:
                return "Asset not found", 404
                
        except Exception as e:
            return f"Error loading asset: {str(e)}", 500

def update_main_app():
    """Update main.py to use enhanced BI"""
    main_py_content = '''"""
Enhanced Fleet Copilot API with Advanced BI
"""

from flask import Flask
from flask_cors import CORS
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # App configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['FIREBASE_API_URL'] = os.environ.get('FIREBASE_API_URL', 'https://firebase-bi-api.onrender.com')
    app.config['PORT'] = int(os.environ.get('PORT', 5000))
    
    # Register blueprints
    register_blueprints(app)
    
    # Add health check
    @app.route('/health')
    @app.route('/api/health')
    def health_check():
        return {
            'status': 'healthy',
            'service': 'Fleet Copilot Enhanced BI API',
            'version': '2.0.0'
        }
    
    return app

def register_blueprints(app):
    """Register all application blueprints"""
    
    # Original copilot routes
    try:
        from routes.copilot import copilot_bp
        app.register_blueprint(copilot_bp, url_prefix='/api/copilot')
        logger.info("Registered copilot blueprint")
    except ImportError as e:
        logger.warning(f"Could not import copilot routes: {e}")
    
    # FlutterFlow routes
    try:
        from routes.flutterflow import flutterflow_bp
        app.register_blueprint(flutterflow_bp, url_prefix='/api/flutterflow')
        logger.info("Registered flutterflow blueprint")
    except ImportError as e:
        logger.warning(f"Could not import flutterflow routes: {e}")
    
    # Enhanced BI routes
    try:
        from dynamic_bi_routes import dynamic_bi_bp
        app.register_blueprint(dynamic_bi_bp, url_prefix='/api/copilot')
        logger.info("Registered dynamic BI blueprint")
    except ImportError as e:
        logger.warning(f"Could not import dynamic BI routes: {e}")
    
    # Enhanced dashboard route
    add_dashboard_routes(app)

def add_dashboard_routes(app):
    """Add enhanced dashboard routes"""
    
    @app.route('/api/copilot/enhanced-dashboard')
    def enhanced_dashboard():
        """Serve enhanced dashboard"""
        try:
            dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard_melhorado.html')
            
            if os.path.exists(dashboard_path):
                with open(dashboard_path, 'r', encoding='utf-8') as f:
                    return f.read(), 200, {'Content-Type': 'text/html; charset=utf-8'}
            else:
                return "Enhanced dashboard not found", 404
                
        except Exception as e:
            logger.error(f"Error serving dashboard: {e}")
            return f"Error: {str(e)}", 500
    
    @app.route('/api/copilot/assets/<filename>')
    def dashboard_assets(filename):
        """Serve dashboard assets"""
        try:
            asset_path = os.path.join(os.path.dirname(__file__), filename)
            
            if os.path.exists(asset_path):
                with open(asset_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                content_type = 'text/javascript' if filename.endswith('.js') else 'text/css'
                return content, 200, {'Content-Type': content_type}
            else:
                return "Asset not found", 404
                
        except Exception as e:
            logger.error(f"Error serving asset: {e}")
            return f"Error: {str(e)}", 500

# Create app instance
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Enhanced Fleet Copilot API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
'''
    
    return main_py_content

def create_requirements_txt():
    """Create requirements.txt for the enhanced BI"""
    requirements = """
flask==2.3.3
flask-cors==4.0.0
flask-sqlalchemy==3.0.5
requests==2.31.0
pandas==2.0.3
numpy==1.24.3
python-dateutil==2.8.2
gunicorn==21.2.0
"""
    return requirements.strip()

def create_deployment_config():
    """Create deployment configuration"""
    
    # Render.yaml for deployment
    render_yaml = """
services:
  - type: web
    name: fleet-copilot-enhanced-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn main:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: FLASK_ENV
        value: production
      - key: FIREBASE_API_URL
        value: https://firebase-bi-api.onrender.com
"""
    
    # Dockerfile (optional)
    dockerfile = """
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
"""
    
    return {
        'render.yaml': render_yaml.strip(),
        'Dockerfile': dockerfile.strip()
    }

def create_integration_test():
    """Create integration test script"""
    test_script = """
#!/usr/bin/env python3
"""
Test script for Enhanced BI System
"""

import requests
import json
import time

def test_enhanced_bi_system(base_url="http://localhost:5000"):
    """Test all enhanced BI endpoints"""
    
    print("🧪 Testing Enhanced BI System...")
    print(f"Base URL: {base_url}")
    
    # Test health check
    print("\\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test collections endpoint
    print("\\n2. Testing collections endpoint...")
    try:
        response = requests.get(f"{base_url}/api/copilot/collections")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Collections endpoint passed - {len(data['data'])} collections found")
            else:
                print(f"❌ Collections endpoint failed: {data.get('message')}")
        else:
            print(f"❌ Collections endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Collections endpoint error: {e}")
    
    # Test enhanced dashboard
    print("\\n3. Testing enhanced dashboard...")
    try:
        response = requests.get(f"{base_url}/api/copilot/enhanced-dashboard")
        if response.status_code == 200:
            print("✅ Enhanced dashboard loaded successfully")
        else:
            print(f"❌ Enhanced dashboard failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Enhanced dashboard error: {e}")
    
    # Test collection-specific endpoints
    collections = ['checklist', 'trips', 'alerts', 'maintenance', 'drivers']
    enterprise_id = 'sA9EmrE3ymtnBqJKcYn7'
    
    for collection in collections:
        print(f"\\n4.{collections.index(collection)+1}. Testing {collection} endpoint...")
        try:
            response = requests.get(f"{base_url}/api/copilot/{collection}?enterpriseId={enterprise_id}&days=30")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ {collection.title()} endpoint passed")
                else:
                    print(f"❌ {collection.title()} endpoint failed: {data.get('message')}")
            else:
                print(f"❌ {collection.title()} endpoint failed: {response.status_code}")
        except Exception as e:
            print(f"❌ {collection.title()} endpoint error: {e}")
    
    print("\\n🎉 Enhanced BI System testing completed!")

if __name__ == "__main__":
    import sys
    
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    test_enhanced_bi_system(base_url)
"""
    
    return test_script

# Export functions for use in other modules
__all__ = [
    'create_enhanced_bi_app',
    'register_blueprints',
    'update_main_app',
    'create_requirements_txt',
    'create_deployment_config',
    'create_integration_test'
]

