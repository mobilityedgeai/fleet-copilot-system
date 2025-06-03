/**
 * Sistema de DataTables Avançado para BI de Frotas
 * Gerencia tabelas interativas com exportação e filtros
 */

class DataTableManager {
    constructor() {
        this.tables = {};
        this.tableConfigs = {};
        this.currentCollection = 'checklist';
        this.currentData = [];
        
        this.init();
    }
    
    init() {
        // Set DataTables defaults
        $.extend(true, $.fn.dataTable.defaults, {
            language: {
                url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/pt-BR.json'
            },
            pageLength: 25,
            responsive: true,
            processing: true,
            serverSide: false,
            stateSave: true,
            stateDuration: 60 * 60 * 24, // 24 hours
            dom: 'Bfrtip',
            buttons: this.getDefaultButtons(),
            order: [[0, 'desc']],
            columnDefs: [
                {
                    targets: '_all',
                    className: 'text-center'
                }
            ]
        });
        
        this.setupCustomStyles();
    }
    
    setupCustomStyles() {
        // Add custom CSS for DataTables
        const style = document.createElement('style');
        style.textContent = `
            /* DataTables Custom Styling */
            .dataTables_wrapper {
                color: #ecf0f1;
            }
            
            .dataTables_wrapper .dataTables_length,
            .dataTables_wrapper .dataTables_filter,
            .dataTables_wrapper .dataTables_info,
            .dataTables_wrapper .dataTables_paginate {
                color: #ecf0f1;
            }
            
            .dataTables_wrapper .dataTables_length select,
            .dataTables_wrapper .dataTables_filter input {
                background: #34495e;
                border: 1px solid #1abc9c;
                color: #ecf0f1;
                border-radius: 4px;
                padding: 5px 10px;
            }
            
            .dataTables_wrapper .dataTables_length select:focus,
            .dataTables_wrapper .dataTables_filter input:focus {
                outline: none;
                border-color: #16a085;
                box-shadow: 0 0 0 2px rgba(26, 188, 156, 0.2);
            }
            
            .dataTables_wrapper .dataTables_paginate .paginate_button {
                background: #34495e;
                border: 1px solid #1abc9c;
                color: #ecf0f1 !important;
                margin: 0 2px;
                border-radius: 4px;
                padding: 6px 12px;
                transition: all 0.3s ease;
            }
            
            .dataTables_wrapper .dataTables_paginate .paginate_button:hover {
                background: #1abc9c !important;
                border-color: #16a085 !important;
                color: white !important;
            }
            
            .dataTables_wrapper .dataTables_paginate .paginate_button.current {
                background: #1abc9c !important;
                border-color: #16a085 !important;
                color: white !important;
            }
            
            .dataTables_wrapper .dataTables_paginate .paginate_button.disabled {
                background: #2c3e50 !important;
                border-color: #34495e !important;
                color: #7f8c8d !important;
            }
            
            .dt-buttons {
                margin-bottom: 15px;
            }
            
            .dt-button {
                background: #1abc9c !important;
                border: none !important;
                color: white !important;
                padding: 8px 16px !important;
                border-radius: 4px !important;
                margin-right: 5px !important;
                font-weight: 500 !important;
                transition: all 0.3s ease !important;
            }
            
            .dt-button:hover {
                background: #16a085 !important;
                transform: translateY(-1px);
            }
            
            .dt-button.buttons-excel {
                background: #27ae60 !important;
            }
            
            .dt-button.buttons-excel:hover {
                background: #229954 !important;
            }
            
            .dt-button.buttons-pdf {
                background: #e74c3c !important;
            }
            
            .dt-button.buttons-pdf:hover {
                background: #c0392b !important;
            }
            
            .dt-button.buttons-print {
                background: #9b59b6 !important;
            }
            
            .dt-button.buttons-print:hover {
                background: #8e44ad !important;
            }
            
            .dt-button.buttons-copy {
                background: #3498db !important;
            }
            
            .dt-button.buttons-copy:hover {
                background: #2980b9 !important;
            }
            
            /* Loading overlay */
            .dataTables_processing {
                background: rgba(44, 62, 80, 0.9) !important;
                color: #ecf0f1 !important;
                border: 1px solid #1abc9c !important;
                border-radius: 8px !important;
                font-weight: 500 !important;
            }
            
            /* Row hover effects */
            .table-dark tbody tr:hover {
                background: #34495e !important;
                cursor: pointer;
            }
            
            /* Status badges */
            .status-badge {
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 0.8rem;
                font-weight: 500;
                text-transform: uppercase;
            }
            
            .status-conforme {
                background: #27ae60;
                color: white;
            }
            
            .status-nao-conforme {
                background: #e74c3c;
                color: white;
            }
            
            .status-pendente {
                background: #f39c12;
                color: white;
            }
            
            .status-ativo {
                background: #1abc9c;
                color: white;
            }
            
            .status-inativo {
                background: #95a5a6;
                color: white;
            }
            
            /* Priority indicators */
            .priority-high {
                color: #e74c3c;
                font-weight: bold;
            }
            
            .priority-medium {
                color: #f39c12;
                font-weight: 500;
            }
            
            .priority-low {
                color: #27ae60;
            }
            
            /* Action buttons in table */
            .table-action-btn {
                padding: 4px 8px;
                margin: 0 2px;
                border: none;
                border-radius: 4px;
                font-size: 0.8rem;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .table-action-btn.btn-view {
                background: #3498db;
                color: white;
            }
            
            .table-action-btn.btn-edit {
                background: #f39c12;
                color: white;
            }
            
            .table-action-btn.btn-delete {
                background: #e74c3c;
                color: white;
            }
            
            .table-action-btn:hover {
                transform: translateY(-1px);
                opacity: 0.9;
            }
        `;
        document.head.appendChild(style);
    }
    
