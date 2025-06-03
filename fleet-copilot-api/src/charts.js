/**
 * Sistema de Gráficos Avançados para BI de Frotas
 * Gerencia visualizações dinâmicas com Chart.js
 */

class ChartManager {
    constructor() {
        this.charts = {};
        this.colors = {
            primary: '#1abc9c',
            secondary: '#16a085',
            purple: '#9b59b6',
            purpleSecondary: '#8e44ad',
            success: '#27ae60',
            warning: '#f39c12',
            danger: '#e74c3c',
            info: '#3498db',
            light: '#ecf0f1',
            dark: '#2c3e50',
            muted: '#bdc3c7'
        };
        
        this.gradients = {};
        this.chartConfigs = {};
        
        this.init();
    }
    
    init() {
        // Set Chart.js defaults
        Chart.defaults.color = this.colors.light;
        Chart.defaults.borderColor = '#34495e';
        Chart.defaults.backgroundColor = 'rgba(26, 188, 156, 0.1)';
        
        // Register custom plugins
        this.registerCustomPlugins();
    }
    
    registerCustomPlugins() {
        // Custom plugin for gradient backgrounds
        Chart.register({
            id: 'gradientBg',
            beforeDraw: (chart) => {
                if (chart.config.options.plugins?.gradientBg) {
                    const ctx = chart.ctx;
                    const chartArea = chart.chartArea;
                    
                    const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
                    gradient.addColorStop(0, 'rgba(26, 188, 156, 0.1)');
                    gradient.addColorStop(1, 'rgba(26, 188, 156, 0.01)');
                    
                    ctx.fillStyle = gradient;
                    ctx.fillRect(chartArea.left, chartArea.top, chartArea.right - chartArea.left, chartArea.bottom - chartArea.top);
                }
            }
        });
    }
    
    createGradient(ctx, color1, color2, direction = 'vertical') {
        let gradient;
        
        if (direction === 'vertical') {
            gradient = ctx.createLinearGradient(0, 0, 0, 400);
        } else {
            gradient = ctx.createLinearGradient(0, 0, 400, 0);
        }
        
        gradient.addColorStop(0, color1);
        gradient.addColorStop(1, color2);
        
        return gradient;
    }
    
    getChartConfig(type, collection) {
        const configs = {
            checklist: {
                compliance: this.getComplianceChartConfig(),
                evolution: this.getEvolutionChartConfig(),
                itemTypes: this.getItemTypesChartConfig(),
                vehicleStatus: this.getVehicleStatusChartConfig()
            },
            trips: {
                distance: this.getDistanceChartConfig(),
                speed: this.getSpeedChartConfig(),
                routes: this.getRoutesChartConfig(),
                efficiency: this.getEfficiencyChartConfig()
            },
            alerts: {
                severity: this.getSeverityChartConfig(),
                types: this.getAlertTypesChartConfig(),
                timeline: this.getTimelineChartConfig(),
                distribution: this.getDistributionChartConfig()
            },
            maintenance: {
                schedule: this.getScheduleChartConfig(),
                costs: this.getCostsChartConfig(),
                types: this.getMaintenanceTypesChartConfig(),
                performance: this.getPerformanceChartConfig()
            }
        };
        
        return configs[collection]?.[type] || this.getDefaultChartConfig();
    }
    
