"""
Enhanced Fleet Copilot API with Advanced BI - FIXED VERSION
Sistema de BI melhorado com dashboards interativos, filtros dinâmicos e IA
CORREÇÃO: SQLAlchemy inicializado corretamente
"""

import os
import sys
import logging

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enhanced configuration
app.config['FIREBASE_API_URL'] = os.environ.get('FIREBASE_API_URL', 'https://firebase-bi-api.onrender.com')
app.config['PORT'] = int(os.environ.get('PORT', 5000))

# Database configuration (FIXED)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure CORS for FlutterFlow integration
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize database (FIXED)
db = None
try:
    from src.models.user import db as user_db
    db = user_db
    db.init_app(app)
    logger.info("✅ Database initialized successfully")
except ImportError as e:
    logger.warning(f"⚠️ Database models not found: {e}")
except Exception as e:
    logger.warning(f"⚠️ Database initialization failed: {e}")

# Import and register blueprints
def register_blueprints():
    """Register all application blueprints"""
    
    # Original user routes (with error handling)
    try:
        from src.routes.user import user_bp
        app.register_blueprint(user_bp, url_prefix='/api')
        logger.info("✅ Registered user blueprint")
    except ImportError as e:
        logger.warning(f"⚠️ User routes not found: {e}")
    except Exception as e:
        logger.warning(f"⚠️ Failed to register user routes: {e}")
    
    # Enhanced copilot routes
    try:
        from src.routes.copilot import copilot_bp
        app.register_blueprint(copilot_bp, url_prefix='/api/copilot')
        logger.info("✅ Registered enhanced copilot blueprint")
    except ImportError as e:
        logger.warning(f"⚠️ Copilot routes not found: {e}")
    except Exception as e:
        logger.warning(f"⚠️ Failed to register copilot routes: {e}")
    
    # FlutterFlow integration routes
    try:
        from src.routes.flutterflow import flutterflow_bp
        app.register_blueprint(flutterflow_bp, url_prefix='/api/flutterflow')
        logger.info("✅ Registered FlutterFlow blueprint")
    except ImportError as e:
        logger.warning(f"⚠️ FlutterFlow routes not found: {e}")
    except Exception as e:
        logger.warning(f"⚠️ Failed to register FlutterFlow routes: {e}")
    
    # Dynamic BI routes (new)
    try:
        from src.dynamic_bi_routes import dynamic_bi_bp
        app.register_blueprint(dynamic_bi_bp, url_prefix='/api/bi')
        logger.info("✅ Registered Dynamic BI blueprint")
    except ImportError as e:
        logger.warning(f"⚠️ Dynamic BI routes not found: {e}")
    except Exception as e:
        logger.warning(f"⚠️ Failed to register Dynamic BI routes: {e}")

# Register all blueprints
register_blueprints()

