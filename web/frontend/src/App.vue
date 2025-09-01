<template>
  <div class="container">
    <!-- Header Controls -->
    <div class="header">
      <div class="controls">
        <div class="input-group">
          <label for="year">Ano referência:</label>
          <input 
            id="year" 
            v-model.number="year" 
            type="number" 
            min="1" 
            max="2100"
            @keyup.enter="generateCalendar"
          />
        </div>
        
        <div class="checkbox-group">
          <input 
            id="visibility" 
            v-model="useVisibility" 
            type="checkbox"
          />
          <label for="visibility">Heurística visibilidade (Jerusalém)</label>
        </div>
        
        <div class="checkbox-group">
          <input 
            id="academic" 
            v-model="academicMode" 
            type="checkbox"
          />
          <label for="academic">🔬 Modo Pesquisa Acadêmica (DE440)</label>
        </div>
        
        <button @click="generateCalendar" :disabled="loading">
          {{ loading ? 'Gerando...' : 'Gerar' }}
        </button>
        
        <button @click="exportCSV" :disabled="!calendarData">
          Exportar CSV
        </button>
        
        <button @click="exportICS" :disabled="!calendarData">
          Exportar ICS
        </button>
      </div>
      
      <div class="status-info" v-if="calendarData">
        Efeméride: {{ calendarData.ephemeris }}
      </div>
    </div>

    <!-- Error Display -->
    <div v-if="error" class="error">
      {{ error }}
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading">
      <div>Calculando calendário bíblico...</div>
      <div style="margin-top: 10px; font-size: 14px;">
        Isso pode levar alguns segundos para download de efemérides.
      </div>
    </div>

    <!-- Main Content -->
    <div v-if="calendarData && !loading" class="main-content">
      <!-- Calendar Section -->
      <div class="calendar-section">
        <div class="calendar-header">
          <div>
            <div class="calendar-title">
              Mês {{ currentMonth?.index }} - {{ currentMonth?.name }}
            </div>
            <div style="font-size: 14px; color: #718096; margin-top: 5px;">
              <strong>Inicia em:</strong> {{ currentMonth?.start }} ({{ currentMonth?.days }} dias)
            </div>
            <div style="font-size: 12px; color: #718096; margin-top: 5px;">
              <div><strong>Cronologias do Ano:</strong></div>
              <div style="margin-left: 10px;">Ussher: {{ ussherYear }} AM (desde Criação)</div>
              <div style="margin-left: 10px;">Hebraico: {{ hebrewYear }} AM (Anno Mundi)</div>
              <div style="margin-left: 10px;">Gregoriano: {{ year }} DC (Era Cristã)</div>
            </div>
            <div v-if="currentSeasonForDate" style="font-size: 12px; color: #2d3748; margin-top: 5px; font-weight: 500;">
              <strong>Estação Astronômica:</strong> 🌍 Jerusalém: {{ currentSeasonForDate.jerusalem }} | São Paulo: {{ currentSeasonForDate.sao_paulo }}
            </div>
          </div>
          <div class="nav-buttons">
            <button class="nav-button" @click="previousMonth">◀ Anterior</button>
            <button class="nav-button" @click="goToToday">Hoje</button>
            <button class="nav-button" @click="nextMonth">Próximo ▶</button>
          </div>
        </div>
        
        <div class="calendar-grid">
          <div class="day-header" v-for="day in weekDays" :key="day">{{ day }}</div>
          <div 
            v-for="day in calendarDays" 
            :key="day.key"
            class="day-cell"
            :class="{ today: day.isToday }"
            @click="selectDay(day)"
          >
            <div v-if="day.dayNumber">
              <div class="day-number">{{ day.dayNumber }}</div>
              <div class="day-greg">({{ day.gregDate }})</div>
              <div class="day-events">
                <div 
                  v-for="event in day.events" 
                  :key="event.name"
                  class="event-indicator"
                >
                  {{ event.icon }} {{ event.shortName }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Events Panel -->
      <div class="events-section">
        <div class="events-title">
          {{ selectedDay ? `Eventos do Dia ${selectedDay.dayNumber}` : 'Eventos do Dia' }}
        </div>
        <div class="events-panel">
          <div v-if="selectedDay && selectedDay.fullEvents.length > 0">
            <div class="event-item" v-for="event in selectedDay.fullEvents" :key="event.name">
              <div class="event-name">{{ event.displayName }}</div>
              <div class="event-description" v-if="event.description" style="white-space: pre-line;">
                {{ event.description }}
              </div>
            </div>
          </div>
          <div v-else-if="selectedDay">
            Nenhum evento especial neste dia.
          </div>
          <div v-else>
            Clique em um dia para ver os eventos.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'BiblicalCalendarApp',
  setup() {
    // Reactive state
    const year = ref(new Date().getFullYear())
    const useVisibility = ref(false)
    const academicMode = ref(false)
    const loading = ref(false)
    const error = ref('')
    const calendarData = ref(null)
    const currentMonthIndex = ref(0)
    const selectedDay = ref(null)

    // Constants
    const weekDays = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
    const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'

    // Computed properties
    const currentMonth = computed(() => {
      if (!calendarData.value) return null
      return calendarData.value.months[currentMonthIndex.value]
    })

    const ussherYear = computed(() => year.value + 4004)
    const hebrewYear = computed(() => year.value + 3760)

    const currentSeasonForDate = computed(() => {
      if (!calendarData.value) return null
      
      let referenceDate
      
      if (selectedDay.value) {
        // Use selected day
        referenceDate = selectedDay.value.date
      } else if (currentMonth.value) {
        // Use first day of current month
        referenceDate = new Date(currentMonth.value.start + 'T00:00:00Z')
      } else {
        // Fallback to today
        referenceDate = new Date()
      }
      
      return getCurrentSeasonForDate(referenceDate)
    })

    const getCurrentSeasonForDate = (targetDate) => {
      if (!calendarData.value) return null
      
      // Find the current season based on the target date
      let currentSeason = null
      const seasons = calendarData.value.seasons
      
      for (let i = 0; i < seasons.length; i++) {
        const seasonDate = new Date(seasons[i].utc)
        if (i < seasons.length - 1) {
          const nextSeasonDate = new Date(seasons[i + 1].utc)
          if (seasonDate <= targetDate && targetDate < nextSeasonDate) {
            currentSeason = seasons[i].event
            break
          }
        } else {
          // Last season of the year, check if date is after it
          if (seasonDate <= targetDate) {
            currentSeason = seasons[i].event
            break
          }
        }
      }
      
      // If no season found, it might be before March equinox (winter from previous year)
      if (!currentSeason && seasons.length > 0) {
        currentSeason = "December Solstice"  // Winter in Northern Hemisphere
      }
      
      if (currentSeason) {
        const seasonMap = {
          "March Equinox": {"jerusalem": "Primavera", "sao_paulo": "Outono"},
          "June Solstice": {"jerusalem": "Verão", "sao_paulo": "Inverno"},
          "September Equinox": {"jerusalem": "Outono", "sao_paulo": "Primavera"},
          "December Solstice": {"jerusalem": "Inverno", "sao_paulo": "Verão"}
        }
        return seasonMap[currentSeason] || {"jerusalem": "N/A", "sao_paulo": "N/A"}
      }
      
      return null
    }

    const calendarDays = computed(() => {
      if (!currentMonth.value) return []
      
      const startDate = new Date(currentMonth.value.start + 'T00:00:00Z')
      const days = currentMonth.value.days
      const startWeekday = startDate.getUTCDay()
      
      const calendarDays = []
      
      // Empty cells before month start
      for (let i = 0; i < startWeekday; i++) {
        calendarDays.push({ key: `empty-${i}` })
      }
      
      // Month days
      for (let day = 1; day <= days; day++) {
        const currentDate = new Date(startDate.getTime())
        currentDate.setUTCDate(startDate.getUTCDate() + day - 1)
        
        const gregDate = currentDate.toLocaleDateString('pt-BR', { 
          day: '2-digit', 
          month: '2-digit',
          timeZone: 'UTC'
        })
        
        const isToday = currentDate.toDateString() === new Date().toDateString()
        
        // Find events for this day
        const dayEvents = findEventsForDay(day, currentDate)
        
        calendarDays.push({
          key: `day-${day}`,
          dayNumber: day,
          gregDate,
          isToday,
          date: currentDate,
          events: dayEvents.map(e => ({
            ...e,
            shortName: e.name.length > 10 ? e.name.substring(0, 10) + '...' : e.name
          })),
          fullEvents: dayEvents
        })
      }
      
      return calendarDays
    })

    // Methods
    const generateCalendar = async () => {
      loading.value = true
      error.value = ''
      
      try {
        const response = await axios.get(`${API_BASE}/calendar/${year.value}`, {
          params: {
            visibility: useVisibility.value,
            academic: academicMode.value
          }
        })
        
        calendarData.value = response.data
        
        // Find current month and select today
        const today = new Date()
        let foundToday = false
        
        for (let i = 0; i < response.data.months.length; i++) {
          const month = response.data.months[i]
          const startDate = new Date(month.start + 'T00:00:00Z')
          const endDate = new Date(month.end + 'T00:00:00Z')
          
          if (today >= startDate && today <= endDate) {
            currentMonthIndex.value = i
            foundToday = true
            
            // Calculate which day of the biblical month today is
            const daysDiff = Math.floor((today - startDate) / (1000 * 60 * 60 * 24)) + 1
            
            // Find and select today in the calendar days (will be set after computed runs)
            setTimeout(() => {
              const todayDay = calendarDays.value.find(day => day.isToday)
              if (todayDay) {
                selectedDay.value = todayDay
              }
            }, 0)
            
            break
          }
        }
        
        if (!foundToday) {
          currentMonthIndex.value = 0
          selectedDay.value = null
        }
        
      } catch (err) {
        error.value = `Erro ao gerar calendário: ${err.response?.data?.error || err.message}`
      } finally {
        loading.value = false
      }
    }

    const findEventsForDay = (day, date) => {
      if (!calendarData.value) return []
      
      const events = []
      const monthIndex = currentMonthIndex.value + 1
      
      // Check festivals
      calendarData.value.festivals.forEach(festival => {
        const festivalDate = new Date(festival.date + 'T00:00:00Z')
        if (festivalDate.toDateString() === date.toDateString()) {
          events.push({
            name: festival.name,
            displayName: `★ ${festival.name} (${festival.portuguese_name})`,
            description: festival.description,
            icon: '★',
            type: 'festival'
          })
        }
      })
      
      // Check for new moon (day 1)
      if (day === 1) {
        events.push({
          name: 'Lua Nova',
          displayName: '🌑 Lua Nova',
          description: 'Início do mês bíblico baseado na conjunção astronômica Sol-Lua.',
          icon: '🌑',
          type: 'moon'
        })
      }
      
      // Check seasons
      calendarData.value.seasons.forEach(season => {
        const seasonDate = new Date(season.utc)
        if (seasonDate.toDateString() === date.toDateString()) {
          events.push({
            name: season.event,
            displayName: `🌍 ${season.event}`,
            description: getSeasonDescription(season.event),
            icon: '🌍',
            type: 'season'
          })
        }
      })
      
      return events
    }

    const getSeasonDescription = (event) => {
      const descriptions = {
        'March Equinox': `Jerusalém: início da primavera (Hemisfério Norte)
São Paulo: início do outono (Hemisfério Sul)`,
        'June Solstice': `Jerusalém: início do verão (Hemisfério Norte)
São Paulo: início do inverno (Hemisfério Sul)`,
        'September Equinox': `Jerusalém: início do outono (Hemisfério Norte)
São Paulo: início da primavera (Hemisfério Sul)`,
        'December Solstice': `Jerusalém: início do inverno (Hemisfério Norte)
São Paulo: início do verão (Hemisfério Sul)`
      }
      return descriptions[event] || ''
    }

    const selectDay = (day) => {
      if (day.dayNumber) {
        selectedDay.value = day
      }
    }

    const previousMonth = () => {
      if (currentMonthIndex.value > 0) {
        currentMonthIndex.value--
        selectedDay.value = null
      } else if (currentMonthIndex.value === 0) {
        // First month, go to previous year
        if (year.value > 1) {
          year.value--
          generateCalendar().then(() => {
            // Go to last month of previous year
            if (calendarData.value) {
              currentMonthIndex.value = calendarData.value.months.length - 1
            }
          })
        }
      }
    }

    const nextMonth = () => {
      if (calendarData.value && currentMonthIndex.value < calendarData.value.months.length - 1) {
        currentMonthIndex.value++
        selectedDay.value = null
      } else if (calendarData.value && currentMonthIndex.value === calendarData.value.months.length - 1) {
        // Last month, go to next year
        if (year.value < 2100) {
          year.value++
          generateCalendar()
        }
      }
    }

    const goToToday = () => {
      const today = new Date()
      const currentYear = today.getFullYear()
      
      // If not in current year, change year and regenerate calendar
      if (year.value !== currentYear) {
        year.value = currentYear
        generateCalendar()
        return
      }
      
      // If already in current year, just navigate to today's month
      if (!calendarData.value) return
      
      for (let i = 0; i < calendarData.value.months.length; i++) {
        const month = calendarData.value.months[i]
        const startDate = new Date(month.start + 'T00:00:00Z')
        const endDate = new Date(month.end + 'T00:00:00Z')
        
        if (today >= startDate && today <= endDate) {
          currentMonthIndex.value = i
          
          // Select today after calendar renders
          setTimeout(() => {
            const todayDay = calendarDays.value.find(day => day.isToday)
            if (todayDay) {
              selectedDay.value = todayDay
            }
          }, 0)
          
          break
        }
      }
    }

    const exportCSV = async () => {
      try {
        const response = await axios.get(`${API_BASE}/export/csv/${year.value}`, {
          params: {
            visibility: useVisibility.value,
            academic: academicMode.value
          },
          responseType: 'blob'
        })
        
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `biblical_calendar_${year.value}.csv`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        
      } catch (err) {
        error.value = `Erro ao exportar CSV: ${err.message}`
      }
    }

    const exportICS = async () => {
      try {
        const response = await axios.get(`${API_BASE}/export/ics/${year.value}`, {
          params: {
            visibility: useVisibility.value,
            academic: academicMode.value
          },
          responseType: 'blob'
        })
        
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `biblical_festivals_${year.value}.ics`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        
      } catch (err) {
        error.value = `Erro ao exportar ICS: ${err.message}`
      }
    }

    // Initialize
    onMounted(() => {
      generateCalendar()
    })

    return {
      // State
      year,
      useVisibility,
      academicMode,
      loading,
      error,
      calendarData,
      currentMonthIndex,
      selectedDay,
      
      // Constants
      weekDays,
      
      // Computed
      currentMonth,
      ussherYear,
      hebrewYear,
      calendarDays,
      currentSeasonForDate,
      
      // Methods
      generateCalendar,
      selectDay,
      previousMonth,
      nextMonth,
      goToToday,
      exportCSV,
      exportICS
    }
  }
}
</script>