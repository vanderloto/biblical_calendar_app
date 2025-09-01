"""Biblical Lunisolar Calendar Core - Calendário Bíblico Lunissolar (Core).

Este módulo implementa a lógica central do calendário bíblico sem dependências GUI.
Versão web-compatible sem tkinter.

Funcionalidades:
    - Meses ancorados em luas novas astronômicas (Skyfield)
    - Heurística opcional para primeira crescente visível em Jerusalém
    - 10 festivais bíblicos completos com nomes hebraicos e traduções
    - Eventos de Yeshua com múltiplas hipóteses
    - Fases lunares completas e estações astronômicas
    - Informações para ambos hemisférios (Jerusalém/São Paulo)
    - Exportação CSV e ICS para integração externa

Exemplo:
    >>> calendar = BiblicalCalendarCore()
    >>> months_df, embolismic, nissan_start = calendar.generate_biblical_months_dynamic(2025)

Autor:
    Vander Loto - DATAMETRIA

Versão:
    2.0.0
"""

from datetime import datetime, date, timedelta, timezone, time as dt_time
import pandas as pd
import pytz
import os
import math

# Astronomy
from skyfield import api, almanac
from skyfield.api import Topos
from astral import LocationInfo
from astral.sun import sun

# ICS
from icalendar import Calendar, Event

# ---------------- CONFIG ----------------
JERUSALEM = {"name": "Jerusalem", "region": "Israel", "lat": 31.7683, "lon": 35.2137, "tz": "Asia/Jerusalem"}
SAOPAULO  = {"name": "São Paulo",  "region": "Brazil", "lat": -23.5505, "lon": -46.6333, "tz": "America/Sao_Paulo"}

MONTH_NAMES = ["Nissan", "Iyar", "Sivan", "Tammuz", "Av", "Elul",
               "Tishrei", "Cheshvan", "Kislev", "Tevet", "Shevat", "Adar"]

# Cronologias para comparação de anos
def calculate_ussher_year(gregorian_year: int) -> int:
    """Calcula ano segundo cronologia de Ussher (Criação em 4004 AC)."""
    return gregorian_year + 4004

def calculate_hebrew_year(gregorian_year: int) -> int:
    """Calcula ano hebraico aproximado (AM - Anno Mundi)."""
    return gregorian_year + 3760

FESTIVALS_DEF = {
    # Festas da Primavera
    "Pessach": (1, 15),                    # Páscoa - Nissan 15
    "Chag HaMatzot": (1, 16),             # Festa dos Pães Asmos - Nissan 16-21 (início)
    "Omer Reshit": (1, 17),               # Primícias - Nissan 17
    
    # Festa do Verão
    "Shavuot": (3, 6),                    # Pentecostes - Sivan 6
    
    # Festas do Outono
    "Rosh Hashaná": (7, 1),               # Festa das Trombetas - Tishrei 1
    "Yom Kippur": (7, 10),                # Dia da Expiação - Tishrei 10
    "Sukkot": (7, 15),                    # Festa dos Tabernáculos - Tishrei 15
    
    # Outras celebrações importantes
    "Chanucá": (9, 25),                   # Festa das Luzes - Kislev 25
    "Purim": (12, 14),                    # Livramento de Ester - Adar 14
}

YESHUA_EVENTS_DEF = {
    "Leidat Yeshua (Nissan)": (1, 15),
    "Leidat Yeshua (Tishrei)": (7, 15),
    "Mavet Yeshua (Tzliva)": (1, 14)
}

# Traduções para português
FESTIVAL_TRANSLATIONS = {
    # Festas da Primavera
    "Pessach": "Páscoa",
    "Chag HaMatzot": "Festa dos Pães Asmos",
    "Omer Reshit": "Primícias",
    
    # Festa do Verão
    "Shavuot": "Pentecostes",
    
    # Festas do Outono
    "Rosh Hashaná": "Festa das Trombetas",
    "Yom Kippur": "Dia da Expiação",
    "Sukkot": "Festa dos Tabernáculos",
    
    # Outras celebrações
    "Chanucá": "Festa das Luzes",
    "Purim": "Festa de Purim",
    
    # Eventos de Yeshua
    "Leidat Yeshua (Nissan)": "Nascimento de Jesus (hipótese Nissan)",
    "Leidat Yeshua (Tishrei)": "Nascimento de Jesus (hipótese Sukkot)",
    "Mavet Yeshua (Tzliva)": "Crucificação de Jesus"
}

