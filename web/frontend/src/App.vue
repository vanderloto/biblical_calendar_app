<template>
  <div id="app">
    <header class="header">
      <h1>🌙 Biblical Calendar App</h1>
      <p>Calendário bíblico-lunissolar dinâmico com cálculos astronômicos precisos</p>
    </header>

    <main class="main">
      <div class="controls">
        <div class="control-group">
          <label>Ano:</label>
          <input v-model="year" type="number" min="1" max="2100" />
        </div>
        <div class="control-group">
          <label>
            <input v-model="useVisibility" type="checkbox" />
            Heurística de visibilidade
          </label>
        </div>
        <div class="control-group">
          <label>
            <input v-model="academicMode" type="checkbox" />
            🔬 Modo Acadêmico (DE440)
          </label>
        </div>
        <button @click="generateCalendar" :disabled="loading">
          {{ loading ? 'Gerando...' : 'Gerar Calendário' }}
        </button>
      </div>

      <div v-if="error" class="error">
        {{ error }}
      </div>

      <div v-if="calendarData" class="calendar-info">
        <h2>Calendário {{ calendarData.year }}</h2>
        <div class="info-grid">
          <div class="info-item">
            <strong>Efeméride:</strong> {{ calendarData.ephemeris }}
          </div>
          <div class="info-item">
            <strong>Nissan inicia:</strong> {{ formatDate(calendarData.nissan_start) }}
          </div>
          <div class="info-item">
            <strong>Ano embolísmico:</strong> {{ calendarData.embolismic ? 'Sim (13 meses)' : 'Não (12 meses)' }}
          </div>
        </div>

        <div class="tabs">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="{ active: activeTab === tab.id }"
            class="tab-button"
          >
            {{ tab.name }}
          </button>
        </div>

        <div class="tab-content">
          <div v-if="activeTab === 'months'" class="months-tab">
            <h3>Meses do Ano</h3>
            <table class="months-table">
              <thead>
                <tr>
                  <th>Índice</th>
                  <th>Nome</th>
                  <th>Início</th>
                  <th>Fim</th>
                  <th>Dias</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="month in calendarData.months" :key="month.index">
                  <td>{{ month.index }}</td>
                  <td>{{ month.name }}</td>
                  <td>{{ formatDate(month.start) }}</td>
                  <td>{{ formatDate(month.end) }}</td>
                  <td>{{ month.days }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-if="activeTab === 'festivals'" class="festivals-tab">
            <h3>Festivais e Eventos</h3>
            <div class="festivals-list">
              <div v-for="festival in calendarData.festivals" :key="festival.name" class="festival-item">
                <div class="festival-header">
                  <strong>{{ festival.name }}</strong>
                  <span class="festival-portuguese">({{ festival.portuguese_name }})</span>
                  <span class="festival-date">{{ formatDate(festival.date) }}</span>
                </div>
                <div class="festival-description">{{ festival.description }}</div>
              </div>
            </div>
          </div>

          <div v-if="activeTab === 'seasons'" class="seasons-tab">
            <h3>Estações Astronômicas</h3>
            <div class="seasons-list">
              <div v-for="season in calendarData.seasons" :key="season.event" class="season-item">
                <strong>{{ season.event }}</strong>
                <span class="season-date">{{ formatDateTime(season.utc) }}</span>
              </div>
            </div>
            <div class="current-season">
              <h4>Estação Atual:</h4>
              <p><strong>Jerusalém:</strong> {{ calendarData.current_season.jerusalem }}</p>
              <p><strong>São Paulo:</strong> {{ calendarData.current_season.sao_paulo }}</p>
            </div>
          </div>
        </div>

        <div class="export-buttons">
          <button @click="exportCSV">Exportar CSV</button>
          <button @click="exportICS">Exportar ICS</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'App',
  setup() {
    const year = ref(new Date().getFullYear())
    const useVisibility = ref(false)
    const academicMode = ref(false)
    const loading = ref(false)
    const error = ref('')
    const calendarData = ref(null)
    const activeTab = ref('months')

    const tabs = [
      { id: 'months', name: 'Meses' },
      { id: 'festivals', name: 'Festivais' },
      { id: 'seasons', name: 'Estações' }
    ]

    const generateCalendar = async () => {
      loading.value = true
      error.value = ''
      
      try {
        const params = {
          visibility: useVisibility.value,
          academic: academicMode.value
        }
        
        const response = await axios.get(`/api/calendar/${year.value}`, { params })
        calendarData.value = response.data
      } catch (err) {
        error.value = err.response?.data?.error || 'Erro ao gerar calendário'
      } finally {
        loading.value = false
      }
    }

    const exportCSV = () => {
      const params = new URLSearchParams({
        visibility: useVisibility.value,
        academic: academicMode.value
      })
      window.open(`/api/export/csv/${year.value}?${params}`)
    }

    const exportICS = () => {
      const params = new URLSearchParams({
        visibility: useVisibility.value,
        academic: academicMode.value
      })
      window.open(`/api/export/ics/${year.value}?${params}`)
    }

    const formatDate = (dateStr) => {
      return new Date(dateStr).toLocaleDateString('pt-BR')
    }

    const formatDateTime = (dateTimeStr) => {
      return new Date(dateTimeStr).toLocaleString('pt-BR')
    }

    onMounted(() => {
      generateCalendar()
    })

    return {
      year,
      useVisibility,
      academicMode,
      loading,
      error,
      calendarData,
      activeTab,
      tabs,
      generateCalendar,
      exportCSV,
      exportICS,
      formatDate,
      formatDateTime
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #f5f7fa;
  color: #333;
}

#app {
  min-height: 100vh;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  text-align: center;
}

.header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.controls {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.control-group input[type="number"] {
  width: 80px;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

button:hover {
  background: #5a6fd8;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error {
  background: #fee;
  color: #c33;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.calendar-info {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  overflow: hidden;
}

.calendar-info h2 {
  background: #f8f9fa;
  padding: 1rem;
  margin: 0;
  border-bottom: 1px solid #eee;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-bottom: 1px solid #eee;
}

.info-item {
  padding: 0.5rem;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #eee;
}

.tab-button {
  background: none;
  border: none;
  padding: 1rem 2rem;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  color: #666;
}

.tab-button.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

.tab-content {
  padding: 2rem;
}

.months-table {
  width: 100%;
  border-collapse: collapse;
}

.months-table th,
.months-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.months-table th {
  background: #f8f9fa;
  font-weight: 600;
}

.festivals-list {
  display: grid;
  gap: 1rem;
}

.festival-item {
  border: 1px solid #eee;
  border-radius: 4px;
  padding: 1rem;
}

.festival-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.festival-portuguese {
  color: #666;
  font-style: italic;
}

.festival-date {
  margin-left: auto;
  background: #667eea;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
}

.festival-description {
  color: #666;
  line-height: 1.5;
}

.seasons-list {
  display: grid;
  gap: 1rem;
  margin-bottom: 2rem;
}

.season-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 4px;
}

.season-date {
  color: #666;
  font-family: monospace;
}

.current-season {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
}

.export-buttons {
  padding: 1rem;
  border-top: 1px solid #eee;
  display: flex;
  gap: 1rem;
}

.export-buttons button {
  background: #28a745;
}

.export-buttons button:hover {
  background: #218838;
}
</style>