    getDefaultButtons() {
        return [
            {
                extend: 'excel',
                text: '<i class="fas fa-file-excel"></i> Excel',
                className: 'btn btn-success btn-sm buttons-excel',
                exportOptions: {
                    columns: ':visible:not(.no-export)'
                },
                filename: function() {
                    return `bi-${this.currentCollection}-${new Date().toISOString().split('T')[0]}`;
                }.bind(this)
            },
            {
                extend: 'pdf',
                text: '<i class="fas fa-file-pdf"></i> PDF',
                className: 'btn btn-danger btn-sm buttons-pdf',
                exportOptions: {
                    columns: ':visible:not(.no-export)'
                },
                filename: function() {
                    return `bi-${this.currentCollection}-${new Date().toISOString().split('T')[0]}`;
                }.bind(this),
                customize: function(doc) {
                    doc.defaultStyle.fontSize = 8;
                    doc.styles.tableHeader.fontSize = 9;
                    doc.styles.tableHeader.fillColor = '#1abc9c';
                }
            },
            {
                extend: 'copy',
                text: '<i class="fas fa-copy"></i> Copiar',
                className: 'btn btn-info btn-sm buttons-copy',
                exportOptions: {
                    columns: ':visible:not(.no-export)'
                }
            },
            {
                extend: 'print',
                text: '<i class="fas fa-print"></i> Imprimir',
                className: 'btn btn-secondary btn-sm buttons-print',
                exportOptions: {
                    columns: ':visible:not(.no-export)'
                }
            },
            {
                text: '<i class="fas fa-columns"></i> Colunas',
                className: 'btn btn-outline-primary btn-sm',
                action: function(e, dt, node, config) {
                    this.showColumnVisibilityModal(dt);
                }.bind(this)
            },
            {
                text: '<i class="fas fa-sync"></i> Atualizar',
                className: 'btn btn-outline-primary btn-sm',
                action: function(e, dt, node, config) {
                    this.refreshTable();
                }.bind(this)
            }
        ];
    }
    