# Descrições das festas e eventos
FESTIVAL_DESCRIPTIONS = {
    "Pessach": "Celebra a libertação do povo de Israel do Egito. Simboliza redenção e sacrifício.",
    "Chag HaMatzot": "Representa a purificação do pecado, com a retirada do fermento.",
    "Omer Reshit": "Marca o início da colheita e a consagração dos primeiros frutos a Deus.",
    "Shavuot": "Comemora a entrega da Torá no Sinai e também é associada à colheita do trigo.",
    "Rosh Hashaná": "Ano Novo judaico, marcado pelo toque do shofar e chamado ao arrependimento.",
    "Yom Kippur": "Dia solene de jejum e arrependimento, buscando perdão e purificação.",
    "Sukkot": "Celebra a proteção divina durante a travessia no deserto e a colheita final.",
    "Chanucá": "Comemora a dedicação do templo e o milagre do azeite.",
    "Purim": "Celebra o livramento dos judeus na história de Ester.",
    "Leidat Yeshua (Nissan)": "Hipótese do nascimento de Jesus em Nissan 15 (Páscoa). Alguns estudiosos sugerem esta data baseando-se na simbologia do 'Cordeiro Pascal' e na proximidade com a Páscoa. Esta teoria conecta o nascimento com o tema da redenção e libertação.",
    "Leidat Yeshua (Tishrei)": "Hipótese do nascimento de Jesus em Tishrei 15 (Sukkot). Muitos eruditos favorecem esta data considerando que Sukkot era época de peregrinação a Jerusalém, explicando a lotação das hospedarias. A festa simboliza a habitação de Deus entre os homens (João 1:14 - 'o Verbo se fez carne e habitou entre nós').",
    "Mavet Yeshua (Tzliva)": "Crucificação de Jesus em Nissan 14, véspera da Páscoa (30 ou 33 d.C.). Momento central da fé cristã, quando Jesus é sacrificado como 'Cordeiro Pascal' para redenção da humanidade. A data coincide simbolicamente com o sacrifício dos cordeiros pascais no Templo.",
    "Lua Nova": "Início do mês bíblico baseado na conjunção astronômica Sol-Lua.",
    "Lua Cheia": "Fase lunar quando a Lua está completamente iluminada pelo Sol.",
    "Quarto Crescente": "Fase lunar quando metade da Lua está visível e crescendo.",
    "Quarto Minguante": "Fase lunar quando metade da Lua está visível e diminuindo.",
    "Equinócio de Primavera": "Em Jerusalém, marca o início da primavera (Hemisfério Norte)\\nEm São Paulo, marca o início do outono (Hemisfério Sul)",
    "Solstício de Verão": "Em Jerusalém, marca o início do verão (Hemisfério Norte)\\nEm São Paulo, marca o início do inverno (Hemisfério Sul)",
    "Equinócio de Outono": "Em Jerusalém, marca o início do outono (Hemisfério Norte)\\nEm São Paulo, marca o início da primavera (Hemisfério Sul)",
    "Solstício de Inverno": "Em Jerusalém, marca o início do inverno (Hemisfério Norte)\\nEm São Paulo, marca o início do verão (Hemisfério Sul)"
}

# Skyfield ephemeris - Dynamic loading based on year
TS = api.load.timescale()

# Global ephemeris variable - will be set dynamically
Eph = None
CURRENT_EPHEMERIS = "none"

# Jerusalem Topos for positional checks
JER_TOPOS = Topos(latitude_degrees=JERUSALEM["lat"], longitude_degrees=JERUSALEM["lon"])

