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

        <div class="visual-calendar">
          <div class="calendar-header">
            <button @click="previousMonth" class="nav-btn">◀ Anterior</button>
            <div class="month-info">
              <div class="info-columns">
                <div class="left-column">
                  <h3>Mês {{ currentMonth.index }} - {{ currentMonth.name }}</h3>
                  <p>{{ formatDate(currentMonth.start) }} - {{ currentMonth.days }} dias</p>
                  <!-- DEBUG: {{ currentMonth.start }} -->
                  <div class="chronologies">
                    <strong>Cronologias do Ano:</strong><br>
                    <span class="chrono-item">Ussher: {{ chronologies.ussher }} AM (desde Criação)</span><br>
                    <span class="chrono-item">Hebraico: {{ chronologies.hebrew }} AM (Anno Mundi)</span><br>
                    <span class="chrono-item">Gregoriano: {{ chronologies.gregorian }} DC (Era Cristã)</span>
                  </div>
                  <div class="current-season">
                    <strong>🌍 Estação Atual:</strong><br>
                    <span class="season-item">Jerusalém: {{ currentSeason.jerusalem }}</span><br>
                    <span class="season-item">São Paulo: {{ currentSeason.sao_paulo }}</span>
                  </div>
                </div>
                <div class="right-column">
                  <div class="legend">
                    <h4>Legenda:</h4>
                    <div class="legend-item">🌑 Lua Nova</div>
                    <div class="legend-item">🌓 Lua Crescente</div>
                    <div class="legend-item">🌕 Lua Cheia</div>
                    <div class="legend-item">🌗 Lua Minguante</div>
                    <div class="legend-item">★ Festival</div>
                    <div class="legend-item">🌍 Estação Astronômica</div>
                    <div class="legend-item">Fundo azul = Hoje</div>
                  </div>
                </div>
              </div>
            </div>
            <button @click="nextMonth" class="nav-btn">Próximo ▶</button>
            <button @click="goToToday" class="today-btn">Hoje</button>
          </div>

          <div class="calendar-container">
            <div class="calendar-grid">
              <div class="weekday-header" v-for="day in weekdays" :key="day">{{ day }}</div>
              
              <!-- Empty cells for days before month start -->
              <div v-for="n in startWeekday" :key="'empty-' + n" class="day-cell empty"></div>
              
              <div 
                v-for="(day, index) in calendarDays" 
                :key="index"
                :class="['day-cell', { 
                  'today': day.isToday, 
                  'has-events': day.events.length > 0,
                  'selected': selectedDay && selectedDay.dayInMonth === day.dayInMonth
                }]"
                @click="selectDay(day)"
              >
                <div class="day-number">{{ day.dayInMonth }}</div>
                <div class="gregorian-date">({{ day.gregorianDate }})</div>
                <div class="day-events">
                  <div v-for="event in day.events" :key="event.type" class="event-marker">
                    {{ event.icon }}
                  </div>
                </div>
              </div>
            </div>

            <div class="events-panel">
              <div class="day-details" v-if="selectedDay">
                <h4>Eventos do Dia:</h4>
                <div class="selected-day-info">
                  <strong>Dia {{ selectedDay.dayInMonth }} ({{ selectedDay.gregorianDate }})</strong>
                </div>

                <div v-if="selectedDay.events.length > 0" class="events-list">
                  <div v-for="event in selectedDay.events" :key="event.name" class="event-detail">
                    <div class="event-header">
                      <strong>{{ event.icon }} {{ event.name }}</strong>
                      <span v-if="event.portuguese" class="portuguese-name">({{ event.portuguese }})</span>
                    </div>
                    <div v-if="event.description" class="event-description">
                      {{ event.description }}
                    </div>
                  </div>
                </div>
                
                <div v-else class="no-events">
                  Nenhum evento especial.
                </div>
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
        
        const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || '/api'
        const response = await axios.get(`${apiBaseUrl}/calendar/${year.value}`, { 
          params,
          headers: { 'Cache-Control': 'no-cache' }
        })
        
        // Debug: check Elul date
        const elulMonth = response.data.months.find(m => m.name === 'Elul')
        console.log('DEBUG: Elul received from API:', elulMonth)
        
        calendarData.value = response.data
        
        // Set current month and select today if it's the current year
        const today = new Date()
        const todayStr = today.toISOString().split('T')[0]
        
        if (year.value === today.getFullYear() && calendarData.value.months) {
          for (let i = 0; i < calendarData.value.months.length; i++) {
            const month = calendarData.value.months[i]
            if (todayStr >= month.start && todayStr <= month.end) {
              currentMonthIndex.value = i
              const startDate = new Date(month.start)
              const dayOfMonth = Math.floor((today - startDate) / (1000 * 60 * 60 * 24)) + 1
              selectedDay.value = {
                dayInMonth: dayOfMonth,
                gregorianDate: today.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' }),
                date: todayStr,
                isToday: true,
                events: getDayEvents(dayOfMonth, todayStr)
              }
              break
            }
          }
        }
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
      const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || '/api'
      window.open(`${apiBaseUrl}/export/csv/${year.value}?${params}`)
    }

    const exportICS = () => {
      const params = new URLSearchParams({
        visibility: useVisibility.value,
        academic: academicMode.value
      })
      const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || '/api'
      window.open(`${apiBaseUrl}/export/ics/${year.value}?${params}`)
    }

    const formatDate = (dateStr) => {
      if (!dateStr) return 'N/A'
      
      // Parse as local date to avoid timezone conversion
      const [year, month, day] = dateStr.split('-').map(Number)
      const date = new Date(year, month - 1, day)
      
      if (isNaN(date.getTime())) return 'Invalid Date'
      return date.toLocaleDateString('pt-BR')
    }

    const formatDateTime = (dateTimeStr) => {
      return new Date(dateTimeStr).toLocaleString('pt-BR')
    }

    onMounted(() => {
      year.value = new Date().getFullYear()
      generateCalendar()
    })

    const currentMonth = computed(() => {
      if (!calendarData.value || !calendarData.value.months || !calendarData.value.months.length) {
        return {}
      }
      return calendarData.value.months[currentMonthIndex.value] || {}
    })
    
    const chronologies = computed(() => {
      if (!currentMonth.value || !currentMonth.value.start) return { ussher: 0, hebrew: 0, gregorian: 0 }
      const date = new Date(currentMonth.value.start)
      if (isNaN(date.getTime())) return { ussher: 0, hebrew: 0, gregorian: 0 }
      const gregorianYear = date.getFullYear()
      return {
        ussher: gregorianYear + 4004,
        hebrew: gregorianYear + 3760,
        gregorian: gregorianYear
      }
    })
    
    const startWeekday = computed(() => {
      if (!currentMonth.value || !currentMonth.value.start) return 0
      
      // Calculate day of week for first day of month (Saturday = 6)
      const [year, month, day] = currentMonth.value.start.split('-').map(Number)
      const date = new Date(Date.UTC(year, month - 1, day))
      return date.getUTCDay() // Sunday=0, Monday=1, ..., Saturday=6
    })
    
    const calendarDays = computed(() => {
      if (!currentMonth.value || !currentMonth.value.start || !currentMonth.value.days) return []
      
      const days = []
      const today = new Date().toISOString().split('T')[0]
      
      // Parse start date components
      const [startYear, startMonth, startDay] = currentMonth.value.start.split('-').map(Number)
      
      // Add days of current month
      for (let d = 1; d <= currentMonth.value.days; d++) {
        // Calculate current date by adding days to start date
        const currentDate = new Date(Date.UTC(startYear, startMonth - 1, startDay + d - 1))
        const dateStr = currentDate.toISOString().split('T')[0]
        
        // Format gregorian date from dateStr to avoid timezone issues
        const [year, month, day] = dateStr.split('-').map(Number)
        const gregorianDate = `${day.toString().padStart(2, '0')}/${month.toString().padStart(2, '0')}`
        
        const dayEvents = getDayEvents(d, dateStr)
        
        days.push({
          dayInMonth: d,
          gregorianDate: gregorianDate,
          date: dateStr,
          isToday: dateStr === today,
          events: dayEvents
        })
      }
      
      return days
    })
    
    const getDayEvents = (dayInMonth, dateStr) => {
      if (!calendarData.value) return []
      
      const events = []
      
      // New moon on day 1
      if (dayInMonth === 1) {
        events.push({ type: 'new_moon', icon: '🌑', name: 'Lua Nova', description: 'Início do mês bíblico baseado na conjunção astronômica Sol-Lua.' })
      }
      
      // Check for festivals
      if (calendarData.value.festivals) {
        calendarData.value.festivals.forEach(festival => {
          if (festival.date === dateStr) {
            events.push({
              type: 'festival',
              icon: '★',
              name: festival.name,
              portuguese: festival.portuguese_name,
              description: festival.description
            })
          }
        })
      }
      
      // Check for seasons
      if (calendarData.value.seasons) {
        calendarData.value.seasons.forEach(season => {
          if (season.utc && season.utc.split('T')[0] === dateStr) {
            events.push({
              type: 'season',
              icon: '🌍',
              name: season.event,
              description: getSeasonDescription(season.event)
            })
          }
        })
      }
      
      return events
    };
    
    const getSeasonDescription = (event) => {
      const descriptions = {
        'March Equinox': 'Em Jerusalém, marca o início da primavera (Hemisfério Norte). Em São Paulo, marca o início do outono (Hemisfério Sul)',
        'June Solstice': 'Em Jerusalém, marca o início do verão (Hemisfério Norte). Em São Paulo, marca o início do inverno (Hemisfério Sul)',
        'September Equinox': 'Em Jerusalém, marca o início do outono (Hemisfério Norte). Em São Paulo, marca o início da primavera (Hemisfério Sul)',
        'December Solstice': 'Em Jerusalém, marca o início do inverno (Hemisfério Norte). Em São Paulo, marca o início do verão (Hemisfério Sul)'
      }
      return descriptions[event] || ''
    }
    
    const selectDay = (day) => {
      selectedDay.value = day
    }
    
    const previousMonth = async () => {
      if (currentMonthIndex.value > 0) {
        currentMonthIndex.value--
        selectedDay.value = null
      } else {
        // Move to previous year, last month
        year.value--
        await generateCalendar()
        if (calendarData.value) {
          currentMonthIndex.value = calendarData.value.months.length - 1
          selectedDay.value = null
        }
      }
    }
    
    const nextMonth = async () => {
      if (calendarData.value && currentMonthIndex.value < calendarData.value.months.length - 1) {
        currentMonthIndex.value++
        selectedDay.value = null
      } else {
        // Move to next year, first month
        year.value++
        await generateCalendar()
        currentMonthIndex.value = 0
        selectedDay.value = null
      }
    }
    
    const goToToday = async () => {
      const today = new Date()
      const currentYear = today.getFullYear()
      const todayStr = today.toISOString().split('T')[0]
      
      if (year.value !== currentYear) {
        year.value = currentYear
        await generateCalendar()
      }
      
      if (calendarData.value) {
        for (let i = 0; i < calendarData.value.months.length; i++) {
          const month = calendarData.value.months[i]
          if (todayStr >= month.start && todayStr <= month.end) {
            currentMonthIndex.value = i
            // Find and select today's day
            const startDate = new Date(month.start)
            const dayOfMonth = Math.floor((today - startDate) / (1000 * 60 * 60 * 24)) + 1
            selectedDay.value = {
              dayInMonth: dayOfMonth,
              gregorianDate: today.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' }),
              date: todayStr,
              isToday: true,
              events: getDayEvents(dayOfMonth, todayStr)
            }
            break
          }
        }
      }
    }

    const currentSeason = computed(() => {
      if (!calendarData.value || !calendarData.value.seasons) return { jerusalem: 'N/A', sao_paulo: 'N/A' }
      
      // Use selected day if available, otherwise current month's first day
      let referenceDate
      if (selectedDay.value) {
        referenceDate = selectedDay.value.date
      } else if (currentMonth.value.start) {
        referenceDate = currentMonth.value.start.split('T')[0]
      } else {
        referenceDate = new Date().toISOString().split('T')[0]
      }
      
      const seasons = calendarData.value.seasons
      let current = null
      
      for (let i = 0; i < seasons.length; i++) {
        const seasonDate = seasons[i].utc.split('T')[0]
        if (i < seasons.length - 1) {
          const nextSeasonDate = seasons[i + 1].utc.split('T')[0]
          if (seasonDate <= referenceDate && referenceDate < nextSeasonDate) {
            current = seasons[i].event
            break
          }
        } else {
          if (seasonDate <= referenceDate) {
            current = seasons[i].event
            break
          }
        }
      }
      
      if (!current && seasons.length > 0) {
        current = 'December Solstice'
      }
      
      const seasonMap = {
        'March Equinox': { jerusalem: 'Primavera', sao_paulo: 'Outono' },
        'June Solstice': { jerusalem: 'Verão', sao_paulo: 'Inverno' },
        'September Equinox': { jerusalem: 'Outono', sao_paulo: 'Primavera' },
        'December Solstice': { jerusalem: 'Inverno', sao_paulo: 'Verão' }
      }
      
      return seasonMap[current] || { jerusalem: 'N/A', sao_paulo: 'N/A' }
    })

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
      chronologies,
      calendarDays,
      startWeekday,
      currentSeason,
      generateCalendar,
      exportCSV,
      exportICS,
      formatDate,
      formatDateTime,
      selectDay,
      previousMonth,
      nextMonth,
      goToToday
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