    getTableConfig(collection) {
        const configs = {
            checklist: {
                columns: [
                    {
                        data: 'created_at',
                        title: 'Data',
                        render: function(data) {
                            return data ? new Date(data).toLocaleDateString('pt-BR') : 'N/A';
                        }
                    },
                    {
                        data: 'vehiclePlate',
                        title: 'Placa',
                        render: function(data) {
                            return data || 'N/A';
                        }
                    },
                    {
                        data: 'driverName',
                        title: 'Motorista',
                        render: function(data) {
                            return data || 'N/A';
                        }
                    },
                    {
                        data: 'itemName',
                        title: 'Item',
                        render: function(data) {
                            return data || 'N/A';
                        }
                    },
                    {
                        data: 'noCompliant',
                        title: 'Status',
                        render: function(data, type, row) {
                            const isCompliant = !data;
                            const statusClass = isCompliant ? 'status-conforme' : 'status-nao-conforme';
                            const statusText = isCompliant ? 'Conforme' : 'Não Conforme';
                            return `<span class="status-badge ${statusClass}">${statusText}</span>`;
                        }
                    },
                    {
                        data: 'observations',
                        title: 'Observações',
                        render: function(data) {
                            return data || 'Sem observações';
                        }
                    },
                    {
                        data: null,
                        title: 'Ações',
                        className: 'no-export',
                        orderable: false,
                        render: function(data, type, row) {
                            return `
                                <button class="table-action-btn btn-view" onclick="viewChecklistItem('${row.id || ''}')">
                                    <i class="fas fa-eye"></i>
                                </button>
                                <button class="table-action-btn btn-edit" onclick="editChecklistItem('${row.id || ''}')">
                                    <i class="fas fa-edit"></i>
                                </button>
                            `;
                        }
                    }
                ],
                order: [[0, 'desc']]
            },
            
            trips: {
                columns: [
                    {
                        data: 'date',
                        title: 'Data',
                        render: function(data) {
                            return data ? new Date(data).toLocaleDateString('pt-BR') : 'N/A';
                        }
                    },
                    {
                        data: 'vehiclePlate',
                        title: 'Placa'
                    },
                    {
                        data: 'driverName',
                        title: 'Motorista'
                    },
                    {
                        data: 'origin',
                        title: 'Origem'
                    },
                    {
                        data: 'destination',
                        title: 'Destino'
                    },
                    {
                        data: 'distance',
                        title: 'Distância (km)',
                        render: function(data) {
                            return data ? data.toLocaleString() : '0';
                        }
                    },
                    {
                        data: 'duration',
                        title: 'Duração'
                    },
                    {
                        data: 'avgSpeed',
                        title: 'Vel. Média',
                        render: function(data) {
                            return data ? `${data} km/h` : 'N/A';
                        }
                    },
                    {
                        data: null,
                        title: 'Ações',
                        className: 'no-export',
                        orderable: false,
                        render: function(data, type, row) {
                            return `
                                <button class="table-action-btn btn-view" onclick="viewTrip('${row.id || ''}')">
                                    <i class="fas fa-route"></i>
                                </button>
                            `;
                        }
                    }
                ],
                order: [[0, 'desc']]
            },
            
            alerts: {
                columns: [
                    {
                        data: 'timestamp',
                        title: 'Data/Hora',
                        render: function(data) {
                            return data ? new Date(data).toLocaleString('pt-BR') : 'N/A';
                        }
                    },
                    {
                        data: 'vehiclePlate',
                        title: 'Placa'
                    },
                    {
                        data: 'alertType',
                        title: 'Tipo de Alerta'
                    },
                    {
                        data: 'severity',
                        title: 'Severidade',
                        render: function(data) {
                            const severityClass = {
                                'high': 'priority-high',
                                'medium': 'priority-medium',
                                'low': 'priority-low'
                            };
                            const className = severityClass[data] || '';
                            return `<span class="${className}">${data || 'N/A'}</span>`;
                        }
                    },
                    {
                        data: 'description',
                        title: 'Descrição'
                    },
                    {
                        data: 'status',
                        title: 'Status',
                        render: function(data) {
                            const statusClass = data === 'resolved' ? 'status-conforme' : 'status-pendente';
                            const statusText = data === 'resolved' ? 'Resolvido' : 'Pendente';
                            return `<span class="status-badge ${statusClass}">${statusText}</span>`;
                        }
                    },
                    {
                        data: null,
                        title: 'Ações',
                        className: 'no-export',
                        orderable: false,
                        render: function(data, type, row) {
                            return `
                                <button class="table-action-btn btn-view" onclick="viewAlert('${row.id || ''}')">
                                    <i class="fas fa-eye"></i>
                                </button>
                                <button class="table-action-btn btn-edit" onclick="resolveAlert('${row.id || ''}')">
                                    <i class="fas fa-check"></i>
                                </button>
                            `;
                        }
                    }
                ],
                order: [[0, 'desc']]
            },
            
            maintenance: {
                columns: [
                    {
                        data: 'scheduledDate',
                        title: 'Data Agendada',
                        render: function(data) {
                            return data ? new Date(data).toLocaleDateString('pt-BR') : 'N/A';
                        }
                    },
                    {
                        data: 'vehiclePlate',
                        title: 'Placa'
                    },
                    {
                        data: 'maintenanceType',
                        title: 'Tipo'
                    },
                    {
                        data: 'description',
                        title: 'Descrição'
                    },
                    {
                        data: 'status',
                        title: 'Status',
                        render: function(data) {
                            const statusMap = {
                                'scheduled': { class: 'status-pendente', text: 'Agendada' },
                                'in_progress': { class: 'status-ativo', text: 'Em Andamento' },
                                'completed': { class: 'status-conforme', text: 'Concluída' },
                                'cancelled': { class: 'status-inativo', text: 'Cancelada' }
                            };
                            const status = statusMap[data] || { class: 'status-pendente', text: 'N/A' };
                            return `<span class="status-badge ${status.class}">${status.text}</span>`;
                        }
                    },
                    {
                        data: 'cost',
                        title: 'Custo',
                        render: function(data) {
                            return data ? `R$ ${data.toLocaleString()}` : 'N/A';
                        }
                    },
                    {
                        data: 'technician',
                        title: 'Técnico'
                    },
                    {
                        data: null,
                        title: 'Ações',
                        className: 'no-export',
                        orderable: false,
                        render: function(data, type, row) {
                            return `
                                <button class="table-action-btn btn-view" onclick="viewMaintenance('${row.id || ''}')">
                                    <i class="fas fa-eye"></i>
                                </button>
                                <button class="table-action-btn btn-edit" onclick="editMaintenance('${row.id || ''}')">
                                    <i class="fas fa-edit"></i>
                                </button>
                            `;
                        }
                    }
                ],
                order: [[0, 'desc']]
            }
        };
        
        return configs[collection] || configs.checklist;
    }
    