def load_optimal_ephemeris(year: int, force_academic: bool = False) -> tuple[object, str]:
    """Carrega a efeméride mais adequada para o ano especificado."""
    global Eph, CURRENT_EPHEMERIS
    
    # Modo acadêmico sempre usa DE440
    if force_academic:
        try:
            eph = api.load('de440.bsp')
            Eph = eph
            CURRENT_EPHEMERIS = "DE440 (Modo Acadêmico)"
            return eph, CURRENT_EPHEMERIS
        except Exception as e:
            # Fallback para DE430 se DE440 não disponível
            try:
                eph = api.load('de430.bsp')
                Eph = eph
                CURRENT_EPHEMERIS = "DE430 (Fallback Acadêmico)"
                return eph, CURRENT_EPHEMERIS
            except Exception:
                raise RuntimeError(f"Modo acadêmico requer DE440/DE430. Erro: {e}")
    
    # Seleção automática baseada no ano
    if year <= 2050:
        # DE421 para anos "normais" (1900-2050)
        try:
            eph = api.load('de421.bsp')
            Eph = eph
            CURRENT_EPHEMERIS = "DE421 (Padrão)"
            return eph, CURRENT_EPHEMERIS
        except Exception as e:
            # Fallback para DE440 se DE421 não disponível
            try:
                eph = api.load('de440.bsp')
                Eph = eph
                CURRENT_EPHEMERIS = "DE440 (Fallback)"
                return eph, CURRENT_EPHEMERIS
            except Exception:
                raise RuntimeError(f"Não foi possível carregar efeméride adequada. Erro: {e}")
    else:
        # DE440 para anos > 2050
        try:
            eph = api.load('de440.bsp')
            Eph = eph
            CURRENT_EPHEMERIS = "DE440 (Ano > 2050)"
            return eph, CURRENT_EPHEMERIS
        except Exception as e:
            # Fallback para DE430
            try:
                eph = api.load('de430.bsp')
                Eph = eph
                CURRENT_EPHEMERIS = "DE430 (Fallback)"
                return eph, CURRENT_EPHEMERIS
            except Exception:
                raise RuntimeError(f"Anos > 2050 requerem DE440/DE430. Erro: {e}")

# Initialize with default ephemeris
try:
    Eph, CURRENT_EPHEMERIS = load_optimal_ephemeris(datetime.now().year)
except Exception:
    # Ultimate fallback
    Eph = api.load('de421.bsp')
    CURRENT_EPHEMERIS = "DE421 (Fallback)"

# ---------------- Astronomical helpers ----------------

def get_march_equinox(year: int) -> date:
    """Obtém a data do equinócio de março."""
    t0 = TS.utc(year, 1, 1, 0, 0, 0)
    t1 = TS.utc(year, 12, 31, 23, 59, 59)
    times, events = almanac.find_discrete(t0, t1, almanac.seasons(Eph))
    for ti, ev in zip(times, events):
        if ev == 0:
            return ti.utc_datetime().replace(tzinfo=timezone.utc).date()
    return date(year, 3, 20)

def find_new_moons_window(start_date: date, end_date: date) -> list[date]:
    """Encontra luas novas astronômicas em um período."""
    t0 = TS.utc(start_date.year, start_date.month, start_date.day, 0, 0, 0)
    t1 = TS.utc(end_date.year, end_date.month, end_date.day, 23, 59, 59)
    f = almanac.moon_phases(Eph)
    times, phases = almanac.find_discrete(t0, t1, f)
    out = []
    for ti, ph in zip(times, phases):
        if ph == 0:
            # Force UTC date calculation
            out.append(ti.utc_datetime().replace(tzinfo=timezone.utc).date())
    return out

def next_new_moon_on_or_after(start_date: date) -> date:
    """Próxima lua nova astronômica em ou após a data especificada."""
    # search 2 years ahead - use UTC midnight
    t0 = TS.utc(start_date.year, start_date.month, start_date.day, 0, 0, 0)
    t1 = TS.utc(start_date.year + 2, 12, 31, 23, 59, 59)
    f = almanac.moon_phases(Eph)
    times, phases = almanac.find_discrete(t0, t1, f)
    for ti, ph in zip(times, phases):
        if ph == 0:
            # Force UTC date calculation
            dt = ti.utc_datetime().replace(tzinfo=timezone.utc).date()
            if dt >= start_date:
                return dt
    raise RuntimeError("No new moon found in search window.")

def sun_moon_elongation_and_altitude_at(city_cfg: dict, when_dt_utc: datetime) -> tuple[float, float]:
    """Calcula elongação e altitude da lua para uma cidade."""
    # when_dt_utc: timezone-aware UTC datetime
    t = TS.utc(when_dt_utc.year, when_dt_utc.month, when_dt_utc.day,
               when_dt_utc.hour, when_dt_utc.minute, when_dt_utc.second)
    sun = Eph['sun']
    moon = Eph['moon']
    earth = Eph['earth']
    # Observer location
    obs = earth + Topos(latitude_degrees=city_cfg["lat"], longitude_degrees=city_cfg["lon"])
    # Apparent positions
    astrometric_moon = obs.at(t).observe(moon).apparent()
    astrometric_sun = obs.at(t).observe(sun).apparent()
    # Separation
    sep = astrometric_moon.separation_from(astrometric_sun).degrees
    # Moon altitude
    alt, az, distance = astrometric_moon.altaz()
    alt_deg = alt.degrees
    return sep, alt_deg

