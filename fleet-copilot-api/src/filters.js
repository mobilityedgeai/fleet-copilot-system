/**
 * Sistema de Filtros Interativos para BI de Frotas
 * Gerencia filtros dinâmicos, persistência e atualização de dados
 */

class FilterManager {
    constructor() {
        this.filters = {
            startDate: null,
            endDate: null,
            garage: '',
            branch: '',
            plate: '',
            itemType: '',
            status: '',
            collection: 'checklist'
        };
        
        this.filterOptions = {
            plates: [],
            itemTypes: [],
            garages: [],
            branches: []
        };
        
        this.callbacks = {
            onFilterChange: null,
            onDataUpdate: null
        };
        
        this.init();
    }
    
    init() {
        this.loadFiltersFromStorage();
        this.bindEvents();
        this.setDefaultDates();
    }
    
    bindEvents() {
        // Date filters
        document.getElementById('startDate')?.addEventListener('change', (e) => {
            this.updateFilter('startDate', e.target.value);
        });
        
        document.getElementById('endDate')?.addEventListener('change', (e) => {
            this.updateFilter('endDate', e.target.value);
        });
        
        // Dropdown filters
        document.getElementById('garageFilter')?.addEventListener('change', (e) => {
            this.updateFilter('garage', e.target.value);
        });
        
        document.getElementById('branchFilter')?.addEventListener('change', (e) => {
            this.updateFilter('branch', e.target.value);
        });
        
        document.getElementById('plateFilter')?.addEventListener('change', (e) => {
            this.updateFilter('plate', e.target.value);
        });
        
        document.getElementById('itemTypeFilter')?.addEventListener('change', (e) => {
            this.updateFilter('itemType', e.target.value);
        });
        
        document.getElementById('statusFilter')?.addEventListener('change', (e) => {
            this.updateFilter('status', e.target.value);
        });
        
        // Collection tabs
        document.querySelectorAll('.collection-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.updateCollection(tab.dataset.collection);
            });
        });
        
        // Quick filter buttons
        document.querySelectorAll('.quick-filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const period = btn.getAttribute('onclick')?.match(/'([^']+)'/)?.[1];
                if (period) {
                    this.setQuickFilter(period);
                }
            });
        });
    }
    
    updateFilter(key, value) {
        this.filters[key] = value;
        this.saveFiltersToStorage();
        this.triggerFilterChange();
    }
    
    updateCollection(collection) {
        // Update active tab
        document.querySelectorAll('.collection-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-collection="${collection}"]`)?.classList.add('active');
        
        this.filters.collection = collection;
        this.saveFiltersToStorage();
        this.updateFilterOptions(collection);
        this.triggerFilterChange();
    }
    
    setQuickFilter(period) {
        // Update active quick filter button
        document.querySelectorAll('.quick-filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        event.target.classList.add('active');
        
        const today = new Date();
        let startDate;
        
        switch(period) {
            case 'today':
                startDate = new Date(today);
                break;
            case '7days':
                startDate = new Date(today.getTime() - (7 * 24 * 60 * 60 * 1000));
                break;
            case '30days':
                startDate = new Date(today.getTime() - (30 * 24 * 60 * 60 * 1000));
                break;
            case '90days':
                startDate = new Date(today.getTime() - (90 * 24 * 60 * 60 * 1000));
                break;
        }
        
        this.filters.startDate = startDate.toISOString().split('T')[0];
        this.filters.endDate = today.toISOString().split('T')[0];
        
        // Update form inputs
        document.getElementById('startDate').value = this.filters.startDate;
        document.getElementById('endDate').value = this.filters.endDate;
        
        this.saveFiltersToStorage();
        this.triggerFilterChange();
    }
    
    setDefaultDates() {
        if (!this.filters.startDate || !this.filters.endDate) {
            const today = new Date();
            const thirtyDaysAgo = new Date(today.getTime() - (30 * 24 * 60 * 60 * 1000));
            
            this.filters.endDate = today.toISOString().split('T')[0];
            this.filters.startDate = thirtyDaysAgo.toISOString().split('T')[0];
            
            document.getElementById('endDate').value = this.filters.endDate;
            document.getElementById('startDate').value = this.filters.startDate;
        }
    }
    
    updateFilterOptions(collection) {
        // Clear existing options
        this.clearFilterOptions();
        
        // Load new options based on collection
        this.loadFilterOptions(collection);
    }
    
    clearFilterOptions() {
        const selects = ['plateFilter', 'itemTypeFilter', 'garageFilter', 'branchFilter'];
        selects.forEach(selectId => {
            const select = document.getElementById(selectId);
            if (select) {
                // Keep first option (All/Todos)
                const firstOption = select.firstElementChild;
                select.innerHTML = '';
                if (firstOption) {
                    select.appendChild(firstOption);
                }
            }
        });
    }
    
    async loadFilterOptions(collection) {
        try {
            // Load options from API based on collection
            const options = await this.fetchFilterOptions(collection);
            
            this.populateFilterDropdowns(options);
            this.filterOptions = options;
            
        } catch (error) {
            console.error('Error loading filter options:', error);
        }
    }
    
    async fetchFilterOptions(collection) {
        // This would normally fetch from your API
        // For now, return sample data
        
        const sampleOptions = {
            checklist: {
                plates: ['ABC-1234', 'DEF-5678', 'GHI-9012', 'JKL-3456'],
                itemTypes: ['Farol', 'Pneu', 'Freio', 'Motor', 'Bateria', 'Óleo'],
                garages: ['Garagem Central', 'Garagem Norte', 'Garagem Sul'],
                branches: ['Filial SP', 'Filial RJ', 'Filial BH', 'Filial RS']
            },
            trips: {
                plates: ['ABC-1234', 'DEF-5678', 'GHI-9012'],
                itemTypes: [],
                garages: ['Garagem Central', 'Garagem Norte'],
                branches: ['Filial SP', 'Filial RJ']
            },
            alerts: {
                plates: ['ABC-1234', 'DEF-5678'],
                itemTypes: ['Velocidade', 'Combustível', 'Manutenção'],
                garages: ['Garagem Central'],
                branches: ['Filial SP']
            },
            maintenance: {
                plates: ['ABC-1234', 'DEF-5678', 'GHI-9012'],
                itemTypes: ['Preventiva', 'Corretiva', 'Preditiva'],
                garages: ['Garagem Central', 'Garagem Norte'],
                branches: ['Filial SP', 'Filial RJ']
            }
        };
        
        return sampleOptions[collection] || sampleOptions.checklist;
    }
    
    populateFilterDropdowns(options) {
        // Populate plates
        this.populateSelect('plateFilter', options.plates, 'Todas as Placas');
        
        // Populate item types
        this.populateSelect('itemTypeFilter', options.itemTypes, 'Todos os Tipos');
        
        // Populate garages
        this.populateSelect('garageFilter', options.garages, 'Todas as Garagens');
        
        // Populate branches
        this.populateSelect('branchFilter', options.branches, 'Todas as Filiais');
    }
    
    populateSelect(selectId, options, defaultText) {
        const select = document.getElementById(selectId);
        if (!select) return;
        
        // Clear existing options except first
        const firstOption = select.firstElementChild;
        select.innerHTML = '';
        
        // Add default option
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = defaultText;
        select.appendChild(defaultOption);
        
        // Add options
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option;
            optionElement.textContent = option;
            select.appendChild(optionElement);
        });
        
        // Restore selected value if exists
        if (this.filters[selectId.replace('Filter', '')]) {
            select.value = this.filters[selectId.replace('Filter', '')];
        }
    }
    
    getActiveFilters() {
        const activeFilters = {};
        
        Object.keys(this.filters).forEach(key => {
            if (this.filters[key] && this.filters[key] !== '') {
                activeFilters[key] = this.filters[key];
            }
        });
        
        return activeFilters;
    }
    
    getFilterParams() {
        const params = new URLSearchParams();
        
        Object.keys(this.filters).forEach(key => {
            if (this.filters[key] && this.filters[key] !== '') {
                params.append(key, this.filters[key]);
            }
        });
        
        return params.toString();
    }
    
    clearAllFilters() {
        // Reset filters
        this.filters = {
            startDate: null,
            endDate: null,
            garage: '',
            branch: '',
            plate: '',
            itemType: '',
            status: '',
            collection: this.filters.collection // Keep current collection
        };
        
        // Reset form inputs
        document.getElementById('garageFilter').value = '';
        document.getElementById('branchFilter').value = '';
        document.getElementById('plateFilter').value = '';
        document.getElementById('itemTypeFilter').value = '';
        document.getElementById('statusFilter').value = '';
        
        // Reset dates
        this.setDefaultDates();
        
        // Reset quick filter buttons
        document.querySelectorAll('.quick-filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector('.quick-filter-btn[onclick*="30days"]')?.classList.add('active');
        
        this.saveFiltersToStorage();
        this.triggerFilterChange();
    }
    
    saveFiltersToStorage() {
        try {
            localStorage.setItem('biFilters', JSON.stringify(this.filters));
        } catch (error) {
            console.warn('Could not save filters to localStorage:', error);
        }
    }
    
    loadFiltersFromStorage() {
        try {
            const saved = localStorage.getItem('biFilters');
            if (saved) {
                const parsedFilters = JSON.parse(saved);
                this.filters = { ...this.filters, ...parsedFilters };
                this.applyFiltersToForm();
            }
        } catch (error) {
            console.warn('Could not load filters from localStorage:', error);
        }
    }
    
    applyFiltersToForm() {
        // Apply saved filters to form inputs
        if (this.filters.startDate) {
            document.getElementById('startDate').value = this.filters.startDate;
        }
        if (this.filters.endDate) {
            document.getElementById('endDate').value = this.filters.endDate;
        }
        if (this.filters.garage) {
            document.getElementById('garageFilter').value = this.filters.garage;
        }
        if (this.filters.branch) {
            document.getElementById('branchFilter').value = this.filters.branch;
        }
        if (this.filters.plate) {
            document.getElementById('plateFilter').value = this.filters.plate;
        }
        if (this.filters.itemType) {
            document.getElementById('itemTypeFilter').value = this.filters.itemType;
        }
        if (this.filters.status) {
            document.getElementById('statusFilter').value = this.filters.status;
        }
        
        // Apply collection tab
        if (this.filters.collection) {
            document.querySelectorAll('.collection-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelector(`[data-collection="${this.filters.collection}"]`)?.classList.add('active');
        }
    }
    
    triggerFilterChange() {
        if (this.callbacks.onFilterChange) {
            this.callbacks.onFilterChange(this.getActiveFilters());
        }
    }
    
    onFilterChange(callback) {
        this.callbacks.onFilterChange = callback;
    }
    
    onDataUpdate(callback) {
        this.callbacks.onDataUpdate = callback;
    }
    
    // Validation methods
    validateDateRange() {
        if (this.filters.startDate && this.filters.endDate) {
            const start = new Date(this.filters.startDate);
            const end = new Date(this.filters.endDate);
            
            if (start > end) {
                this.showValidationError('Data inicial não pode ser maior que data final');
                return false;
            }
            
            // Check if range is too large (e.g., more than 1 year)
            const diffTime = Math.abs(end - start);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            
            if (diffDays > 365) {
                this.showValidationError('Período não pode ser maior que 1 ano');
                return false;
            }
        }
        
        return true;
    }
    
    showValidationError(message) {
        // Create or update validation message
        let errorDiv = document.getElementById('filter-validation-error');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = 'filter-validation-error';
            errorDiv.className = 'alert alert-warning mt-2';
            errorDiv.style.display = 'none';
            
            const filtersSection = document.querySelector('.filters-section');
            filtersSection.appendChild(errorDiv);
        }
        
        errorDiv.innerHTML = `
            <i class="fas fa-exclamation-triangle"></i>
            ${message}
        `;
        errorDiv.style.display = 'block';
        
        // Hide after 5 seconds
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    }
    
    // Export methods
    exportFilters() {
        return {
            filters: this.filters,
            options: this.filterOptions,
            timestamp: new Date().toISOString()
        };
    }
    
    importFilters(data) {
        if (data.filters) {
            this.filters = { ...this.filters, ...data.filters };
            this.applyFiltersToForm();
            this.saveFiltersToStorage();
            this.triggerFilterChange();
        }
    }
}

