# Fleet Copilot BI - Enterprise Edition

Business Intelligence platform for fleet management with enterprise-grade design and real-time data visualization.

## 🚀 Features

### ✅ Available BIs:
- **⛽ Fuel BI**: Comprehensive fuel consumption and cost analysis with real-time data
- **✅ Checklist BI**: Vehicle inspection and compliance monitoring (coming soon)
- **🚗 Trips BI**: Route optimization and travel analytics (coming soon)
- **🔧 Maintenance BI**: Predictive maintenance and service tracking (coming soon)
- **👨‍💼 Drivers BI**: Driver performance and behavior analysis (coming soon)
- **💰 Financial BI**: Complete financial analysis with cost control and ROI (coming soon)

### 🎨 Enterprise Design:
- **Dark theme** with professional black background
- **SVG icons** - Clean, professional, no emojis
- **Teal/Cyan accent** color scheme (#14b8a6)
- **Responsive layout** optimized for desktop and mobile
- **Smooth animations** and hover effects

## 🔗 URL Structure

### Main Routes:
- `/` - Redirects to BI menu
- `/api/copilot/dashboard` - Main BI selection menu
- `/api/copilot/enhanced-dashboard` - Legacy compatibility (redirects)
- `/health` - Health check endpoint
- `/api/copilot/bis` - JSON API listing available BIs

### BI Routes:
- `/api/copilot/bi-combustivel` - Fuel BI (functional)
- `/api/copilot/bi-checklist` - Checklist BI (placeholder)
- `/api/copilot/bi-viagens` - Trips BI (placeholder)
- `/api/copilot/bi-manutencao` - Maintenance BI (placeholder)
- `/api/copilot/bi-motoristas` - Drivers BI (placeholder)
- `/api/copilot/bi-financeiro` - Financial BI (placeholder)

## 🛠️ Tech Stack

- **Backend**: Flask (Python 3.11)
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js with dark theme
- **Data Source**: Firebase API
- **Hosting**: Render.com
- **Design**: Enterprise dark theme with SVG icons

## 🔧 Configuration

### Environment Variables:
```
FLASK_ENV=production
PORT=10000
```

### Dependencies:
- Flask 2.3.3
- Gunicorn 21.2.0
- Jinja2 3.1.2

## 📊 Data Integration

### Firebase Collections:
- `alelo-supply-history` - Fuel consumption data
- `Checklist` - Vehicle inspection records
- `vehicles` - Fleet vehicle information
- `drivers` - Driver profiles and performance

### Enterprise Support:
All BIs support enterprise-specific filtering via `enterpriseId` parameter:
```
/api/copilot/bi-combustivel?enterpriseId=YOUR_ENTERPRISE_ID
```

## 🚀 Deployment

### Render.com Configuration:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 app:app`
- **Python Version**: 3.11.0
- **Auto-Deploy**: Enabled
- **Health Check**: `/health`

### File Structure:
```
project/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── runtime.txt              # Python version
├── Procfile                 # Render configuration
└── templates/               # HTML templates
    ├── dashboard_menu.html  # Main BI menu
    ├── bi_combustivel.html  # Fuel BI (functional)
    └── bi_*.html           # Other BIs (placeholders)
```

## 📈 Features by BI

### ⛽ Fuel BI (Functional):
- **Real-time metrics**: Total supplies, liters, costs, efficiency
- **Interactive charts**: Cost per km, driver efficiency, state distribution
- **Smart insights**: AI-generated analysis and recommendations
- **Advanced filters**: Date range, vehicle, driver, fuel type, state
- **Export options**: Excel and PDF reports
- **Responsive tables**: Paginated data with search and sort

### 🚧 Other BIs (Coming Soon):
- Professional placeholder pages with enterprise design
- Navigation back to main menu
- Consistent visual identity
- Ready for implementation

## 🎯 Enterprise Features

### 🔒 Security:
- Enterprise ID-based data filtering
- Health check monitoring
- Production-ready configuration

### 📱 User Experience:
- Intuitive navigation between BIs
- Consistent enterprise design language
- Mobile-responsive interface
- Fast loading with optimized assets

### 📊 Analytics:
- Real-time data visualization
- Interactive charts and graphs
- Automated insights generation
- Comprehensive reporting tools

## 🔄 Legacy Compatibility

Maintains full compatibility with existing URLs:
- `/api/copilot/enhanced-dashboard` automatically redirects to new menu
- All enterprise IDs continue to work seamlessly
- No breaking changes for existing users

## 📞 Support

For technical support or feature requests, refer to the deployment logs in Render.com dashboard or check the health endpoint at `/health`.

---

**Fleet Copilot BI - Powering intelligent fleet management with enterprise-grade analytics.**