.visual-calendar {
  padding: 1rem;
}

.calendar-header {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.nav-btn, .today-btn {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.nav-btn:hover, .today-btn:hover {
  background: #5a6fd8;
}

.today-btn {
  background: #28a745;
}

.today-btn:hover {
  background: #218838;
}

.month-info {
  flex: 1;
}

.info-columns {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
}

.left-column {
  flex: 1;
  text-align: center;
}

.right-column {
  flex: 0 0 200px;
  text-align: left;
}

.month-info h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.month-info p {
  margin: 0 0 1rem 0;
  color: #666;
  font-size: 0.9rem;
}

.chronologies {
  font-size: 0.8rem;
  color: #666;
  line-height: 1.4;
  margin-bottom: 1rem;
}

.chrono-item {
  display: inline-block;
  margin-right: 1rem;
}

.current-season {
  font-size: 0.8rem;
  color: #666;
  line-height: 1.4;
  padding: 0.5rem;
  background: #e8f5e8;
  border-radius: 4px;
  border-left: 3px solid #28a745;
}

.season-item {
  display: inline-block;
  margin-right: 1rem;
}

.calendar-container {
  display: flex;
  gap: 2rem;
}

.calendar-grid {
  flex: 2;
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  background: #ddd;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
}

.weekday-header {
  background: #667eea;
  color: white;
  padding: 0.75rem;
  text-align: center;
  font-weight: 600;
  font-size: 0.9rem;
}

.day-cell {
  background: white;
  padding: 0.5rem;
  min-height: 100px;
  cursor: pointer;
  border: 2px solid transparent;
  position: relative;
}

.day-cell:hover {
  background: #f8f9fa;
}

.day-cell.today {
  background: lightblue;
}

.day-cell.selected {
  border-color: #667eea;
  background: #e3f2fd;
}

.day-cell.has-events {
  background: #fff8e1;
}

.day-number {
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
}

.gregorian-date {
  font-size: 0.75rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.day-events {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.event-marker {
  font-size: 1rem;
  line-height: 1;
}

.events-panel {
  flex: 1;
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  max-height: 600px;
  overflow-y: auto;
}

.legend {
  margin-bottom: 2rem;
}

.legend h4 {
  margin: 0 0 1rem 0;
  color: #333;
}

.legend-item {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #666;
}

.day-details h4 {
  margin: 0 0 1rem 0;
  color: #333;
  border-bottom: 2px solid #667eea;
  padding-bottom: 0.5rem;
}

.selected-day-info {
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.season-info {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #e8f5e8;
  border-radius: 4px;
  border-left: 4px solid #28a745;
  font-size: 0.9rem;
  line-height: 1.5;
}

.events-list {
  margin-top: 1rem;
}

.event-detail {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #fff8e1;
  border-radius: 4px;
  border-left: 4px solid #ff9800;
}

.event-header {
  margin-bottom: 0.5rem;
}

.portuguese-name {
  color: #666;
  font-style: italic;
  font-weight: normal;
}

.event-description {
  color: #555;
  line-height: 1.5;
  font-size: 0.9rem;
}

.no-events {
  color: #999;
  font-style: italic;
  text-align: center;
  padding: 2rem;
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