    createTable(tableId, collection, data) {
        this.currentCollection = collection;
        this.currentData = data;
        
        // Destroy existing table if exists
        if (this.tables[tableId]) {
            this.tables[tableId].destroy();
            delete this.tables[tableId];
        }
        
        const config = this.getTableConfig(collection);
        const tableConfig = {
            ...config,
            data: data,
            buttons: this.getDefaultButtons()
        };
        
        // Store config for later use
        this.tableConfigs[tableId] = tableConfig;
        
        // Initialize DataTable
        this.tables[tableId] = $(`#${tableId}`).DataTable(tableConfig);
        
        // Add custom event handlers
        this.addEventHandlers(tableId);
        
        return this.tables[tableId];
    }
    
    addEventHandlers(tableId) {
        const table = this.tables[tableId];
        if (!table) return;
        
        // Row click handler
        $(`#${tableId} tbody`).off('click', 'tr').on('click', 'tr', function() {
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
            } else {
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });
        
        // Double click to view details
        $(`#${tableId} tbody`).off('dblclick', 'tr').on('dblclick', 'tr', function() {
            const data = table.row(this).data();
            if (data) {
                this.showRowDetails(data);
            }
        }.bind(this));
    }
    
    updateTable(tableId, newData) {
        const table = this.tables[tableId];
        if (!table) return;
        
        table.clear();
        table.rows.add(newData);
        table.draw();
        
        this.currentData = newData;
    }
    
