/**
 * Sistema de IA Dinâmica para BI de Frotas
 * Detecta automaticamente collections e gera componentes apropriados
 */

class DynamicBISystem {
    constructor() {
        this.currentCollection = 'checklist';
        this.availableCollections = {};
        this.collectionConfigs = {};
        this.apiBaseUrl = window.location.origin + '/api';
        
        this.init();
    }
    
    async init() {
        await this.loadAvailableCollections();
        this.setupCollectionSelector();
        this.setupEventHandlers();
        
        // Load default collection
        await this.loadCollection(this.currentCollection);
    }
    
    async loadAvailableCollections() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/copilot/collections`);
            const data = await response.json();
            
            if (data.success) {
                this.availableCollections = data.data;
                this.setupCollectionConfigs();
            }
        } catch (error) {
            console.error('Error loading collections:', error);
            // Fallback to default collections
            this.setupDefaultCollections();
        }
    }
    
    setupDefaultCollections() {
        this.availableCollections = {
            checklist: {
                name: 'Checklist de Veículos',
                description: 'Inspeções e verificações de conformidade',
                icon: 'fas fa-clipboard-check',
                color: '#1abc9c'
            },
            trips: {
                name: 'Viagens',
                description: 'Histórico de viagens e rotas',
                icon: 'fas fa-route',
                color: '#3498db'
            },
            alerts: {
                name: 'Alertas',
                description: 'Alertas e notificações do sistema',
                icon: 'fas fa-exclamation-triangle',
                color: '#e74c3c'
            },
            maintenance: {
                name: 'Manutenção',
                description: 'Agendamentos e histórico de manutenção',
                icon: 'fas fa-tools',
                color: '#f39c12'
            },
            drivers: {
                name: 'Motoristas',
                description: 'Performance e dados dos motoristas',
                icon: 'fas fa-user-tie',
                color: '#9b59b6'
            },
            vehicles: {
                name: 'Veículos',
                description: 'Frota e informações dos veículos',
                icon: 'fas fa-truck',
                color: '#27ae60'
            }
        };
        
        this.setupCollectionConfigs();
    }
    
    setupCollectionConfigs() {
        this.collectionConfigs = {
            checklist: {
                metrics: [
                    { key: 'total_checks', label: 'Total de Verificações', icon: 'fas fa-clipboard-list' },
                    { key: 'compliance_rate', label: 'Taxa de Conformidade', icon: 'fas fa-check-circle', format: 'percentage' },
                    { key: 'non_compliant', label: 'Não Conformes', icon: 'fas fa-times-circle' },
                    { key: 'vehicles_checked', label: 'Veículos Verificados', icon: 'fas fa-truck' }
                ],
                charts: [
                    { type: 'doughnut', title: 'Conformidade vs Não Conformidade', dataKey: 'compliance_chart' },
                    { type: 'bar', title: 'Verificações por Veículo', dataKey: 'vehicle_checks' },
                    { type: 'line', title: 'Tendência de Conformidade', dataKey: 'compliance_trend' }
                ],
                filters: [
                    { key: 'vehiclePlate', label: 'Placa do Veículo', type: 'select' },
                    { key: 'driverName', label: 'Motorista', type: 'select' },
                    { key: 'itemName', label: 'Tipo de Item', type: 'select' },
                    { key: 'compliance', label: 'Status de Conformidade', type: 'select', options: [
                        { value: 'all', label: 'Todos' },
                        { value: 'compliant', label: 'Conforme' },
                        { value: 'non_compliant', label: 'Não Conforme' }
                    ]}
                ]
            },
            
            trips: {
                metrics: [
                    { key: 'total_trips', label: 'Total de Viagens', icon: 'fas fa-route' },
                    { key: 'total_distance', label: 'Distância Total', icon: 'fas fa-road', format: 'distance' },
                    { key: 'avg_speed', label: 'Velocidade Média', icon: 'fas fa-tachometer-alt', format: 'speed' },
                    { key: 'fuel_efficiency', label: 'Eficiência Combustível', icon: 'fas fa-gas-pump', format: 'fuel' }
                ],
                charts: [
                    { type: 'line', title: 'Viagens por Dia', dataKey: 'trips_timeline' },
                    { type: 'bar', title: 'Distância por Motorista', dataKey: 'driver_distances' },
                    { type: 'scatter', title: 'Velocidade vs Eficiência', dataKey: 'speed_efficiency' }
                ],
                filters: [
                    { key: 'vehiclePlate', label: 'Placa do Veículo', type: 'select' },
                    { key: 'driverName', label: 'Motorista', type: 'select' },
                    { key: 'origin', label: 'Origem', type: 'text' },
                    { key: 'destination', label: 'Destino', type: 'text' }
                ]
            },
            
            alerts: {
                metrics: [
                    { key: 'total_alerts', label: 'Total de Alertas', icon: 'fas fa-bell' },
                    { key: 'critical_alerts', label: 'Alertas Críticos', icon: 'fas fa-exclamation-triangle' },
                    { key: 'resolved_alerts', label: 'Alertas Resolvidos', icon: 'fas fa-check' },
                    { key: 'avg_resolution_time', label: 'Tempo Médio de Resolução', icon: 'fas fa-clock', format: 'time' }
                ],
                charts: [
                    { type: 'doughnut', title: 'Alertas por Severidade', dataKey: 'severity_distribution' },
                    { type: 'bar', title: 'Alertas por Tipo', dataKey: 'alert_types' },
                    { type: 'line', title: 'Tendência de Alertas', dataKey: 'alerts_timeline' }
                ],
                filters: [
                    { key: 'vehiclePlate', label: 'Placa do Veículo', type: 'select' },
                    { key: 'alertType', label: 'Tipo de Alerta', type: 'select' },
                    { key: 'severity', label: 'Severidade', type: 'select', options: [
                        { value: 'all', label: 'Todas' },
                        { value: 'low', label: 'Baixa' },
                        { value: 'medium', label: 'Média' },
                        { value: 'high', label: 'Alta' },
                        { value: 'critical', label: 'Crítica' }
                    ]},
                    { key: 'status', label: 'Status', type: 'select', options: [
                        { value: 'all', label: 'Todos' },
                        { value: 'active', label: 'Ativo' },
                        { value: 'resolved', label: 'Resolvido' }
                    ]}
                ]
            },
            
            maintenance: {
                metrics: [
                    { key: 'scheduled_maintenance', label: 'Manutenções Agendadas', icon: 'fas fa-calendar' },
                    { key: 'completed_maintenance', label: 'Manutenções Concluídas', icon: 'fas fa-check-circle' },
                    { key: 'overdue_maintenance', label: 'Manutenções Atrasadas', icon: 'fas fa-exclamation-circle' },
                    { key: 'total_cost', label: 'Custo Total', icon: 'fas fa-dollar-sign', format: 'currency' }
                ],
                charts: [
                    { type: 'bar', title: 'Manutenções por Mês', dataKey: 'maintenance_timeline' },
                    { type: 'doughnut', title: 'Tipos de Manutenção', dataKey: 'maintenance_types' },
                    { type: 'line', title: 'Custos de Manutenção', dataKey: 'cost_timeline' }
                ],
                filters: [
                    { key: 'vehiclePlate', label: 'Placa do Veículo', type: 'select' },
                    { key: 'maintenanceType', label: 'Tipo de Manutenção', type: 'select' },
                    { key: 'status', label: 'Status', type: 'select', options: [
                        { value: 'all', label: 'Todos' },
                        { value: 'scheduled', label: 'Agendada' },
                        { value: 'in_progress', label: 'Em Andamento' },
                        { value: 'completed', label: 'Concluída' },
                        { value: 'cancelled', label: 'Cancelada' }
                    ]},
                    { key: 'technician', label: 'Técnico', type: 'select' }
                ]
            },
            
            drivers: {
                metrics: [
                    { key: 'total_drivers', label: 'Total de Motoristas', icon: 'fas fa-users' },
                    { key: 'active_drivers', label: 'Motoristas Ativos', icon: 'fas fa-user-check' },
                    { key: 'avg_score', label: 'Score Médio', icon: 'fas fa-star', format: 'score' },
                    { key: 'violations', label: 'Violações', icon: 'fas fa-exclamation-triangle' }
                ],
                charts: [
                    { type: 'bar', title: 'Score por Motorista', dataKey: 'driver_scores' },
                    { type: 'line', title: 'Evolução dos Scores', dataKey: 'score_evolution' },
                    { type: 'radar', title: 'Performance Geral', dataKey: 'performance_radar' }
                ],
                filters: [
                    { key: 'driverName', label: 'Nome do Motorista', type: 'select' },
                    { key: 'status', label: 'Status', type: 'select', options: [
                        { value: 'all', label: 'Todos' },
                        { value: 'active', label: 'Ativo' },
                        { value: 'inactive', label: 'Inativo' }
                    ]},
                    { key: 'scoreRange', label: 'Faixa de Score', type: 'select', options: [
                        { value: 'all', label: 'Todos' },
                        { value: 'excellent', label: 'Excelente (90-100)' },
                        { value: 'good', label: 'Bom (70-89)' },
                        { value: 'average', label: 'Médio (50-69)' },
                        { value: 'poor', label: 'Ruim (0-49)' }
                    ]}
                ]
            },
            
            vehicles: {
                metrics: [
                    { key: 'total_vehicles', label: 'Total de Veículos', icon: 'fas fa-truck' },
                    { key: 'active_vehicles', label: 'Veículos Ativos', icon: 'fas fa-check-circle' },
                    { key: 'avg_mileage', label: 'Quilometragem Média', icon: 'fas fa-road', format: 'distance' },
                    { key: 'maintenance_due', label: 'Manutenção Pendente', icon: 'fas fa-wrench' }
                ],
                charts: [
                    { type: 'doughnut', title: 'Status dos Veículos', dataKey: 'vehicle_status' },
                    { type: 'bar', title: 'Quilometragem por Veículo', dataKey: 'vehicle_mileage' },
                    { type: 'line', title: 'Utilização Mensal', dataKey: 'usage_timeline' }
                ],
                filters: [
                    { key: 'vehiclePlate', label: 'Placa do Veículo', type: 'select' },
                    { key: 'vehicleType', label: 'Tipo de Veículo', type: 'select' },
                    { key: 'status', label: 'Status', type: 'select', options: [
                        { value: 'all', label: 'Todos' },
                        { value: 'active', label: 'Ativo' },
                        { value: 'inactive', label: 'Inativo' },
                        { value: 'maintenance', label: 'Em Manutenção' }
                    ]},
                    { key: 'year', label: 'Ano', type: 'select' }
                ]
            }
        };
    }
    
    setupCollectionSelector() {
        const selectorHTML = `
            <div class="collection-selector mb-4">
                <div class="row">
                    <div class="col-md-6">
                        <label for="collectionSelect" class="form-label">
                            <i class="fas fa-database"></i> Selecionar Análise
                        </label>
                        <select id="collectionSelect" class="form-select">
                            ${Object.entries(this.availableCollections).map(([key, config]) => 
                                `<option value="${key}" ${key === this.currentCollection ? 'selected' : ''}>
                                    ${config.name}
                                </option>`
                            ).join('')}
                        </select>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label">
                            <i class="fas fa-info-circle"></i> Descrição
                        </label>
                        <p id="collectionDescription" class="form-text">
                            ${this.availableCollections[this.currentCollection]?.description || ''}
                        </p>
                    </div>
                </div>
                
