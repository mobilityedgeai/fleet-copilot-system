import React, { useState, useEffect } from 'react'
import { Truck, Users, CheckCircle, AlertTriangle, BarChart3, RefreshCw, MessageCircle } from 'lucide-react'
import './App.css'

// Configuração da API
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://sua-app.onrender.com/api/copilot'  // Será atualizado no deploy
  : 'http://localhost:5000/api/copilot'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [fleetData, setFleetData] = useState(null)
  const [vehicles, setVehicles] = useState([])
  const [insights, setInsights] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [question, setQuestion] = useState('')
  const [chatResponse, setChatResponse] = useState('')
  const [chatLoading, setChatLoading] = useState(false)

  // Parâmetros configuráveis
  const enterpriseId = 'sA9EmrE3ymtnBqJKcYn7'
  const days = 30

  // Carregar dados iniciais
  useEffect(() => {
    loadFleetData()
  }, [])

  const loadFleetData = async () => {
    try {
      setLoading(true)
      setError(null)

      // Carregar resumo da frota
      const summaryResponse = await fetch(`${API_BASE_URL}/summary?enterpriseId=${enterpriseId}&days=${days}`)
      const summaryData = await summaryResponse.json()
      
      if (summaryData.success) {
        setFleetData(summaryData.data)
      }

      // Carregar veículos
      const vehiclesResponse = await fetch(`${API_BASE_URL}/vehicles?enterpriseId=${enterpriseId}&days=${days}`)
      const vehiclesData = await vehiclesResponse.json()
      
      if (vehiclesData.success) {
        setVehicles(vehiclesData.data)
      }

      // Carregar insights
      const insightsResponse = await fetch(`${API_BASE_URL}/insights?enterpriseId=${enterpriseId}&days=${days}`)
      const insightsData = await insightsResponse.json()
      
      if (insightsData.success) {
        setInsights(insightsData.data)
      }

    } catch (err) {
      setError('Erro ao carregar dados: ' + err.message)
      console.error('Erro:', err)
    } finally {
      setLoading(false)
    }
  }

  const askQuestion = async () => {
    if (!question.trim()) return

    try {
      setChatLoading(true)
      setChatResponse('')

      const response = await fetch(`${API_BASE_URL}/question`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: question,
          enterpriseId: enterpriseId,
          days: days
        })
      })

      const data = await response.json()
      
      if (data.success) {
        setChatResponse(data.data.answer)
      } else {
        setChatResponse('Erro ao processar pergunta: ' + data.message)
      }

    } catch (err) {
      setChatResponse('Erro ao enviar pergunta: ' + err.message)
    } finally {
      setChatLoading(false)
    }
  }

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'text-red-600 bg-red-50 border-red-200'
      case 'medium': return 'text-yellow-600 bg-yellow-50 border-yellow-200'
      case 'low': return 'text-green-600 bg-green-50 border-green-200'
      default: return 'text-gray-600 bg-gray-50 border-gray-200'
    }
  }

  const getComplianceColor = (rate) => {
    if (rate >= 90) return 'text-green-600'
    if (rate >= 70) return 'text-yellow-600'
    return 'text-red-600'
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-4 text-blue-600" />
          <p className="text-gray-600">Carregando dados da frota...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md">
          <AlertTriangle className="h-12 w-12 mx-auto mb-4 text-red-600" />
          <h2 className="text-xl font-bold text-gray-900 mb-2">Erro ao Carregar</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button 
            onClick={loadFleetData}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Tentar Novamente
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="bg-blue-600 p-2 rounded-lg">
                <Truck className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Copiloto de Frotas</h1>
                <p className="text-sm text-gray-500">Gestão Inteligente de Frotas</p>
              </div>
            </div>
            <button
              onClick={loadFleetData}
              className="flex items-center space-x-2 px-3 py-2 text-sm bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors"
            >
              <RefreshCw className="h-4 w-4" />
              <span>Atualizar</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Navigation Tabs */}
        <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg mb-6">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'dashboard'
                ? 'bg-white text-blue-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <BarChart3 className="h-4 w-4" />
            <span>Dashboard</span>
          </button>
          <button
            onClick={() => setActiveTab('insights')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'insights'
                ? 'bg-white text-blue-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <AlertTriangle className="h-4 w-4" />
            <span>Insights</span>
          </button>
          <button
            onClick={() => setActiveTab('vehicles')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'vehicles'
                ? 'bg-white text-blue-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <Truck className="h-4 w-4" />
            <span>Veículos</span>
          </button>
          <button
            onClick={() => setActiveTab('chat')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'chat'
                ? 'bg-white text-blue-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <MessageCircle className="h-4 w-4" />
            <span>Chat</span>
          </button>
        </div>

        {/* Dashboard Content */}
        {activeTab === 'dashboard' && fleetData && (
          <div className="space-y-6">
            {/* Metrics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Total de Verificações</p>
                    <p className="text-2xl font-bold text-gray-900">{fleetData.totalChecks}</p>
                  </div>
                  <CheckCircle className="h-8 w-8 text-green-600" />
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Taxa de Conformidade</p>
                    <p className={`text-2xl font-bold ${getComplianceColor(fleetData.complianceRate)}`}>
                      {fleetData.complianceRate}%
                    </p>
                  </div>
                  <BarChart3 className="h-8 w-8 text-blue-600" />
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Veículos Ativos</p>
                    <p className="text-2xl font-bold text-gray-900">{fleetData.totalVehicles}</p>
                  </div>
                  <Truck className="h-8 w-8 text-purple-600" />
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Motoristas</p>
                    <p className="text-2xl font-bold text-gray-900">{fleetData.totalDrivers}</p>
                  </div>
                  <Users className="h-8 w-8 text-orange-600" />
                </div>
              </div>
            </div>

            {/* Summary Section */}
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <h3 className="text-lg font-semibold mb-4">Resumo dos Últimos {days} Dias</h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Conformidade Média</span>
                  <span className={`font-semibold ${getComplianceColor(fleetData.complianceRate)}`}>
                    {fleetData.complianceRate}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full" 
                    style={{ width: `${fleetData.complianceRate}%` }}
                  ></div>
                </div>
                
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Verificações Conformes</span>
                  <span className="font-semibold">{fleetData.compliantChecks} / {fleetData.totalChecks}</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-600 h-2 rounded-full" 
                    style={{ width: `${(fleetData.compliantChecks / fleetData.totalChecks) * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Insights Content */}
        {activeTab === 'insights' && insights && (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold">Insights Principais</h3>
                <div className="flex space-x-2 text-sm">
                  <span className="bg-red-100 text-red-800 px-2 py-1 rounded">
                    {insights.highPriorityCount} Alta
                  </span>
                  <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
                    {insights.mediumPriorityCount} Média
                  </span>
                  <span className="bg-green-100 text-green-800 px-2 py-1 rounded">
                    {insights.lowPriorityCount} Baixa
                  </span>
                </div>
              </div>
              
              <div className="space-y-4">
                {insights.insights.slice(0, 5).map((insight, index) => (
                  <div key={index} className={`p-4 border-l-4 rounded-lg ${getPriorityColor(insight.priority)}`}>
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium">{insight.title}</h4>
                      <span className="text-xs px-2 py-1 rounded uppercase font-bold">
                        {insight.priority}
                      </span>
                    </div>
                    <p className="text-sm mb-2">{insight.description}</p>
                    {insight.recommendation && (
                      <p className="text-sm">
                        <strong>Recomendação:</strong> {insight.recommendation}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Vehicles Content */}
        {activeTab === 'vehicles' && (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <h3 className="text-lg font-semibold mb-4">Performance por Veículo</h3>
              
              <div className="space-y-4">
                {vehicles.length > 0 ? vehicles.map((vehicle, index) => (
                  <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <Truck className="h-5 w-5 text-blue-600" />
                      <div>
                        <p className="font-medium">{vehicle.vehiclePlate}</p>
                        <p className="text-sm text-gray-500">{vehicle.totalChecks} verificações</p>
                      </div>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getComplianceColor(vehicle.complianceRate)} bg-opacity-10`}>
                      {vehicle.complianceRate}%
                    </span>
                  </div>
                )) : (
                  <p className="text-gray-500 text-center py-8">Nenhum veículo encontrado</p>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Chat Content */}
        {activeTab === 'chat' && (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <h3 className="text-lg font-semibold mb-4">Pergunte ao Copiloto</h3>
              
              <div className="space-y-4">
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ex: Qual é a taxa de conformidade da frota?"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    onKeyPress={(e) => e.key === 'Enter' && askQuestion()}
                  />
                  <button
                    onClick={askQuestion}
                    disabled={chatLoading || !question.trim()}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    {chatLoading ? <RefreshCw className="h-4 w-4 animate-spin" /> : 'Perguntar'}
                  </button>
                </div>

                {chatResponse && (
                  <div className="p-4 bg-blue-50 border-l-4 border-blue-400 rounded-lg">
                    <p className="text-blue-800">{chatResponse}</p>
                  </div>
                )}

                <div className="text-sm text-gray-500">
                  <p className="font-medium mb-2">Exemplos de perguntas:</p>
                  <ul className="space-y-1">
                    <li>• "Quantos checklists foram feitos esta semana?"</li>
                    <li>• "Quais veículos precisam de atenção?"</li>
                    <li>• "Como está a performance dos motoristas?"</li>
                    <li>• "Há algum problema urgente?"</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App