    refreshTable(tableId = null) {
        if (tableId && this.tables[tableId]) {
            this.tables[tableId].ajax.reload();
        } else {
            // Refresh all tables
            Object.keys(this.tables).forEach(id => {
                this.tables[id].ajax.reload();
            });
        }
    }
    
    exportTable(tableId, format = 'excel') {
        const table = this.tables[tableId];
        if (!table) return;
        
        switch(format) {
            case 'excel':
                table.button('.buttons-excel').trigger();
                break;
            case 'pdf':
                table.button('.buttons-pdf').trigger();
                break;
            case 'copy':
                table.button('.buttons-copy').trigger();
                break;
            case 'print':
                table.button('.buttons-print').trigger();
                break;
        }
    }
    
    showColumnVisibilityModal(table) {
        // Create modal for column visibility
        const columns = table.columns().header().toArray();
        let modalHTML = `
            <div class="modal fade" id="columnVisibilityModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content" style="background: #2c3e50; color: #ecf0f1;">
                        <div class="modal-header">
                            <h5 class="modal-title">Visibilidade das Colunas</h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
        `;
        
        columns.forEach((header, index) => {
            const columnText = $(header).text();
            const isVisible = table.column(index).visible();
            
            modalHTML += `
                <div class="col-md-6 mb-2">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="col_${index}" ${isVisible ? 'checked' : ''}>
                        <label class="form-check-label" for="col_${index}">
                            ${columnText}
                        </label>
                    </div>
                </div>
            `;
        });
        
        modalHTML += `
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                            <button type="button" class="btn btn-primary" onclick="dataTableManager.applyColumnVisibility()">Aplicar</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Remove existing modal
        $('#columnVisibilityModal').remove();
        
        // Add new modal
        $('body').append(modalHTML);
        
        // Store table reference
        this.currentModalTable = table;
        
        // Show modal
        $('#columnVisibilityModal').modal('show');
    }
    
    applyColumnVisibility() {
        const table = this.currentModalTable;
        if (!table) return;
        
        // Apply visibility changes
        $('#columnVisibilityModal input[type="checkbox"]').each(function(index) {
            const columnIndex = parseInt($(this).attr('id').split('_')[1]);
            const isVisible = $(this).is(':checked');
            table.column(columnIndex).visible(isVisible);
        });
        
        // Close modal
        $('#columnVisibilityModal').modal('hide');
    }
    
    showRowDetails(rowData) {
        // Create modal for row details
        let detailsHTML = `
            <div class="modal fade" id="rowDetailsModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content" style="background: #2c3e50; color: #ecf0f1;">
                        <div class="modal-header">
                            <h5 class="modal-title">Detalhes do Registro</h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
        `;
        
        Object.keys(rowData).forEach(key => {
            if (key !== null && rowData[key] !== null) {
                const label = this.formatFieldLabel(key);
                const value = this.formatFieldValue(key, rowData[key]);
                
                detailsHTML += `
                    <div class="col-md-6 mb-3">
                        <strong>${label}:</strong><br>
                        <span>${value}</span>
                    </div>
                `;
            }
        });
        
        detailsHTML += `
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Remove existing modal
        $('#rowDetailsModal').remove();
        
        // Add new modal
        $('body').append(detailsHTML);
        
        // Show modal
        $('#rowDetailsModal').modal('show');
    }
    
    formatFieldLabel(fieldName) {
        const labelMap = {
            'created_at': 'Data de Criação',
            'vehiclePlate': 'Placa do Veículo',
            'driverName': 'Nome do Motorista',
            'itemName': 'Nome do Item',
            'noCompliant': 'Não Conforme',
            'observations': 'Observações',
            'timestamp': 'Data/Hora',
            'alertType': 'Tipo de Alerta',
            'severity': 'Severidade',
            'description': 'Descrição',
            'status': 'Status',
            'scheduledDate': 'Data Agendada',
            'maintenanceType': 'Tipo de Manutenção',
            'cost': 'Custo',
            'technician': 'Técnico'
        };
        
        return labelMap[fieldName] || fieldName;
    }
    