// Advanced Filter Features
class AdvancedFilters {
    constructor(filterManager) {
        this.filterManager = filterManager;
        this.savedFilters = [];
        this.init();
    }
    
    init() {
        this.loadSavedFilters();
        this.createAdvancedUI();
    }
    
    createAdvancedUI() {
        // Add advanced filter controls
        const filtersSection = document.querySelector('.filters-section');
        if (!filtersSection) return;
        
        const advancedControls = document.createElement('div');
        advancedControls.className = 'advanced-filters mt-3';
        advancedControls.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <div class="filter-group">
                        <label class="filter-label">Filtros Salvos</label>
                        <div class="input-group">
                            <select class="form-select" id="savedFiltersSelect">
                                <option value="">Selecione um filtro salvo</option>
                            </select>
                            <button class="btn btn-outline-primary" onclick="advancedFilters.loadSavedFilter()">
                                <i class="fas fa-upload"></i>
                            </button>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="filter-group">
                        <label class="filter-label">Salvar Filtro Atual</label>
                        <div class="input-group">
                            <input type="text" class="form-control" id="saveFilterName" placeholder="Nome do filtro">
                            <button class="btn btn-outline-primary" onclick="advancedFilters.saveCurrentFilter()">
                                <i class="fas fa-save"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-2">
                <div class="col-12">
                    <div class="filter-actions-advanced">
                        <button class="btn btn-sm btn-outline-info" onclick="advancedFilters.exportFilters()">
                            <i class="fas fa-download"></i>
                            Exportar Filtros
                        </button>
                        <button class="btn btn-sm btn-outline-info" onclick="advancedFilters.importFilters()">
                            <i class="fas fa-upload"></i>
                            Importar Filtros
                        </button>
                        <button class="btn btn-sm btn-outline-secondary" onclick="advancedFilters.resetToDefaults()">
                            <i class="fas fa-undo"></i>
                            Padrões
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        filtersSection.appendChild(advancedControls);
        this.updateSavedFiltersDropdown();
    }
    