def is_first_crescent_visible_heuristic(new_moon_date: date, city_cfg: dict) -> date | None:
    """Heurística para determinar visibilidade da primeira crescente."""
    tz = pytz.timezone(city_cfg["tz"])
    # candidate days: new_moon_date, new_moon_date+1, +2, +3
    for delta in range(0, 4):
        cand = new_moon_date + timedelta(days=delta)
        # compute local sunset time for the city on 'cand' date
        loc = LocationInfo(city_cfg["name"], city_cfg["region"], city_cfg["tz"], city_cfg["lat"], city_cfg["lon"])
        try:
            s = sun(loc.observer, date=cand)
            sunset_local = s['sunset']  # timezone-aware local
        except Exception:
            # fallback: use 18:00 local
            sunset_local = tz.localize(datetime.combine(cand, dt_time(hour=18, minute=0)))
        # convert sunset to UTC
        sunset_utc = sunset_local.astimezone(pytz.UTC)
        # compute elongation and altitude at 20-30 minutes after sunset (safer)
        check_time = sunset_utc + timedelta(minutes=30)
        sep, alt = sun_moon_elongation_and_altitude_at(city_cfg, check_time)
        # thresholds: elongation >= 7-10 deg, altitude >= 3 deg
        if sep >= 10 and alt >= 3:
            # return the local date cand as the month start (Nissan 1 = that evening -> local date)
            return cand
    return None

# ---------------- Month generation ----------------

def generate_biblical_months_dynamic(reference_year: int, use_visibility_heuristic: bool = False) -> tuple[pd.DataFrame, bool, date]:
    """Gera meses bíblicos dinâmicos para um ano."""
    equinox = get_march_equinox(reference_year)
    # find first astronomical new moon on/after equinox
    nissan_astro = next_new_moon_on_or_after(equinox)
    # if using heuristic visibility, try to determine visible date for Nissan
    if use_visibility_heuristic:
        vis = is_first_crescent_visible_heuristic(nissan_astro, JERUSALEM)
        if vis is not None:
            nissan_start = vis
        else:
            nissan_start = nissan_astro
    else:
        nissan_start = nissan_astro

    # collect successive astronomical new moons (14+) to detect embolismic
    new_moons = [nissan_astro]
    cursor = nissan_astro + timedelta(days=1)
    for _ in range(14):
        nm = next_new_moon_on_or_after(cursor)
        new_moons.append(nm)
        cursor = nm + timedelta(days=1)

    # count new moons within ~370 days -> embolismic if >=13
    limit = nissan_astro + timedelta(days=370)
    count = sum(1 for nm in new_moons if nm <= limit)
    embolismic = (count >= 13)

    # Now build months using astronomical new moons, but shift start to visible date if heuristic True
    months = []
    # prepare names sequence
    if embolismic:
        # will have 13 months: Nissan..Shevat, Adar I, Adar II
        for i in range(13):
            astro_start = new_moons[i]
            # If using visibility rule, compute local visible date for this astro new moon
            if use_visibility_heuristic:
                vis = is_first_crescent_visible_heuristic(astro_start, JERUSALEM)
                start_date = vis if vis is not None else astro_start
            else:
                start_date = astro_start
            end_date = new_moons[i+1] - timedelta(days=1)
            # name mapping: 0..10 -> MONTH_NAMES[0..10]; 11->Adar I, 12->Adar II
            if i < 11:
                name = MONTH_NAMES[i]
            elif i == 11:
                name = "Adar I"
            else:
                name = "Adar II"
            months.append({"index": i+1, "name": name, "start": start_date, "end": end_date, "days": (end_date - start_date).days + 1})
    else:
        for i in range(12):
            astro_start = new_moons[i]
            if use_visibility_heuristic:
                vis = is_first_crescent_visible_heuristic(astro_start, JERUSALEM)
                start_date = vis if vis is not None else astro_start
            else:
                start_date = astro_start
            end_date = new_moons[i+1] - timedelta(days=1)
            name = MONTH_NAMES[i]
            months.append({"index": i+1, "name": name, "start": start_date, "end": end_date, "days": (end_date - start_date).days + 1})

    df = pd.DataFrame(months)
    # Ensure Nissan start returned is the mapped start (visible or astro)
    nissan_mapped_start = df.iloc[0]["start"] if not df.empty else nissan_start
    return df, embolismic, nissan_mapped_start