    formatFieldValue(fieldName, value) {
        if (value === null || value === undefined) {
            return 'N/A';
        }
        
        // Date fields
        if (fieldName.includes('date') || fieldName === 'created_at' || fieldName === 'timestamp') {
            return new Date(value).toLocaleString('pt-BR');
        }
        
        // Boolean fields
        if (typeof value === 'boolean') {
            return value ? 'Sim' : 'Não';
        }
        
        // Cost fields
        if (fieldName === 'cost' && typeof value === 'number') {
            return `R$ ${value.toLocaleString()}`;
        }
        
        return value.toString();
    }
    
    getSelectedRows(tableId) {
        const table = this.tables[tableId];
        if (!table) return [];
        
        return table.rows('.selected').data().toArray();
    }
    
    clearSelection(tableId) {
        const table = this.tables[tableId];
        if (!table) return;
        
        table.$('tr.selected').removeClass('selected');
    }
    
    searchTable(tableId, searchTerm) {
        const table = this.tables[tableId];
        if (!table) return;
        
        table.search(searchTerm).draw();
    }
    
    filterColumn(tableId, columnIndex, filterValue) {
        const table = this.tables[tableId];
        if (!table) return;
        
        table.column(columnIndex).search(filterValue).draw();
    }
    
    destroyTable(tableId) {
        if (this.tables[tableId]) {
            this.tables[tableId].destroy();
            delete this.tables[tableId];
            delete this.tableConfigs[tableId];
        }
    }
    
    destroyAllTables() {
        Object.keys(this.tables).forEach(tableId => {
            this.destroyTable(tableId);
        });
    }
    
    // Advanced filtering
    addAdvancedFilters(tableId) {
        const table = this.tables[tableId];
        if (!table) return;
        
        // Add individual column filters
        $(`#${tableId} thead tr`).clone(true).appendTo(`#${tableId} thead`);
        $(`#${tableId} thead tr:eq(1) th`).each(function(i) {
            const title = $(this).text();
            $(this).html(`<input type="text" placeholder="Filtrar ${title}" class="form-control form-control-sm" style="background: #34495e; border: 1px solid #1abc9c; color: #ecf0f1;" />`);
            
            $('input', this).on('keyup change', function() {
                if (table.column(i).search() !== this.value) {
                    table.column(i).search(this.value).draw();
                }
            });
        });
    }
    
    // Statistics
    getTableStats(tableId) {
        const table = this.tables[tableId];
        if (!table) return null;
        
        const data = table.data().toArray();
        
        return {
            totalRows: data.length,
            filteredRows: table.rows({ filter: 'applied' }).count(),
            selectedRows: table.rows('.selected').count(),
            columns: table.columns().count()
        };
    }
}

// Global DataTable manager instance
let dataTableManager;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    dataTableManager = new DataTableManager();
});

// Global functions for table management
function createTableForCollection(collection, data) {
    if (!dataTableManager) return;
    
    return dataTableManager.createTable('dataTable', collection, data);
}

function updateTableData(data) {
    if (!dataTableManager) return;
    
    dataTableManager.updateTable('dataTable', data);
}

function exportToExcel() {
    if (!dataTableManager) return;
    
    dataTableManager.exportTable('dataTable', 'excel');
}

function exportToPDF() {
    if (!dataTableManager) return;
    
    dataTableManager.exportTable('dataTable', 'pdf');
}

// Action handlers for table buttons
function viewChecklistItem(id) {
    console.log('Viewing checklist item:', id);
    // Implement view logic
}

function editChecklistItem(id) {
    console.log('Editing checklist item:', id);
    // Implement edit logic
}

function viewTrip(id) {
    console.log('Viewing trip:', id);
    // Implement view logic
}

function viewAlert(id) {
    console.log('Viewing alert:', id);
    // Implement view logic
}

function resolveAlert(id) {
    console.log('Resolving alert:', id);
    // Implement resolve logic
}

function viewMaintenance(id) {
    console.log('Viewing maintenance:', id);
    // Implement view logic
}

function editMaintenance(id) {
    console.log('Editing maintenance:', id);
    // Implement edit logic
}

