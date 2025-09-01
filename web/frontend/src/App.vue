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

        <div class="calendar-visual">
          <div class="calendar-header">
            <button @click="previousMonth" class="nav-button">◀ Anterior</button>
            <h3>{{ currentMonthName }} ({{ currentMonth.days }} dias)</h3>
            <button @click="nextMonth" class="nav-button">Próximo ▶</button>
          </div>
          
          <div class="calendar-grid">
            <div class="weekday" v-for="day in weekdays" :key="day">{{ day }}</div>
            <div 
              v-for="day in calendarDays" 
              :key="day.date"
              :class="['calendar-day', { 'today': day.isToday, 'other-month': !day.inMonth }]"
              @click="selectDay(day)"
            >
              <div class="day-number">{{ day.dayNumber }}</div>
              <div class="day-events">
                <span v-for="event in day.events" :key="event" class="event-icon">{{ event }}</span>
              </div>
            </div>
          </div>
          
          <div class="day-details" v-if="selectedDay">
            <h4>{{ formatDate(selectedDay.date) }}</h4>
            <div class="day-info">
              <div v-for="festival in getDayFestivals(selectedDay)" :key="festival.name" class="festival-detail">
                <strong>★ {{ festival.name }}</strong> ({{ festival.portuguese_name }})
                <p>{{ festival.description }}</p>
              </div>
              <div class="season-info">
                <strong>Estação:</strong> 
                Jerusalém: {{ calendarData.current_season.jerusalem }} | 
                São Paulo: {{ calendarData.current_season.sao_paulo }}
              </div>
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
import { ref, computed, onMounted } from 'vue'
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
    const currentMonthIndex = ref(0)
    const selectedDay = ref(null)
    
    const weekdays = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']

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

    const currentMonth = computed(() => {
      return calendarData.value?.months[currentMonthIndex.value] || {}
    })
    
    const currentMonthName = computed(() => {
      const month = currentMonth.value
      return month.name ? `${month.name} (${month.index})` : ''
    })
    
    const calendarDays = computed(() => {
      if (!currentMonth.value.start) return []
      
      const startDate = new Date(currentMonth.value.start)
      const endDate = new Date(currentMonth.value.end)
      const days = []
      
      // Add days from previous month to fill first week
      const firstDayOfWeek = startDate.getDay()
      for (let i = firstDayOfWeek - 1; i >= 0; i--) {
        const date = new Date(startDate)
        date.setDate(date.getDate() - i - 1)
        days.push({
          date: date.toISOString().split('T')[0],
          dayNumber: date.getDate(),
          inMonth: false,
          isToday: false,
          events: []
        })
      }
      
      // Add days of current month
      const currentDate = new Date(startDate)
      while (currentDate <= endDate) {
        const dateStr = currentDate.toISOString().split('T')[0]
        const dayEvents = getDayEvents(dateStr)
        
        days.push({
          date: dateStr,
          dayNumber: currentDate.getDate(),
          inMonth: true,
          isToday: dateStr === new Date().toISOString().split('T')[0],
          events: dayEvents
        })
        
        currentDate.setDate(currentDate.getDate() + 1)
      }
      
      // Add days from next month to fill last week
      while (days.length % 7 !== 0) {
        const date = new Date(currentDate)
        days.push({
          date: date.toISOString().split('T')[0],
          dayNumber: date.getDate(),
          inMonth: false,
          isToday: false,
          events: []
        })
        currentDate.setDate(currentDate.getDate() + 1)
      }
      
      return days
    })
    
    const getDayEvents = (dateStr) => {
      const events = []
      
      // Check for festivals
      calendarData.value?.festivals.forEach(festival => {
        if (festival.date === dateStr) {
          events.push('★')
        }
      })
      
      // Check for seasons
      calendarData.value?.seasons.forEach(season => {
        if (season.utc.split('T')[0] === dateStr) {
          events.push('🌍')
        }
      })
      
      return events
    }
    
    const getDayFestivals = (day) => {
      return calendarData.value?.festivals.filter(f => f.date === day.date) || []
    }
    
    const selectDay = (day) => {
      selectedDay.value = day
    }
    
    const previousMonth = () => {
      if (currentMonthIndex.value > 0) {
        currentMonthIndex.value--
      }
    }
    
    const nextMonth = () => {
      if (calendarData.value && currentMonthIndex.value < calendarData.value.months.length - 1) {
        currentMonthIndex.value++
      }
    }

    return {
      year,
      useVisibility,
      academicMode,
      loading,
      error,
      calendarData,
      currentMonthIndex,
      selectedDay,
      weekdays,
      currentMonth,
      currentMonthName,
      calendarDays,
      generateCalendar,
      exportCSV,
      exportICS,
      formatDate,
      formatDateTime,
      getDayFestivals,
      selectDay,
      previousMonth,
      nextMonth
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

.calendar-visual {
  padding: 2rem;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.nav-button {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.nav-button:hover {
  background: #5a6fd8;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  background: #ddd;
  border: 1px solid #ddd;
  margin-bottom: 2rem;
}

.weekday {
  background: #f8f9fa;
  padding: 1rem;
  text-align: center;
  font-weight: 600;
  color: #666;
}

.calendar-day {
  background: white;
  padding: 0.5rem;
  min-height: 80px;
  cursor: pointer;
  border: 2px solid transparent;
}

.calendar-day:hover {
  background: #f8f9fa;
}

.calendar-day.today {
  background: #e3f2fd;
  border-color: #2196f3;
}

.calendar-day.other-month {
  background: #f5f5f5;
  color: #ccc;
}

.day-number {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.day-events {
  display: flex;
  gap: 0.25rem;
  flex-wrap: wrap;
}

.event-icon {
  font-size: 0.8rem;
}

.day-details {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 4px;
  border: 1px solid #eee;
}

.day-info {
  margin-top: 1rem;
}

.festival-detail {
  margin-bottom: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 4px;
  border-left: 4px solid #667eea;
}

.festival-detail p {
  margin-top: 0.5rem;
  color: #666;
  line-height: 1.5;
}

.season-info {
  padding: 1rem;
  background: white;
  border-radius: 4px;
  border-left: 4px solid #28a745;
  color: #666;
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