# ---------------- Festival mapping & ICS export ----------------

def map_festivals_to_dates(months_df: pd.DataFrame, festivals_dict: dict) -> list[dict]:
    """Mapeia festivais para datas específicas."""
    out = []
    for fname, (midx, day) in festivals_dict.items():
        row = months_df[months_df["index"] == midx]
        if not row.empty:
            start = row.iloc[0]["start"]
            ev_date = start + timedelta(days=day-1)
            out.append({"name": fname, "date": ev_date})
    return out

def export_events_to_ics(event_list: list[dict], filename: str) -> None:
    """Exporta lista de eventos para arquivo ICS."""
    cal = Calendar()
    cal.add('prodid', '-//Biblical Lunisolar Calendar//')
    cal.add('version', '2.0')
    for ev in event_list:
        ical = Event()
        ical.add('summary', ev['name'])
        # all-day event
        dt = ev['date']
        ical.add('dtstart', dt)
        ical.add('dtend', dt + timedelta(days=1))
        if ev.get('description'):
            ical.add('description', ev['description'])
        cal.add_component(ical)
    with open(filename, 'wb') as f:
        f.write(cal.to_ical())

# ---------------- Seasons & sun events ----------------

def compute_seasons_for_year(year: int) -> list[dict]:
    """Calcula as estações astronômicas para um ano."""
    t0 = TS.utc(year, 1, 1, 0, 0, 0)
    t1 = TS.utc(year, 12, 31, 23, 59, 59)
    times, events = almanac.find_discrete(t0, t1, almanac.seasons(Eph))
    mapping = {0: "March Equinox", 1: "June Solstice", 2: "September Equinox", 3: "December Solstice"}
    out = []
    for ti, ev in zip(times, events):
        out.append({"event": mapping[ev], "utc": ti.utc_datetime().replace(tzinfo=timezone.utc)})
    return out

def sunrise_sunset(location_cfg: dict, target_date: date) -> dict:
    """Calcula nascer e pôr do sol para uma localização e data."""
    loc = LocationInfo(location_cfg["name"], location_cfg["region"], location_cfg["tz"], location_cfg["lat"], location_cfg["lon"])
    try:
        s = sun(loc.observer, date=target_date)
        return {"sunrise": s["sunrise"].astimezone(pytz.timezone(location_cfg["tz"])),
                "sunset": s["sunset"].astimezone(pytz.timezone(location_cfg["tz"]))}
    except Exception:
        return {"sunrise": None, "sunset": None}

def get_moon_phases_for_year(year: int) -> list[dict]:
    """Obtém todas as fases da lua para um ano."""
    t0 = TS.utc(year, 1, 1, 0, 0, 0)
    t1 = TS.utc(year, 12, 31, 23, 59, 59)
    f = almanac.moon_phases(Eph)
    times, phases = almanac.find_discrete(t0, t1, f)
    phase_names = {0: "🌑", 1: "🌓", 2: "🌕", 3: "🌗"}
    phase_labels = {0: "Nova", 1: "Crescente", 2: "Cheia", 3: "Minguante"}
    out = []
    for ti, ph in zip(times, phases):
        out.append({
            "date": ti.utc_datetime().replace(tzinfo=timezone.utc).date(),
            "phase": ph,
            "icon": phase_names[ph],
            "name": phase_labels[ph]
        })
    return out

# ---------------- Core Calendar Class ----------------