                <div class="collection-cards mt-3">
                    <div class="row">
                        ${Object.entries(this.availableCollections).map(([key, config]) => 
                            `<div class="col-md-2 mb-3">
                                <div class="collection-card ${key === this.currentCollection ? 'active' : ''}" 
                                     data-collection="${key}" 
                                     style="border-color: ${config.color};">
                                    <div class="card-icon" style="color: ${config.color};">
                                        <i class="${config.icon}"></i>
                                    </div>
                                    <div class="card-title">${config.name}</div>
                                </div>
                            </div>`
                        ).join('')}
                    </div>
                </div>
            </div>
        `;
        
        document.getElementById('collectionSelector').innerHTML = selectorHTML;
        
        // Add CSS for collection cards
        this.addCollectionSelectorStyles();
    }
    
    addCollectionSelectorStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .collection-selector {
                background: #34495e;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 20px;
            }
            
            .collection-card {
                background: #2c3e50;
                border: 2px solid #34495e;
                border-radius: 8px;
                padding: 15px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                height: 100px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            
            .collection-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            
            .collection-card.active {
                background: #1abc9c;
                color: white;
            }
            
            .collection-card .card-icon {
                font-size: 24px;
                margin-bottom: 8px;
            }
            
            .collection-card .card-title {
                font-size: 12px;
                font-weight: 500;
            }
            
            .collection-card.active .card-icon {
                color: white !important;
            }
            
            #collectionSelect {
                background: #2c3e50;
                border: 1px solid #1abc9c;
                color: #ecf0f1;
            }
            
            #collectionSelect:focus {
                background: #2c3e50;
                border-color: #16a085;
                color: #ecf0f1;
                box-shadow: 0 0 0 0.2rem rgba(26, 188, 156, 0.25);
            }
            
            #collectionDescription {
                color: #bdc3c7;
                font-style: italic;
            }
        `;
        document.head.appendChild(style);
    }
    
    setupEventHandlers() {
        // Collection selector change
        document.getElementById('collectionSelect').addEventListener('change', (e) => {
            this.changeCollection(e.target.value);
        });
        
        // Collection card clicks
        document.addEventListener('click', (e) => {
            if (e.target.closest('.collection-card')) {
                const collection = e.target.closest('.collection-card').dataset.collection;
                this.changeCollection(collection);
            }
        });
    }
    
    async changeCollection(collection) {
        if (collection === this.currentCollection) return;
        
        // Update UI
        this.updateCollectionSelector(collection);
        
        // Load new collection data
        await this.loadCollection(collection);
        
        this.currentCollection = collection;
    }
    
    updateCollectionSelector(collection) {
        // Update select
        document.getElementById('collectionSelect').value = collection;
        
        // Update description
        document.getElementById('collectionDescription').textContent = 
            this.availableCollections[collection]?.description || '';
        
        // Update active card
        document.querySelectorAll('.collection-card').forEach(card => {
            card.classList.remove('active');
        });
        document.querySelector(`[data-collection="${collection}"]`).classList.add('active');
    }
    
    async loadCollection(collection) {
        try {
            // Show loading
            this.showLoading();
            
            // Load data
            const data = await this.fetchCollectionData(collection);
            
            // Generate components
            await this.generateComponents(collection, data);
            
            // Hide loading
            this.hideLoading();
            
        } catch (error) {
            console.error('Error loading collection:', error);
            this.showError('Erro ao carregar dados da collection');
        }
    }
    
    async fetchCollectionData(collection) {
        const enterpriseId = new URLSearchParams(window.location.search).get('enterpriseId') || 'sA9EmrE3ymtnBqJKcYn7';
        const days = new URLSearchParams(window.location.search).get('days') || '30';
        
        const endpoints = {
            checklist: `/copilot/summary?enterpriseId=${enterpriseId}&days=${days}`,
            trips: `/copilot/trips?enterpriseId=${enterpriseId}&days=${days}`,
            alerts: `/copilot/alerts?enterpriseId=${enterpriseId}&days=${days}`,
            maintenance: `/copilot/maintenance?enterpriseId=${enterpriseId}&days=${days}`,
            drivers: `/copilot/drivers?enterpriseId=${enterpriseId}&days=${days}`,
            vehicles: `/copilot/vehicles?enterpriseId=${enterpriseId}&days=${days}`
        };
        
        const endpoint = endpoints[collection] || endpoints.checklist;
        const response = await fetch(`${this.apiBaseUrl}${endpoint}`);
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.message || 'Erro ao buscar dados');
        }
        
        return result.data;
    }
    
    async generateComponents(collection, data) {
        const config = this.collectionConfigs[collection];
        if (!config) return;
        
        // Generate metrics cards
        this.generateMetricsCards(config.metrics, data);
        
        // Generate filters
        this.generateFilters(config.filters, data);
        
        // Generate charts
        await this.generateCharts(config.charts, data);
        
        // Generate data table
        this.generateDataTable(collection, data);
        
        // Generate insights
        this.generateInsights(collection, data);
    }
    
    generateMetricsCards(metrics, data) {
        const metricsHTML = metrics.map(metric => {
            const value = this.formatMetricValue(data[metric.key], metric.format);
            const color = this.getMetricColor(metric.key, data[metric.key]);
            
            return `
                <div class="col-md-3 mb-3">
                    <div class="metric-card" style="border-left-color: ${color};">
                        <div class="metric-icon" style="color: ${color};">
                            <i class="${metric.icon}"></i>
                        </div>
                        <div class="metric-content">
                            <div class="metric-value">${value}</div>
                            <div class="metric-label">${metric.label}</div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
        
        document.getElementById('metricsContainer').innerHTML = `
            <div class="row">
                ${metricsHTML}
            </div>
        `;
    }
    
    generateFilters(filters, data) {
        if (!window.filterManager) return;
        
        // Clear existing filters
        window.filterManager.clearFilters();
        
        // Add collection-specific filters
        filters.forEach(filter => {
            if (filter.options) {
                // Static options
                window.filterManager.addFilter(filter.key, filter.label, filter.type, filter.options);
            } else {
                // Dynamic options from data
                const options = this.extractFilterOptions(filter.key, data);
                window.filterManager.addFilter(filter.key, filter.label, filter.type, options);
            }
        });
        
        // Render filters
        window.filterManager.renderFilters();
    }
    
    extractFilterOptions(filterKey, data) {
        if (!data.raw_data || !Array.isArray(data.raw_data)) return [];
        
        const uniqueValues = [...new Set(
            data.raw_data
                .map(item => item[filterKey])
                .filter(value => value && value !== '')
        )].sort();
        
        return [
            { value: 'all', label: 'Todos' },
            ...uniqueValues.map(value => ({ value, label: value }))
        ];
    }
    
    async generateCharts(charts, data) {
        if (!window.chartManager) return;
        
        // Clear existing charts
        window.chartManager.destroyAllCharts();
        
        // Generate new charts
        for (const chartConfig of charts) {
            const chartData = this.prepareChartData(chartConfig, data);
            await window.chartManager.createChart(
                chartConfig.type,
                chartConfig.title,
                chartData,
                `chart_${chartConfig.dataKey}`
            );
        }
    }
    
    prepareChartData(chartConfig, data) {
        // This would be implemented based on the specific chart type and data structure
        // For now, return sample data
        return {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            datasets: [{
                label: chartConfig.title,
                data: [12, 19, 3, 5, 2],
                backgroundColor: ['#1abc9c', '#3498db', '#9b59b6', '#e74c3c', '#f39c12']
            }]
        };
    }
    
    generateDataTable(collection, data) {
        if (!window.dataTableManager || !data.raw_data) return;
        
        window.dataTableManager.createTable('dataTable', collection, data.raw_data);
    }
    
    generateInsights(collection, data) {
        const insights = this.generateAIInsights(collection, data);
        
        const insightsHTML = insights.map(insight => `
            <div class="insight-card ${insight.type}">
                <div class="insight-icon">
                    <i class="${insight.icon}"></i>
                </div>
                <div class="insight-content">
                    <h6>${insight.title}</h6>
                    <p>${insight.message}</p>
                </div>
            </div>
        `).join('');
        
        document.getElementById('insightsContainer').innerHTML = insightsHTML;
    }
    
    generateAIInsights(collection, data) {
        // AI-powered insights generation based on collection and data
        const insights = [];
        
        switch (collection) {
            case 'checklist':
                if (data.compliance_rate < 80) {
                    insights.push({
                        type: 'warning',
                        icon: 'fas fa-exclamation-triangle',
                        title: 'Taxa de Conformidade Baixa',
                        message: `A taxa de conformidade está em ${data.compliance_rate}%, abaixo do ideal de 80%.`
                    });
                }
                break;
                
            case 'trips':
                if (data.avg_speed > 80) {
                    insights.push({
                        type: 'danger',
                        icon: 'fas fa-tachometer-alt',
                        title: 'Velocidade Média Alta',
                        message: `A velocidade média de ${data.avg_speed} km/h pode indicar direção agressiva.`
                    });
                }
                break;
                
            case 'alerts':
                if (data.critical_alerts > 0) {
                    insights.push({
                        type: 'danger',
                        icon: 'fas fa-bell',
                        title: 'Alertas Críticos Ativos',
                        message: `Existem ${data.critical_alerts} alertas críticos que requerem atenção imediata.`
                    });
                }
                break;
        }
        
        return insights;
    }
    
    formatMetricValue(value, format) {
        if (value === null || value === undefined) return 'N/A';
        
        switch (format) {
            case 'percentage':
                return `${value.toFixed(1)}%`;
            case 'currency':
                return `R$ ${value.toLocaleString()}`;
            case 'distance':
                return `${value.toLocaleString()} km`;
            case 'speed':
                return `${value} km/h`;
            case 'fuel':
                return `${value} km/l`;
            case 'time':
                return `${value} min`;
            case 'score':
                return `${value}/100`;
            default:
                return value.toLocaleString();
        }
    }
    
    getMetricColor(key, value) {
        // Return color based on metric type and value
        const colorMap = {
            compliance_rate: value >= 80 ? '#27ae60' : value >= 60 ? '#f39c12' : '#e74c3c',
            critical_alerts: value > 0 ? '#e74c3c' : '#27ae60',
            avg_score: value >= 80 ? '#27ae60' : value >= 60 ? '#f39c12' : '#e74c3c'
        };
        
        return colorMap[key] || '#1abc9c';
    }
    
    showLoading() {
        document.getElementById('loadingOverlay').style.display = 'flex';
    }
    
    hideLoading() {
        document.getElementById('loadingOverlay').style.display = 'none';
    }
    
    showError(message) {
        // Show error message
        console.error(message);
        // You could implement a toast notification here
    }
    
    // Export functionality
    exportCurrentView(format = 'excel') {
        const data = {
            collection: this.currentCollection,
            metrics: this.getCurrentMetrics(),
            filters: window.filterManager?.getCurrentFilters() || {},
            timestamp: new Date().toISOString()
        };
        
        switch (format) {
            case 'excel':
                this.exportToExcel(data);
                break;
            case 'pdf':
                this.exportToPDF(data);
                break;
            case 'json':
                this.exportToJSON(data);
                break;
        }
    }
    
    getCurrentMetrics() {
        const metrics = {};
        document.querySelectorAll('.metric-card').forEach(card => {
            const label = card.querySelector('.metric-label').textContent;
            const value = card.querySelector('.metric-value').textContent;
            metrics[label] = value;
        });
        return metrics;
    }
    
    exportToExcel(data) {
        // Use DataTable export functionality
        if (window.dataTableManager) {
            window.dataTableManager.exportTable('dataTable', 'excel');
        }
    }
    
    exportToPDF(data) {
        // Use DataTable export functionality
        if (window.dataTableManager) {
            window.dataTableManager.exportTable('dataTable', 'pdf');
        }
    }
    
    exportToJSON(data) {
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `bi-${this.currentCollection}-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }
}

// Global instance
let dynamicBISystem;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    dynamicBISystem = new DynamicBISystem();
});

// Global functions
function changeCollection(collection) {
    if (dynamicBISystem) {
        dynamicBISystem.changeCollection(collection);
    }
}

function exportCurrentView(format = 'excel') {
    if (dynamicBISystem) {
        dynamicBISystem.exportCurrentView(format);
    }
}