    // Checklist Charts
    getComplianceChartConfig() {
        return {
            type: 'doughnut',
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: this.colors.light,
                            padding: 20,
                            usePointStyle: true,
                            font: {
                                size: 12,
                                weight: '500'
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: this.colors.dark,
                        titleColor: this.colors.light,
                        bodyColor: this.colors.light,
                        borderColor: this.colors.primary,
                        borderWidth: 1,
                        cornerRadius: 8,
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed * 100) / total).toFixed(1);
                                return `${context.label}: ${context.parsed} (${percentage}%)`;
                            }
                        }
                    }
                },
                cutout: '60%',
                elements: {
                    arc: {
                        borderWidth: 0
                    }
                }
            }
        };
    }
    
    getEvolutionChartConfig() {
        return {
            type: 'line',
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        labels: {
                            color: this.colors.light,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        backgroundColor: this.colors.dark,
                        titleColor: this.colors.light,
                        bodyColor: this.colors.light,
                        borderColor: this.colors.primary,
                        borderWidth: 1,
                        cornerRadius: 8
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: this.colors.muted
                        },
                        grid: {
                            color: '#34495e',
                            drawBorder: false
                        }
                    },
                    y: {
                        ticks: {
                            color: this.colors.muted,
                            callback: function(value) {
                                return value + '%';
                            }
                        },
                        grid: {
                            color: '#34495e',
                            drawBorder: false
                        },
                        beginAtZero: true,
                        max: 100
                    }
                },
                elements: {
                    line: {
                        tension: 0.4,
                        borderWidth: 3
                    },
                    point: {
                        radius: 6,
                        hoverRadius: 8,
                        borderWidth: 2
                    }
                }
            }
        };
    }
    
    getItemTypesChartConfig() {
        return {
            type: 'bar',
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: this.colors.dark,
                        titleColor: this.colors.light,
                        bodyColor: this.colors.light,
                        borderColor: this.colors.primary,
                        borderWidth: 1,
                        cornerRadius: 8
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: this.colors.muted,
                            maxRotation: 45
                        },
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        ticks: {
                            color: this.colors.muted
                        },
                        grid: {
                            color: '#34495e',
                            drawBorder: false
                        },
                        beginAtZero: true
                    }
                },
                elements: {
                    bar: {
                        borderRadius: 4,
                        borderSkipped: false
                    }
                }
            }
        };
    }
    
    getVehicleStatusChartConfig() {
        return {
            type: 'polarArea',
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: this.colors.light,
                            padding: 15,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        backgroundColor: this.colors.dark,
                        titleColor: this.colors.light,
                        bodyColor: this.colors.light,
                        borderColor: this.colors.primary,
                        borderWidth: 1,
                        cornerRadius: 8
                    }
                },
                scales: {
                    r: {
                        ticks: {
                            color: this.colors.muted,
                            backdropColor: 'transparent'
                        },
                        grid: {
                            color: '#34495e'
                        },
                        angleLines: {
                            color: '#34495e'
                        }
                    }
                }
            }
        };
    }
    
    // Trips Charts
    getDistanceChartConfig() {
        return {
            type: 'bar',
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: this.colors.light
                        }
                    },
                    tooltip: {
                        backgroundColor: this.colors.dark,
                        titleColor: this.colors.light,
                        bodyColor: this.colors.light,
                        borderColor: this.colors.primary,
                        borderWidth: 1,
                        cornerRadius: 8,
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: ${context.parsed.y.toLocaleString()} km`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: this.colors.muted
                        },
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        ticks: {
                            color: this.colors.muted,
                            callback: function(value) {
                                return value.toLocaleString() + ' km';
                            }
                        },
                        grid: {
                            color: '#34495e',
                            drawBorder: false
                        },
                        beginAtZero: true
                    }
                }
            }
        };
    }
    
    getSpeedChartConfig() {
        return {
            type: 'radar',
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: this.colors.light,
                            padding: 15
                        }
                    },
                    tooltip: {
                        backgroundColor: this.colors.dark,
                        titleColor: this.colors.light,
                        bodyColor: this.colors.light,
                        borderColor: this.colors.primary,
                        borderWidth: 1,
                        cornerRadius: 8
                    }
                },
                scales: {
                    r: {
                        ticks: {
                            color: this.colors.muted,
                            backdropColor: 'transparent'
                        },
                        grid: {
                            color: '#34495e'
                        },
                        angleLines: {
                            color: '#34495e'
                        },
                        pointLabels: {
                            color: this.colors.light
                        }
                    }
                }
            }
        };
    }
    
    // Alert Charts
    getSeverityChartConfig() {
        return {
            type: 'doughnut',
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            color: this.colors.light,
                            padding: 20,
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        backgroundColor: this.colors.dark,
                        titleColor: this.colors.light,
                        bodyColor: this.colors.light,
                        borderColor: this.colors.primary,
                        borderWidth: 1,
                        cornerRadius: 8
                    }
                },
                cutout: '50%'
            }
        };
    }
    
    getTimelineChartConfig() {
        return {
            type: 'line',
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        labels: {
                            color: this.colors.light
                        }
                    },
                    tooltip: {
                        backgroundColor: this.colors.dark,
                        titleColor: this.colors.light,
                        bodyColor: this.colors.light,
                        borderColor: this.colors.primary,
                        borderWidth: 1,
                        cornerRadius: 8
                    }
                },
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day'
                        },
                        ticks: {
                            color: this.colors.muted
                        },
                        grid: {
                            color: '#34495e',
                            drawBorder: false
                        }
                    },
                    y: {
                        ticks: {
                            color: this.colors.muted
                        },
                        grid: {
                            color: '#34495e',
                            drawBorder: false
                        },
                        beginAtZero: true
                    }
                }
            }
        };
    }
    
    // Maintenance Charts
    getScheduleChartConfig() {
        return {
            type: 'bar',
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        labels: {
                            color: this.colors.light
                        }
                    },
                    tooltip: {
                        backgroundColor: this.colors.dark,
                        titleColor: this.colors.light,
                        bodyColor: this.colors.light,
                        borderColor: this.colors.primary,
                        borderWidth: 1,
                        cornerRadius: 8
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: this.colors.muted
                        },
                        grid: {
                            color: '#34495e',
                            drawBorder: false
                        },
                        beginAtZero: true
                    },
                    y: {
                        ticks: {
                            color: this.colors.muted
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        };
    }
    
    getCostsChartConfig() {
        return {
            type: 'line',
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: this.colors.light
                        }
                    },
                    tooltip: {
                        backgroundColor: this.colors.dark,
                        titleColor: this.colors.light,
                        bodyColor: this.colors.light,
                        borderColor: this.colors.primary,
                        borderWidth: 1,
                        cornerRadius: 8,
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: R$ ${context.parsed.y.toLocaleString()}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: this.colors.muted
                        },
                        grid: {
                            color: '#34495e',
                            drawBorder: false
                        }
                    },
                    y: {
                        ticks: {
                            color: this.colors.muted,
                            callback: function(value) {
                                return 'R$ ' + value.toLocaleString();
                            }
                        },
                        grid: {
                            color: '#34495e',
                            drawBorder: false
                        },
                        beginAtZero: true
                    }
                }
            }
        };
    }
    
    getDefaultChartConfig() {
        return {
            type: 'bar',
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: this.colors.light
                        }
                    }
                }
            }
        };
    }
    
    createChart(canvasId, type, data, collection = 'checklist') {
        const canvas = document.getElementById(canvasId);
        if (!canvas) {
            console.error(`Canvas with id '${canvasId}' not found`);
            return null;
        }
        
        // Destroy existing chart if exists
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }
        
        const ctx = canvas.getContext('2d');
        const config = this.getChartConfig(type, collection);
        
        // Apply data
        config.data = this.processChartData(data, type, ctx);
        
        // Create chart
        this.charts[canvasId] = new Chart(ctx, config);
        
        return this.charts[canvasId];
    }
    
    processChartData(data, type, ctx) {
        switch(type) {
            case 'compliance':
                return this.processComplianceData(data, ctx);
            case 'evolution':
                return this.processEvolutionData(data, ctx);
            case 'itemTypes':
                return this.processItemTypesData(data, ctx);
            case 'vehicleStatus':
                return this.processVehicleStatusData(data, ctx);
            case 'distance':
                return this.processDistanceData(data, ctx);
            case 'speed':
                return this.processSpeedData(data, ctx);
            case 'severity':
                return this.processSeverityData(data, ctx);
            case 'timeline':
                return this.processTimelineData(data, ctx);
            case 'schedule':
                return this.processScheduleData(data, ctx);
            case 'costs':
                return this.processCostsData(data, ctx);
            default:
                return this.processDefaultData(data, ctx);
        }
    }
    
    processComplianceData(data, ctx) {
        const compliant = data.compliantChecks || 0;
        const nonCompliant = data.nonCompliantChecks || 0;
        
        return {
            labels: ['Conforme', 'Não Conforme'],
            datasets: [{
                data: [compliant, nonCompliant],
                backgroundColor: [
                    this.colors.primary,
                    this.colors.danger
                ],
                borderWidth: 0,
                hoverOffset: 10
            }]
        };
    }
    
    processEvolutionData(data, ctx) {
        // Sample evolution data - would come from API
        const months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'];
        const complianceData = [85, 88, 92, 87, 90, data.complianceRate || 0];
        
        const gradient = this.createGradient(ctx, 
            'rgba(26, 188, 156, 0.8)', 
            'rgba(26, 188, 156, 0.1)'
        );
        
        return {
            labels: months,
            datasets: [{
                label: 'Taxa de Conformidade (%)',
                data: complianceData,
                borderColor: this.colors.primary,
                backgroundColor: gradient,
                borderWidth: 3,
                fill: true,
                pointBackgroundColor: this.colors.primary,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8
            }]
        };
    }
    
    processItemTypesData(data, ctx) {
        // Sample item types data
        const itemTypes = ['Farol', 'Pneu', 'Freio', 'Motor', 'Bateria'];
        const counts = [15, 23, 8, 12, 18];
        
        const colors = [
            this.colors.primary,
            this.colors.purple,
            this.colors.info,
            this.colors.warning,
            this.colors.success
        ];
        
        return {
            labels: itemTypes,
            datasets: [{
                label: 'Verificações',
                data: counts,
                backgroundColor: colors,
                borderWidth: 0,
                borderRadius: 4,
                borderSkipped: false
            }]
        };
    }
    
    processVehicleStatusData(data, ctx) {
        // Sample vehicle status data
        const statuses = ['Ativo', 'Manutenção', 'Inativo', 'Alerta'];
        const counts = [45, 8, 3, 12];
        
        const colors = [
            this.colors.success,
            this.colors.warning,
            this.colors.muted,
            this.colors.danger
        ];
        
        return {
            labels: statuses,
            datasets: [{
                data: counts,
                backgroundColor: colors,
                borderWidth: 0
            }]
        };
    }
    
    processDistanceData(data, ctx) {
        // Sample distance data
        const vehicles = ['ABC-1234', 'DEF-5678', 'GHI-9012', 'JKL-3456'];
        const distances = [1250, 980, 1450, 1100];
        
        const gradient = this.createGradient(ctx, 
            'rgba(26, 188, 156, 0.8)', 
            'rgba(26, 188, 156, 0.3)'
        );
        
        return {
            labels: vehicles,
            datasets: [{
                label: 'Distância (km)',
                data: distances,
                backgroundColor: gradient,
                borderColor: this.colors.primary,
                borderWidth: 2,
                borderRadius: 4,
                borderSkipped: false
            }]
        };
    }
    
    processSpeedData(data, ctx) {
        // Sample speed data for radar chart
        const metrics = ['Vel. Média', 'Vel. Máxima', 'Aceleração', 'Frenagem', 'Curvas'];
        const values = [75, 85, 60, 80, 70];
        
        return {
            labels: metrics,
            datasets: [{
                label: 'Performance',
                data: values,
                borderColor: this.colors.primary,
                backgroundColor: 'rgba(26, 188, 156, 0.2)',
                borderWidth: 2,
                pointBackgroundColor: this.colors.primary,
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        };
    }
    
    processSeverityData(data, ctx) {
        const severities = ['Crítico', 'Alto', 'Médio', 'Baixo'];
        const counts = [5, 12, 18, 8];
        
        const colors = [
            this.colors.danger,
            this.colors.warning,
            this.colors.info,
            this.colors.success
        ];
        
        return {
            labels: severities,
            datasets: [{
                data: counts,
                backgroundColor: colors,
                borderWidth: 0,
                hoverOffset: 10
            }]
        };
    }
    
    processTimelineData(data, ctx) {
        // Sample timeline data
        const dates = ['01/06', '02/06', '03/06', '04/06', '05/06', '06/06', '07/06'];
        const alertCounts = [3, 5, 2, 8, 4, 6, 1];
        
        const gradient = this.createGradient(ctx, 
            'rgba(231, 76, 60, 0.6)', 
            'rgba(231, 76, 60, 0.1)'
        );
        
        return {
            labels: dates,
            datasets: [{
                label: 'Alertas por Dia',
                data: alertCounts,
                borderColor: this.colors.danger,
                backgroundColor: gradient,
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: this.colors.danger,
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        };
    }
    
    processScheduleData(data, ctx) {
        const vehicles = ['ABC-1234', 'DEF-5678', 'GHI-9012'];
        const scheduled = [3, 2, 4];
        const completed = [2, 2, 3];
        const overdue = [1, 0, 1];
        
        return {
            labels: vehicles,
            datasets: [
                {
                    label: 'Agendadas',
                    data: scheduled,
                    backgroundColor: this.colors.info,
                    borderRadius: 4
                },
                {
                    label: 'Concluídas',
                    data: completed,
                    backgroundColor: this.colors.success,
                    borderRadius: 4
                },
                {
                    label: 'Atrasadas',
                    data: overdue,
                    backgroundColor: this.colors.danger,
                    borderRadius: 4
                }
            ]
        };
    }
    
    processCostsData(data, ctx) {
        const months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'];
        const costs = [15000, 18000, 12000, 22000, 16000, 19000];
        
        const gradient = this.createGradient(ctx, 
            'rgba(155, 89, 182, 0.6)', 
            'rgba(155, 89, 182, 0.1)'
        );
        
        return {
            labels: months,
            datasets: [{
                label: 'Custos de Manutenção',
                data: costs,
                borderColor: this.colors.purple,
                backgroundColor: gradient,
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: this.colors.purple,
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        };
    }
    
    processDefaultData(data, ctx) {
        return {
            labels: ['Dados', 'Exemplo'],
            datasets: [{
                label: 'Valores',
                data: [10, 20],
                backgroundColor: this.colors.primary,
                borderColor: this.colors.primary,
                borderWidth: 1
            }]
        };
    }
    
    updateChart(canvasId, newData) {
        const chart = this.charts[canvasId];
        if (!chart) return;
        
        chart.data = newData;
        chart.update('active');
    }
    
    destroyChart(canvasId) {
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
            delete this.charts[canvasId];
        }
    }
    
    destroyAllCharts() {
        Object.keys(this.charts).forEach(canvasId => {
            this.destroyChart(canvasId);
        });
    }
    
    resizeCharts() {
        Object.values(this.charts).forEach(chart => {
            chart.resize();
        });
    }
    
    exportChart(canvasId, filename = 'chart') {
        const chart = this.charts[canvasId];
        if (!chart) return;
        
        const url = chart.toBase64Image();
        const link = document.createElement('a');
        link.download = `${filename}.png`;
        link.href = url;
        link.click();
    }
    
    getChartImage(canvasId) {
        const chart = this.charts[canvasId];
        if (!chart) return null;
        
        return chart.toBase64Image();
    }
}

// Chart Templates for different collections
class ChartTemplates {
    static getChecklistCharts() {
        return [
            {
                id: 'complianceChart',
                type: 'compliance',
                title: 'Status de Conformidade',
                description: 'Distribuição entre itens conformes e não conformes'
            },
            {
                id: 'evolutionChart',
                type: 'evolution',
                title: 'Evolução da Conformidade',
                description: 'Taxa de conformidade ao longo do tempo'
            },
            {
                id: 'itemTypesChart',
                type: 'itemTypes',
                title: 'Verificações por Tipo de Item',
                description: 'Quantidade de verificações por categoria'
            },
            {
                id: 'vehicleStatusChart',
                type: 'vehicleStatus',
                title: 'Status dos Veículos',
                description: 'Distribuição do status da frota'
            }
        ];
    }
    
    static getTripsCharts() {
        return [
            {
                id: 'distanceChart',
                type: 'distance',
                title: 'Distância por Veículo',
                description: 'Quilometragem percorrida por veículo'
            },
            {
                id: 'speedChart',
                type: 'speed',
                title: 'Performance de Condução',
                description: 'Métricas de velocidade e condução'
            },
            {
                id: 'routesChart',
                type: 'routes',
                title: 'Rotas Mais Utilizadas',
                description: 'Frequência de uso das rotas'
            },
            {
                id: 'efficiencyChart',
                type: 'efficiency',
                title: 'Eficiência Operacional',
                description: 'Indicadores de eficiência da frota'
            }
        ];
    }
    
    static getAlertsCharts() {
        return [
            {
                id: 'severityChart',
                type: 'severity',
                title: 'Alertas por Severidade',
                description: 'Distribuição dos alertas por nível de criticidade'
            },
            {
                id: 'typesChart',
                type: 'types',
                title: 'Tipos de Alertas',
                description: 'Categorias de alertas mais frequentes'
            },
            {
                id: 'timelineChart',
                type: 'timeline',
                title: 'Timeline de Alertas',
                description: 'Evolução dos alertas ao longo do tempo'
            },
            {
                id: 'distributionChart',
                type: 'distribution',
                title: 'Distribuição por Veículo',
                description: 'Alertas distribuídos pela frota'
            }
        ];
    }
    
    static getMaintenanceCharts() {
        return [
            {
                id: 'scheduleChart',
                type: 'schedule',
                title: 'Cronograma de Manutenção',
                description: 'Status das manutenções programadas'
            },
            {
                id: 'costsChart',
                type: 'costs',
                title: 'Custos de Manutenção',
                description: 'Evolução dos custos ao longo do tempo'
            },
            {
                id: 'typesChart',
                type: 'types',
                title: 'Tipos de Manutenção',
                description: 'Distribuição por tipo de manutenção'
            },
            {
                id: 'performanceChart',
                type: 'performance',
                title: 'Performance da Manutenção',
                description: 'Indicadores de eficiência da manutenção'
            }
        ];
    }
    
    static getChartsForCollection(collection) {
        switch(collection) {
            case 'checklist':
                return this.getChecklistCharts();
            case 'trips':
                return this.getTripsCharts();
            case 'alerts':
                return this.getAlertsCharts();
            case 'maintenance':
                return this.getMaintenanceCharts();
            default:
                return this.getChecklistCharts();
        }
    }
}

// Global chart manager instance
let chartManager;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    chartManager = new ChartManager();
    
    // Handle window resize
    window.addEventListener('resize', () => {
        chartManager.resizeCharts();
    });
});

// Global functions for chart management
function createChartsForCollection(collection, data) {
    if (!chartManager) return;
    
    const charts = ChartTemplates.getChartsForCollection(collection);
    const chartsGrid = document.getElementById('chartsGrid');
    
    if (!chartsGrid) return;
    
    // Generate charts HTML
    let chartsHTML = '';
    charts.forEach(chart => {
        chartsHTML += `
            <div class="chart-card">
                <div class="chart-header">
                    <div>
                        <h3 class="chart-title">${chart.title}</h3>
                        <p class="chart-description">${chart.description}</p>
                    </div>
                    <div class="chart-actions">
                        <button class="btn btn-sm btn-outline-primary" onclick="chartManager.exportChart('${chart.id}', '${chart.id}')">
                            <i class="fas fa-download"></i>
                        </button>
                    </div>
                </div>
                <div class="chart-container">
                    <canvas id="${chart.id}"></canvas>
                </div>
            </div>
        `;
    });
    
    chartsGrid.innerHTML = chartsHTML;
    
    // Create charts after DOM update
    setTimeout(() => {
        charts.forEach(chart => {
            chartManager.createChart(chart.id, chart.type, data, collection);
        });
    }, 100);
}

function updateChartsData(data) {
    if (!chartManager) return;
    
    Object.keys(chartManager.charts).forEach(canvasId => {
        const chart = chartManager.charts[canvasId];
        if (chart) {
            // Update chart data based on new data
            // This would be more sophisticated in a real implementation
            chart.update();
        }
    });
}