class BiblicalCalendarCore:
    """Classe central do calendário bíblico sem dependências GUI."""
    
    def __init__(self):
        """Inicializa o calendário core."""
        self.months_df = None
        self.embolismic = False
        self.nissan_start = None
        self.current_ephemeris_name = CURRENT_EPHEMERIS
        self.seasons = []
        self.moon_phases = []
    
    def generate_calendar(self, year: int, use_visibility_heuristic: bool = False, force_academic: bool = False) -> dict:
        """Gera calendário completo para um ano."""
        # Load optimal ephemeris
        try:
            eph, eph_name = load_optimal_ephemeris(year, force_academic=force_academic)
            self.current_ephemeris_name = eph_name
        except Exception as e:
            raise RuntimeError(f"Falha ao carregar efeméride: {e}")
        
        # Generate months
        df, embol, nissan = generate_biblical_months_dynamic(year, use_visibility_heuristic)
        self.months_df = df
        self.embolismic = embol
        self.nissan_start = nissan
        
        # Generate festivals
        combined = FESTIVALS_DEF.copy()
        combined.update(YESHUA_EVENTS_DEF)
        festivals = map_festivals_to_dates(df, combined)
        
        # Generate seasons
        self.seasons = compute_seasons_for_year(year)
        
        # Generate moon phases
        self.moon_phases = get_moon_phases_for_year(year)
        
        return {
            "months": df.to_dict('records'),
            "festivals": festivals,
            "seasons": self.seasons,
            "moon_phases": self.moon_phases,
            "embolismic": embol,
            "nissan_start": nissan.isoformat(),
            "ephemeris": eph_name,
            "year": year
        }
    
    def get_day_events(self, target_date: date) -> dict:
        """Obtém eventos para um dia específico."""
        if self.months_df is None:
            return {"events": [], "season": None, "chronologies": {}}
        
        # Find month and day
        month_info = None
        day_in_month = None
        
        for _, row in self.months_df.iterrows():
            if row["start"] <= target_date <= row["end"]:
                month_info = row
                day_in_month = (target_date - row["start"]).days + 1
                break
        
        if not month_info:
            return {"events": [], "season": None, "chronologies": {}}
        
        events = []
        
        # Check festivals
        combined = FESTIVALS_DEF.copy()
        combined.update(YESHUA_EVENTS_DEF)
        
        for fname, (midx, fday) in combined.items():
            if midx == month_info["index"] and fday == day_in_month:
                portuguese_name = FESTIVAL_TRANSLATIONS.get(fname, fname)
                description = FESTIVAL_DESCRIPTIONS.get(fname, "")
                events.append({
                    "type": "festival",
                    "name": f"{fname} ({portuguese_name})",
                    "description": description
                })
        
        # Check moon phases
        for phase in self.moon_phases:
            if phase["date"] == target_date:
                description = FESTIVAL_DESCRIPTIONS.get(f"Lua {phase['name']}", "")
                events.append({
                    "type": "moon_phase",
                    "name": f"{phase['icon']} Lua {phase['name']}",
                    "description": description
                })
        
        # Check seasons
        for season in self.seasons:
            if season["utc"].date() == target_date:
                events.append({
                    "type": "season",
                    "name": f"🌍 {season['event']}",
                    "description": ""
                })
        
        # Current season
        season_info = self._get_current_season(target_date)
        
        # Chronologies
        gregorian_year = target_date.year
        chronologies = {
            "ussher": calculate_ussher_year(gregorian_year),
            "hebrew": calculate_hebrew_year(gregorian_year),
            "gregorian": gregorian_year
        }
        
        return {
            "events": events,
            "season": season_info,
            "chronologies": chronologies,
            "month_info": {
                "name": month_info["name"] if month_info else "",
                "day": day_in_month
            }
        }
    
    def _get_current_season(self, target_date: date) -> dict:
        """Obtém a estação astronômica atual para ambas as localidades."""
        if not self.seasons:
            return None
        
        current_season = None
        for i, season in enumerate(self.seasons):
            season_date = season['utc'].date()
            if i < len(self.seasons) - 1:
                next_season_date = self.seasons[i + 1]['utc'].date()
                if season_date <= target_date < next_season_date:
                    current_season = season['event']
                    break
            else:
                if season_date <= target_date:
                    current_season = season['event']
                    break
        
        if not current_season and self.seasons:
            current_season = "December Solstice"
        
        if current_season:
            season_map = {
                "March Equinox": {"jerusalem": "Primavera", "sao_paulo": "Outono"},
                "June Solstice": {"jerusalem": "Verão", "sao_paulo": "Inverno"},
                "September Equinox": {"jerusalem": "Outono", "sao_paulo": "Primavera"},
                "December Solstice": {"jerusalem": "Inverno", "sao_paulo": "Verão"}
            }
            return season_map.get(current_season, {"jerusalem": "N/A", "sao_paulo": "N/A"})
        
        return None