    saveCurrentFilter() {
        const nameInput = document.getElementById('saveFilterName');
        const name = nameInput.value.trim();
        
        if (!name) {
            alert('Por favor, digite um nome para o filtro');
            return;
        }
        
        const filterData = {
            name: name,
            filters: this.filterManager.getActiveFilters(),
            created: new Date().toISOString()
        };
        
        this.savedFilters.push(filterData);
        this.saveSavedFilters();
        this.updateSavedFiltersDropdown();
        
        nameInput.value = '';
        
        // Show success message
        this.showMessage('Filtro salvo com sucesso!', 'success');
    }
    
    loadSavedFilter() {
        const select = document.getElementById('savedFiltersSelect');
        const selectedIndex = select.value;
        
        if (!selectedIndex) return;
        
        const filterData = this.savedFilters[selectedIndex];
        if (filterData) {
            this.filterManager.importFilters({ filters: filterData.filters });
            this.showMessage('Filtro carregado com sucesso!', 'success');
        }
    }
    
    updateSavedFiltersDropdown() {
        const select = document.getElementById('savedFiltersSelect');
        if (!select) return;
        
        select.innerHTML = '<option value="">Selecione um filtro salvo</option>';
        
        this.savedFilters.forEach((filter, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = `${filter.name} (${new Date(filter.created).toLocaleDateString()})`;
            select.appendChild(option);
        });
    }
    