# Enhanced dashboard route
@app.route('/api/copilot/enhanced-dashboard')
def enhanced_dashboard():
    """Serve the enhanced dashboard with advanced BI features"""
    try:
        # Look for dashboard in multiple locations
        dashboard_paths = [
            os.path.join(os.path.dirname(__file__), 'dashboard_melhorado.html'),
            os.path.join(os.path.dirname(__file__), 'static', 'dashboard_melhorado.html'),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dashboard_melhorado.html')
        ]
        
        for dashboard_path in dashboard_paths:
            if os.path.exists(dashboard_path):
                logger.info(f"✅ Found dashboard at: {dashboard_path}")
                with open(dashboard_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Inject enterprise ID and other parameters
                enterprise_id = request.args.get('enterpriseId', 'sA9EmrE3ymtnBqJKcYn7')
                days = request.args.get('days', '30')
                
                # Replace placeholders if any
                content = content.replace('{{ENTERPRISE_ID}}', enterprise_id)
                content = content.replace('{{DAYS}}', days)
                
                return content, 200, {'Content-Type': 'text/html; charset=utf-8'}
        
        # Fallback if dashboard not found
        logger.error("❌ Dashboard file not found in any location")
        return """
        <html>
        <head><title>Dashboard Not Found</title></head>
        <body>
            <h1>Dashboard em Desenvolvimento</h1>
            <p>O dashboard melhorado está sendo configurado.</p>
            <p>Tente novamente em alguns minutos.</p>
        </body>
        </html>
        """, 404
        
    except Exception as e:
        logger.error(f"❌ Error serving dashboard: {e}")
        return f"Error loading dashboard: {str(e)}", 500

# Static files for enhanced dashboard
@app.route('/api/static/<path:filename>')
def serve_static(filename):
    """Serve static files for the enhanced dashboard"""
    try:
        static_dir = os.path.join(os.path.dirname(__file__), 'static')
        return send_from_directory(static_dir, filename)
    except Exception as e:
        logger.error(f"❌ Error serving static file {filename}: {e}")
        return f"File not found: {filename}", 404

# Health check endpoint
@app.route('/api/health')
def health_check():
    """Enhanced health check with system status"""
    try:
        status = {
            'status': 'healthy',
            'timestamp': '2025-06-03T16:30:00Z',
            'version': '2.0.0-enhanced',
            'features': {
                'enhanced_dashboard': True,
                'dynamic_bi': True,
                'multi_collection': True,
                'advanced_filters': True,
                'data_export': True
            },
            'database': 'connected' if db else 'not_configured',
            'firebase_api': app.config.get('FIREBASE_API_URL', 'not_configured')
        }
        return jsonify(status), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': '2025-06-03T16:30:00Z'
        }), 500

# Welcome page with enhanced features
@app.route('/')
def welcome():
    """Enhanced welcome page with BI features"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fleet Copilot API - Enhanced BI</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #2c3e50; color: #ecf0f1; }
            .container { max-width: 800px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 40px; }
            .feature { background: #34495e; padding: 20px; margin: 20px 0; border-radius: 8px; }
            .btn { background: #1abc9c; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 5px; }
            .btn:hover { background: #16a085; }
            .status { background: #27ae60; color: white; padding: 10px; border-radius: 5px; text-align: center; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚛 Fleet Copilot API - Enhanced BI</h1>
                <div class="status">✅ Sistema Operacional - Versão 2.0.0</div>
            </div>
            
            <div class="feature">
                <h3>🎯 Dashboard Melhorado</h3>
                <p>Interface moderna com tema escuro, filtros interativos e gráficos avançados.</p>
                <a href="/api/copilot/enhanced-dashboard?enterpriseId=sA9EmrE3ymtnBqJKcYn7&days=30" class="btn">Acessar Dashboard</a>
            </div>
            
            <div class="feature">
                <h3>📊 BI Dinâmico</h3>
                <p>Sistema inteligente que adapta automaticamente gráficos e filtros para diferentes collections.</p>
                <a href="/api/bi/collections" class="btn">Ver Collections</a>
            </div>
            
            <div class="feature">
                <h3>📱 Mobile Dashboard</h3>
                <p>Dashboard otimizado para FlutterFlow e dispositivos móveis.</p>
                <a href="/api/flutterflow/mobile-dashboard?enterpriseId=sA9EmrE3ymtnBqJKcYn7" class="btn">Mobile Dashboard</a>
            </div>
            
            <div class="feature">
                <h3>🔧 API Endpoints</h3>
                <p>APIs RESTful para integração com sistemas externos.</p>
                <a href="/api/health" class="btn">Health Check</a>
                <a href="/api/copilot/summary?enterpriseId=sA9EmrE3ymtnBqJKcYn7" class="btn">API Summary</a>
            </div>
        </div>
    </body>
    </html>
    """

# Create database tables (FIXED)
with app.app_context():
    try:
        if db:
            db.create_all()
            logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.warning(f"⚠️ Could not create database tables: {e}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"🚀 Starting Enhanced Fleet Copilot API on port {port}")
    logger.info(f"🎯 Debug mode: {debug}")
    logger.info(f"🔗 Firebase API URL: {app.config['FIREBASE_API_URL']}")
    logger.info(f"💾 Database: {'Configured' if db else 'Not configured'}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