    exportFilters() {
        const data = {
            savedFilters: this.savedFilters,
            currentFilters: this.filterManager.exportFilters(),
            exportDate: new Date().toISOString()
        };
        
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `bi-filters-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        
        URL.revokeObjectURL(url);
    }
    
    importFilters() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';
        
        input.onchange = (e) => {
            const file = e.target.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const data = JSON.parse(e.target.result);
                    
                    if (data.savedFilters) {
                        this.savedFilters = data.savedFilters;
                        this.saveSavedFilters();
                        this.updateSavedFiltersDropdown();
                    }
                    
                    if (data.currentFilters) {
                        this.filterManager.importFilters(data.currentFilters);
                    }
                    
                    this.showMessage('Filtros importados com sucesso!', 'success');
                    
                } catch (error) {
                    this.showMessage('Erro ao importar filtros: ' + error.message, 'error');
                }
            };
            
            reader.readAsText(file);
        };
        
        input.click();
    }
    
    resetToDefaults() {
        if (confirm('Tem certeza que deseja resetar todos os filtros para os padrões?')) {
            this.filterManager.clearAllFilters();
            this.showMessage('Filtros resetados para os padrões', 'info');
        }
    }
    
    loadSavedFilters() {
        try {
            const saved = localStorage.getItem('biSavedFilters');
            if (saved) {
                this.savedFilters = JSON.parse(saved);
            }
        } catch (error) {
            console.warn('Could not load saved filters:', error);
        }
    }
    
    saveSavedFilters() {
        try {
            localStorage.setItem('biSavedFilters', JSON.stringify(this.savedFilters));
        } catch (error) {
            console.warn('Could not save filters:', error);
        }
    }
    
    showMessage(message, type = 'info') {
        // Create or update message div
        let messageDiv = document.getElementById('filter-message');
        if (!messageDiv) {
            messageDiv = document.createElement('div');
            messageDiv.id = 'filter-message';
            messageDiv.className = 'alert mt-2';
            messageDiv.style.display = 'none';
            
            const filtersSection = document.querySelector('.filters-section');
            filtersSection.appendChild(messageDiv);
        }
        
        // Set message type
        messageDiv.className = `alert alert-${type === 'error' ? 'danger' : type} mt-2`;
        
        const icons = {
            success: 'check-circle',
            error: 'exclamation-triangle',
            info: 'info-circle'
        };
        
        messageDiv.innerHTML = `
            <i class="fas fa-${icons[type] || 'info-circle'}"></i>
            ${message}
        `;
        messageDiv.style.display = 'block';
        
        // Hide after 3 seconds
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 3000);
    }
}

// Global instances
let filterManager;
let advancedFilters;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    filterManager = new FilterManager();
    advancedFilters = new AdvancedFilters(filterManager);
    
    // Set up callbacks
    filterManager.onFilterChange((filters) => {
        console.log('Filters changed:', filters);
        // Trigger data reload
        if (window.loadCollectionData) {
            window.loadCollectionData();
        }
    });
});

// Global functions for HTML onclick handlers
function applyFilters() {
    if (filterManager.validateDateRange()) {
        filterManager.triggerFilterChange();
    }
}

function clearFilters() {
    filterManager.clearAllFilters();
}

function setQuickFilter(period) {
    filterManager.setQuickFilter(period);
}

